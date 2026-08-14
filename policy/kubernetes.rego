package kubernetes.security

import rego.v1

is_deployment if {
    input.kind == "Deployment"
}

drops_all(container) if {
    "ALL" in container.securityContext.capabilities.drop
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    container.securityContext.privileged == true
    msg := sprintf("container %q must not run privileged", [container.name])
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    not container.securityContext.allowPrivilegeEscalation == false
    msg := sprintf("container %q must set allowPrivilegeEscalation=false", [container.name])
}

deny contains msg if {
    is_deployment
    not input.spec.template.spec.securityContext.runAsNonRoot == true
    msg := "pod must set securityContext.runAsNonRoot=true"
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    not container.securityContext.readOnlyRootFilesystem == true
    msg := sprintf("container %q must use a read-only root filesystem", [container.name])
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    not drops_all(container)
    msg := sprintf("container %q must drop ALL Linux capabilities", [container.name])
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    not container.resources.limits.cpu
    msg := sprintf("container %q must define a CPU limit", [container.name])
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    not container.resources.limits.memory
    msg := sprintf("container %q must define a memory limit", [container.name])
}

deny contains msg if {
    is_deployment
    some container in input.spec.template.spec.containers
    endswith(container.image, ":latest")
    msg := sprintf("container %q must not use the latest image tag", [container.name])
}

deny contains msg if {
    is_deployment
    input.spec.template.spec.hostNetwork == true
    msg := "hostNetwork must not be enabled"
}

deny contains msg if {
    is_deployment
    input.spec.template.spec.hostPID == true
    msg := "hostPID must not be enabled"
}

deny contains msg if {
    is_deployment
    input.spec.template.spec.hostIPC == true
    msg := "hostIPC must not be enabled"
}

deny contains msg if {
    is_deployment
    some volume in input.spec.template.spec.volumes
    volume.hostPath
    msg := sprintf("hostPath volume %q is not allowed", [volume.name])
}

deny contains msg if {
    is_deployment
    not input.spec.template.spec.securityContext.seccompProfile.type == "RuntimeDefault"
    msg := "pod must use the RuntimeDefault seccomp profile"
}
