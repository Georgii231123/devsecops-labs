.PHONY: test lint image

test:
	pytest -q

lint:
	ruff check .

image:
	docker build -t __SERVICE_SLUG__:local .
