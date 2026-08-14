from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
policies = {p.stem: yaml.safe_load(p.read_text()) for p in (root / "policies").glob("*.yaml")}
required = {
    "disallow-privileged",
    "require-nonroot",
    "disallow-latest",
    "require-runtime-controls",
    "disallow-hostpath",
    "add-seccomp",
    "generate-default-deny",
}
assert required <= set(policies), sorted(set(required) - set(policies))
for name, policy in policies.items():
    assert policy["apiVersion"] == "kyverno.io/v1", name
    assert policy["kind"] == "ClusterPolicy", name
    assert policy["spec"]["rules"], name

seccomp = policies["add-seccomp"]
assert "RuntimeDefault" in str(seccomp)
generate = policies["generate-default-deny"]
assert "NetworkPolicy" in str(generate)
assert "Ingress" in str(generate) and "Egress" in str(generate)

good = yaml.safe_load((root / "fixtures/good.yaml").read_text())
container = good["spec"]["template"]["spec"]["containers"][0]
assert good["spec"]["template"]["spec"]["securityContext"]["runAsNonRoot"] is True
assert container["securityContext"]["privileged"] is False
assert container["resources"]["requests"] and container["resources"]["limits"]
assert container["readinessProbe"] and container["livenessProbe"]
print("kyverno admission-control contract checks passed")
