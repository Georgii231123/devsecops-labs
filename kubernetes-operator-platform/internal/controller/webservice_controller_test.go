package controller

import (
	"context"
	"testing"

	platformv1alpha1 "github.com/Georgii231123/devsecops-labs/kubernetes-operator-platform/api/v1alpha1"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client/fake"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
)

func TestReconcileCreatesHardenedRuntime(t *testing.T) {
	ctx := context.Background()
	scheme := testScheme(t)
	replicas := int32(3)
	web := &platformv1alpha1.WebService{
		ObjectMeta: metav1.ObjectMeta{Name: "payments", Namespace: "default"},
		Spec: platformv1alpha1.WebServiceSpec{
			Image:    "ghcr.io/example/payments:1.4.2",
			Replicas: &replicas,
			Port:     8080,
		},
	}
	c := fake.NewClientBuilder().WithScheme(scheme).WithStatusSubresource(web).WithObjects(web).Build()
	r := &WebServiceReconciler{Client: c, Scheme: scheme}
	req := ctrl.Request{NamespacedName: types.NamespacedName{Name: web.Name, Namespace: web.Namespace}}

	if _, err := r.Reconcile(ctx, req); err != nil {
		t.Fatal(err)
	}
	if _, err := r.Reconcile(ctx, req); err != nil {
		t.Fatal(err)
	}

	var got platformv1alpha1.WebService
	if err := c.Get(ctx, req.NamespacedName, &got); err != nil {
		t.Fatal(err)
	}
	if !controllerutil.ContainsFinalizer(&got, webServiceFinalizer) {
		t.Fatal("expected finalizer")
	}

	var deployment appsv1.Deployment
	if err := c.Get(ctx, req.NamespacedName, &deployment); err != nil {
		t.Fatal(err)
	}
	container := deployment.Spec.Template.Spec.Containers[0]
	if deployment.Spec.Replicas == nil || *deployment.Spec.Replicas != replicas {
		t.Fatal("replica contract failed")
	}
	if container.SecurityContext == nil ||
		container.SecurityContext.AllowPrivilegeEscalation == nil ||
		*container.SecurityContext.AllowPrivilegeEscalation {
		t.Fatal("allowPrivilegeEscalation must be false")
	}
	if container.SecurityContext.ReadOnlyRootFilesystem == nil || !*container.SecurityContext.ReadOnlyRootFilesystem {
		t.Fatal("readOnlyRootFilesystem must be true")
	}
	if len(container.SecurityContext.Capabilities.Drop) != 1 || container.SecurityContext.Capabilities.Drop[0] != "ALL" {
		t.Fatal("must drop ALL capabilities")
	}

	var service corev1.Service
	if err := c.Get(ctx, req.NamespacedName, &service); err != nil {
		t.Fatal(err)
	}
	var metadata corev1.ConfigMap
	if err := c.Get(ctx, types.NamespacedName{Name: "payments-metadata", Namespace: "default"}, &metadata); err != nil {
		t.Fatal(err)
	}
}

func testScheme(t *testing.T) *runtime.Scheme {
	t.Helper()
	s := runtime.NewScheme()
	for _, add := range []func(*runtime.Scheme) error{
		platformv1alpha1.AddToScheme,
		appsv1.AddToScheme,
		corev1.AddToScheme,
	} {
		if err := add(s); err != nil {
			t.Fatal(err)
		}
	}
	return s
}
