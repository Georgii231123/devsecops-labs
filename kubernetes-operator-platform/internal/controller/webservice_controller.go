package controller

import (
	"context"
	"fmt"
	"time"

	platformv1alpha1 "github.com/Georgii231123/devsecops-labs/kubernetes-operator-platform/api/v1alpha1"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	meta "k8s.io/apimachinery/pkg/api/meta"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/apimachinery/pkg/util/intstr"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
)

const webServiceFinalizer = "platform.example.io/finalizer"

type WebServiceReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=platform.example.io,resources=webservices,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=platform.example.io,resources=webservices/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=platform.example.io,resources=webservices/finalizers,verbs=update
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups="",resources=services;configmaps,verbs=get;list;watch;create;update;patch;delete
func (r *WebServiceReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	var web platformv1alpha1.WebService
	if err := r.Get(ctx, req.NamespacedName, &web); err != nil {
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	if !web.DeletionTimestamp.IsZero() {
		return r.finalize(ctx, &web)
	}

	if !controllerutil.ContainsFinalizer(&web, webServiceFinalizer) {
		controllerutil.AddFinalizer(&web, webServiceFinalizer)
		if err := r.Update(ctx, &web); err != nil {
			return ctrl.Result{}, err
		}
		return ctrl.Result{Requeue: true}, nil
	}

	if err := r.reconcileDeployment(ctx, &web); err != nil {
		return ctrl.Result{}, err
	}
	if err := r.reconcileService(ctx, &web); err != nil {
		return ctrl.Result{}, err
	}
	if err := r.reconcileMetadataConfigMap(ctx, &web); err != nil {
		return ctrl.Result{}, err
	}
	if err := r.updateStatus(ctx, &web); err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{RequeueAfter: 20 * time.Second}, nil
}

func (r *WebServiceReconciler) finalize(ctx context.Context, web *platformv1alpha1.WebService) (ctrl.Result, error) {
	if !controllerutil.ContainsFinalizer(web, webServiceFinalizer) {
		return ctrl.Result{}, nil
	}

	key := types.NamespacedName{Name: web.Name + "-metadata", Namespace: web.Namespace}
	var configMap corev1.ConfigMap
	if err := r.Get(ctx, key, &configMap); err == nil {
		if err := r.Delete(ctx, &configMap); err != nil && !apierrors.IsNotFound(err) {
			return ctrl.Result{}, err
		}
	} else if !apierrors.IsNotFound(err) {
		return ctrl.Result{}, err
	}

	controllerutil.RemoveFinalizer(web, webServiceFinalizer)
	return ctrl.Result{}, r.Update(ctx, web)
}

func (r *WebServiceReconciler) reconcileDeployment(ctx context.Context, web *platformv1alpha1.WebService) error {
	deployment := &appsv1.Deployment{ObjectMeta: metav1.ObjectMeta{Name: web.Name, Namespace: web.Namespace}}
	_, err := controllerutil.CreateOrUpdate(ctx, r.Client, deployment, func() error {
		labels := map[string]string{
			"app.kubernetes.io/name":       web.Name,
			"app.kubernetes.io/managed-by": "webservice-operator",
		}
		replicas := int32(2)
		if web.Spec.Replicas != nil {
			replicas = *web.Spec.Replicas
		}
		port := web.Spec.Port
		if port == 0 {
			port = 8080
		}
		deployment.Spec.Replicas = &replicas
		deployment.Spec.Selector = &metav1.LabelSelector{MatchLabels: labels}
		deployment.Spec.Template.ObjectMeta.Labels = labels
		deployment.Spec.Template.Spec.AutomountServiceAccountToken = boolPtr(false)
		deployment.Spec.Template.Spec.SecurityContext = &corev1.PodSecurityContext{
			RunAsNonRoot:   boolPtr(true),
			SeccompProfile: &corev1.SeccompProfile{Type: corev1.SeccompProfileTypeRuntimeDefault},
		}
		deployment.Spec.Template.Spec.Containers = []corev1.Container{{
			Name:  "app",
			Image: web.Spec.Image,
			Ports: []corev1.ContainerPort{{ContainerPort: port}},
			SecurityContext: &corev1.SecurityContext{
				AllowPrivilegeEscalation: boolPtr(false),
				ReadOnlyRootFilesystem:   boolPtr(true),
				RunAsNonRoot:             boolPtr(true),
				Capabilities:             &corev1.Capabilities{Drop: []corev1.Capability{"ALL"}},
			},
			Resources: corev1.ResourceRequirements{
				Requests: corev1.ResourceList{
					corev1.ResourceCPU:    resource.MustParse("50m"),
					corev1.ResourceMemory: resource.MustParse("64Mi"),
				},
				Limits: corev1.ResourceList{
					corev1.ResourceCPU:    resource.MustParse("500m"),
					corev1.ResourceMemory: resource.MustParse("256Mi"),
				},
			},
			ReadinessProbe: httpProbe(port),
			LivenessProbe:  httpProbe(port),
		}}
		return controllerutil.SetControllerReference(web, deployment, r.Scheme)
	})
	return err
}

func (r *WebServiceReconciler) reconcileService(ctx context.Context, web *platformv1alpha1.WebService) error {
	service := &corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: web.Name, Namespace: web.Namespace}}
	_, err := controllerutil.CreateOrUpdate(ctx, r.Client, service, func() error {
		port := web.Spec.Port
		if port == 0 {
			port = 8080
		}
		service.Spec.Selector = map[string]string{"app.kubernetes.io/name": web.Name}
		service.Spec.Ports = []corev1.ServicePort{{Port: port, TargetPort: intstr.FromInt32(port)}}
		return controllerutil.SetControllerReference(web, service, r.Scheme)
	})
	return err
}

