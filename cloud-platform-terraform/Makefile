.PHONY: fmt validate scan plan

fmt:
	terraform fmt -recursive

validate:
	terraform init -backend=false
	terraform validate
	terraform fmt -check -recursive

scan:
	docker run --rm -v "$$(pwd):/src" bridgecrew/checkov:latest -d /src --framework terraform --compact
	docker run --rm -v "$$(pwd):/src" aquasec/trivy:latest config /src

plan:
	terraform plan -var-file=environments/dev.tfvars
