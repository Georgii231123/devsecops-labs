# Runbook

## PLC does not answer

- check `docker compose ps plc`;
- confirm port 1502 is bound only to loopback;
- inspect `docker compose logs plc`;
- run `python scripts/modbus_smoke.py` to separate application problems from Docker networking.

## OPC UA smoke fails

Run `python scripts/opcua_smoke.py`. It creates an isolated OPC UA server on port 48410 and reads one variable through a real client session, without needing Docker or the PLC service.

## MQTT smoke fails

Start only the broker with `docker compose up -d mqtt`, verify it is listening on 127.0.0.1:1883, and then run `python scripts/mqtt_smoke.py`.

## Process entered safe state

Inspect the incident evidence and PLC audit events first. In the simulator, safe state means pump speed is capped at 10% and the relief valve is open. Do not bypass the safety state by modifying the protocol adapter.

## Full cleanup

```bash
docker compose down -v
rm -rf artifacts
```
