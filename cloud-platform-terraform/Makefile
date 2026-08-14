CHECKOV_IMAGE ?= bridgecrew/checkov:3.3.9
TRIVY_IMAGE ?= aquasec/trivy:0.74.0

.PHONY: fmt validate scan plan

fmt:
	terraform fmt -recursive

validate:
	terraform init -backend=false
	terraform validate
	terraform fmt -check -recursive

scan:
	docker run --rm -v "$$(pwd):/src" $(CHECKOV_IMAGE) -d /src --framework terraform --compact
	docker run --rm -v "$$(pwd):/src" $(TRIVY_IMAGE) config /src

plan:
	terraform plan -var-file=environments/dev.tfvars
