# Protocol map

## Modbus/TCP

The range implements a minimal Modbus/TCP endpoint with MBAP framing, function code 3 (read holding registers) and function code 6 (write single register). The implementation exists only for the local process simulator.

Network writes are disabled by default. The CI smoke test explicitly enables them on loopback and verifies a controlled pump-speed write.

## OPC UA

The OPC UA gateway publishes read-only process variables under a `PumpStation` object. It polls the simulated PLC over Modbus. The local lab endpoint does not enable certificate security; production OPC UA deployments should use certificates, explicit trust stores and authenticated users.

## MQTT

Telemetry is published under `plant/plc-01/telemetry`. The broker allows anonymous access only because it is bound to loopback for this isolated range. The detection engine flags topics outside the approved `plant/` namespace.
