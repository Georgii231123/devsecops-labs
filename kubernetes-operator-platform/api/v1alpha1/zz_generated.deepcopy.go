package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
)

func (in *WebService) DeepCopyInto(out *WebService) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	in.ObjectMeta.DeepCopyInto(&out.ObjectMeta)
	out.Spec = in.Spec
	if in.Spec.Replicas != nil {
		out.Spec.Replicas = new(int32)
		*out.Spec.Replicas = *in.Spec.Replicas
	}
	out.Status = in.Status
	if in.Status.Conditions != nil {
		out.Status.Conditions = make([]metav1.Condition, len(in.Status.Conditions))
		copy(out.Status.Conditions, in.Status.Conditions)
	}
}
func (in *WebService) DeepCopy() *WebService { if in == nil { return nil }; out := new(WebService); in.DeepCopyInto(out); return out }
func (in *WebService) DeepCopyObject() runtime.Object { if c := in.DeepCopy(); c != nil { return c }; return nil }
func (in *WebServiceList) DeepCopyInto(out *WebServiceList) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	in.ListMeta.DeepCopyInto(&out.ListMeta)
	if in.Items != nil { out.Items = make([]WebService, len(in.Items)); for i := range in.Items { in.Items[i].DeepCopyInto(&out.Items[i]) } }
}
func (in *WebServiceList) DeepCopy() *WebServiceList { if in == nil { return nil }; out := new(WebServiceList); in.DeepCopyInto(out); return out }
func (in *WebServiceList) DeepCopyObject() runtime.Object { if c := in.DeepCopy(); c != nil { return c }; return nil }
