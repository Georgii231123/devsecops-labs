package controller

import (
	"context"
	"os"
	"path/filepath"
	"testing"

	platformv1alpha1 "github.com/Georgii231123/devsecops-labs/kubernetes-operator-platform/api/v1alpha1"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/envtest"
)

func TestEnvtestReconciliation(t *testing.T) {
	if os.Getenv("KUBEBUILDER_ASSETS") == "" {
		t.Skip("KUBEBUILDER_ASSETS is not set")
	}
	env := &envtest.Environment{
		CRDDirectoryPaths: []string{filepath.Join("..", "..", "config", "crd", "bases")},
	}
	cfg, err := env.Start()
	if err != nil {
		t.Fatal(err)
	}
	defer func() { _ = env.Stop() }()

	scheme := runtime.NewScheme()
	for _, add := range []func(*runtime.Scheme) error{
		platformv1alpha1.AddToScheme,
		appsv1.AddToScheme,
		corev1.AddToScheme,
	} {
		if err := add(scheme); err != nil {
			t.Fatal(err)
		}
	}
	c, err := client.New(cfg, client.Options{Scheme: scheme})
	if err != nil {
		t.Fatal(err)
	}

	ctx := context.Background()
	if err := c.Create(ctx, &corev1.Namespace{ObjectMeta: metav1.ObjectMeta{Name: "default"}}); err != nil {
		t.Fatal(err)
	}
	web := &platformv1alpha1.WebService{
		ObjectMeta: metav1.ObjectMeta{Name: "catalog", Namespace: "default"},
		Spec: platformv1alpha1.WebServiceSpec{
			Image: "ghcr.io/example/catalog:2.0.0",
			Port:  8080,
		},
	}
	if err := c.Create(ctx, web); err != nil {
		t.Fatal(err)
	}
	r := &WebServiceReconciler{Client: c, Scheme: scheme}
	req := ctrl.Request{NamespacedName: types.NamespacedName{Name: web.Name, Namespace: web.Namespace}}
	if _, err := r.Reconcile(ctx, req); err != nil {
		t.Fatal(err)
	}
	if _, err := r.Reconcile(ctx, req); err != nil {
		t.Fatal(err)
	}

	var deployment appsv1.Deployment
	if err := c.Get(ctx, req.NamespacedName, &deployment); err != nil {
		t.Fatalf("deployment not created against envtest API server: %v", err)
	}
}
