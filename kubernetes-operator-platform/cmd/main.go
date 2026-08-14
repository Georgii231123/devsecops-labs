package main

import (
	"flag"
	"os"

	platformv1alpha1 "github.com/Georgii231123/devsecops-labs/kubernetes-operator-platform/api/v1alpha1"
	"github.com/Georgii231123/devsecops-labs/kubernetes-operator-platform/internal/controller"
	"k8s.io/apimachinery/pkg/runtime"
	clientgoscheme "k8s.io/client-go/kubernetes/scheme"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/healthz"
	"sigs.k8s.io/controller-runtime/pkg/log/zap"
	metricsserver "sigs.k8s.io/controller-runtime/pkg/metrics/server"
)
func main() {
	var metricsAddr, probeAddr string
	flag.StringVar(&metricsAddr, "metrics-bind-address", ":8080", "metrics endpoint"); flag.StringVar(&probeAddr, "health-probe-bind-address", ":8081", "health probe endpoint")
	opts := zap.Options{Development: false}; opts.BindFlags(flag.CommandLine); flag.Parse(); ctrl.SetLogger(zap.New(zap.UseFlagOptions(&opts)))
	scheme := runtime.NewScheme(); must(clientgoscheme.AddToScheme(scheme)); must(platformv1alpha1.AddToScheme(scheme))
	mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{Scheme: scheme, Metrics: metricsserver.Options{BindAddress: metricsAddr}, HealthProbeBindAddress: probeAddr, LeaderElection: true, LeaderElectionID: "webservice-operator.platform.example.io"}); must(err)
	must((&controller.WebServiceReconciler{Client: mgr.GetClient(), Scheme: mgr.GetScheme()}).SetupWithManager(mgr)); must(mgr.AddHealthzCheck("healthz", healthz.Ping)); must(mgr.AddReadyzCheck("readyz", healthz.Ping)); must(mgr.Start(ctrl.SetupSignalHandler()))
}
func must(err error) { if err != nil { _, _ = os.Stderr.WriteString(err.Error()+"\n"); os.Exit(1) } }
