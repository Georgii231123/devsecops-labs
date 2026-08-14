.PHONY: test lint validate modbus opcua mqtt drill up down

test:
	python -m pytest -q

lint:
	ruff check .
	bandit -q -r otlab scripts

validate:
	python scripts/validate_architecture.py

modbus:
	python scripts/modbus_smoke.py

opcua:
	python scripts/opcua_smoke.py

mqtt:
	docker compose up -d mqtt
	python scripts/mqtt_smoke.py

drill:
	python scripts/incident_drill.py --scenario unauthorized-modbus-write
	python scripts/incident_drill.py --scenario high-pressure

up:
	docker compose up -d

down:
	docker compose down -v
