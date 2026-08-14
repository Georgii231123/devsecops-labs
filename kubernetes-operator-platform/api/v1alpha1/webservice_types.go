package v1alpha1

import metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

type WebServiceSpec struct {
	Image    string `json:"image"`
	Replicas *int32 `json:"replicas,omitempty"`
	Port     int32  `json:"port,omitempty"`
}

type WebServiceStatus struct {
	ReadyReplicas      int32              `json:"readyReplicas,omitempty"`
	ObservedGeneration int64              `json:"observedGeneration,omitempty"`
	Conditions         []metav1.Condition `json:"conditions,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:resource:shortName=websvc
type WebService struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`
	Spec   WebServiceSpec   `json:"spec,omitempty"`
	Status WebServiceStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true
type WebServiceList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []WebService `json:"items"`
}

func init() { SchemeBuilder.Register(&WebService{}, &WebServiceList{}) }
