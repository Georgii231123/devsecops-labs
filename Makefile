CONFTEST_IMAGE ?= openpolicyagent/conftest:v0.69.0
TRIVY_IMAGE ?= aquasec/trivy:0.74.0
CHECKOV_IMAGE ?= bridgecrew/checkov:3.3.9
PYTHON ?= python3

.PHONY: audit policy vulnerable trivy checkov scan

audit:
	$(PYTHON) tools/repo_audit.py

policy:
	docker run --rm -v "$(PWD):/project" -w /project $(CONFTEST_IMAGE) test k8s/hardened --policy policy

vulnerable:
	docker run --rm -v "$(PWD):/project" -w /project $(CONFTEST_IMAGE) test k8s/vulnerable --policy policy

trivy:
	docker run --rm -v "$(PWD):/project" $(TRIVY_IMAGE) config --severity HIGH,CRITICAL --exit-code 0 /project/k8s/hardened

checkov:
	docker run --rm -v "$(PWD):/project" $(CHECKOV_IMAGE) -d /project/k8s/hardened --framework kubernetes --compact --soft-fail

scan: policy trivy checkov
