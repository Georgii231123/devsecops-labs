# Architecture

The range separates process control, supervisory access, telemetry and monitoring into explicit trust zones.

## Trust boundaries

- **OT-Control** contains the PLC simulator and process state.
- **OT-Engineering** is the only zone permitted to issue modeled control writes.
- **OT-Supervisory** reads process state through Modbus and exposes OPC UA/SCADA views.
- **OT-DMZ** receives MQTT telemetry and does not receive a route for direct controller writes.
- **Monitoring** scrapes metrics but does not receive a control permission.
- **IT** has no direct policy path into OT-Control.

Docker networks model those boundaries for the local range. They are an architectural demonstration, not a replacement for industrial firewalls or data diodes.

## Process and control

`ProcessState` models tank level, pump speed, pressure and relief valve state. `PLCController` owns writable register validation and the safety transition. Protocol adapters never mutate the physical model directly.

## Default behavior

The standalone Modbus server is read-only by default. Local host ports bind to `127.0.0.1`, and OT Docker networks are marked internal. The controlled incident drills operate against in-memory objects, so they cannot accidentally address a real controller.
