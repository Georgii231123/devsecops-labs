CONTFEST_IMAGE ?= openpolicyagent/conftest:latest
TRIVY_IMAGE ?= aquasec/trivy:latest
CHECKOV_IMAGE ?= bridgecrew/checkov:latest

.PHONY: policy vulnerable trivy checkov scan

policy:
	docker run --rm -v "$(PWD):/project" -w /project $(CONTFEST_IMAGE) test k8s/hardened --policy policy

vulnerable:
	docker run --rm -v "$(PWD):/project" -w /project $(CONTFEST_IMAGE) test k8s/vulnerable --policy policy

trivy:
	docker run --rm -v "$(PWD):/project" $(TRIVY_IMAGE) config --severity HIGH,CRITICAL --exit-code 0 /project/k8s/hardened

checkov:
	docker run --rm -v "$(PWD):/project" $(CHECKOV_IMAGE) -d /project/k8s/hardened --framework kubernetes --compact --soft-fail

scan: policy trivy checkov