func (r *WebServiceReconciler) reconcileMetadataConfigMap(ctx context.Context, web *platformv1alpha1.WebService) error {
	configMap := &corev1.ConfigMap{ObjectMeta: metav1.ObjectMeta{Name: web.Name + "-metadata", Namespace: web.Namespace}}
	_, err := controllerutil.CreateOrUpdate(ctx, r.Client, configMap, func() error {
		configMap.Data = map[string]string{
			"managedBy": "webservice-operator",
			"image":     web.Spec.Image,
		}
		return controllerutil.SetControllerReference(web, configMap, r.Scheme)
	})
	return err
}

func (r *WebServiceReconciler) updateStatus(ctx context.Context, web *platformv1alpha1.WebService) error {
	var deployment appsv1.Deployment
	if err := r.Get(ctx, types.NamespacedName{Name: web.Name, Namespace: web.Namespace}, &deployment); err != nil {
		return err
	}

	desired := int32(2)
	if web.Spec.Replicas != nil {
		desired = *web.Spec.Replicas
	}
	status := metav1.ConditionFalse
	reason := "Progressing"
	if deployment.Status.ReadyReplicas >= desired {
		status = metav1.ConditionTrue
		reason = "Available"
	}

	web.Status.ReadyReplicas = deployment.Status.ReadyReplicas
	web.Status.ObservedGeneration = web.Generation
	meta.SetStatusCondition(&web.Status.Conditions, metav1.Condition{
		Type:               "Ready",
		Status:             status,
		Reason:             reason,
		Message:            fmt.Sprintf("%d/%d replicas are ready", deployment.Status.ReadyReplicas, desired),
		ObservedGeneration: web.Generation,
	})
	return r.Status().Update(ctx, web)
}

func (r *WebServiceReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&platformv1alpha1.WebService{}).
		Owns(&appsv1.Deployment{}).
		Owns(&corev1.Service{}).
		Owns(&corev1.ConfigMap{}).
		Complete(r)
}

func boolPtr(v bool) *bool { return &v }

func httpProbe(port int32) *corev1.Probe {
	return &corev1.Probe{
		ProbeHandler: corev1.ProbeHandler{
			HTTPGet: &corev1.HTTPGetAction{Path: "/healthz", Port: intstr.FromInt32(port)},
		},
		InitialDelaySeconds: 5,
		PeriodSeconds:       10,
	}
}
