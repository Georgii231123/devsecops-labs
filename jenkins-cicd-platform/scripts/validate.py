from pathlib import Path

root = Path(__file__).resolve().parents[1]
jenkinsfile = (root / "Jenkinsfile").read_text()
lib = (root / "vars/securePipeline.groovy").read_text()
casc = (root / "casc/jenkins.yaml").read_text()
plugins = set((root / "plugins.txt").read_text().splitlines())

assert "@Library('devops-shared-library@main')" in jenkinsfile
assert ":latest" not in jenkinsfile + lib
assert "trivy image" in lib
assert "syft " in lib
assert "input {" in lib
assert "allowsSignup: false" in casc
assert "numExecutors: 0" in casc
assert "configuration-as-code" in plugins
assert "matrix-auth" in plugins
print("Jenkins platform policy checks passed")
