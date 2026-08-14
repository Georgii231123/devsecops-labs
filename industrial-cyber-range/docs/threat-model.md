# Threat model

## Protected assets

1. process safety state;
2. PLC write authority;
3. integrity of tank level, pressure and pump telemetry;
4. engineering and SCADA trust boundaries;
5. incident evidence.

## Modeled abuse cases

- direct Modbus write attempt from the IT zone;
- unknown OPC UA client;
- MQTT publication outside the approved namespace;
- unsafe process pressure;
- an unexpected direct path between IT and OT-Control.

## Controls

- default-deny network policy model;
- explicit writer allowlist in the PLC controller;
- read-only Modbus network service by default;
- process range validation;
- automatic safe-state transition;
- asset and zone inventory validation;
- protocol-aware detection rules;
- CI regression tests for both allowed and denied behavior.

## Out of scope

The range does not scan networks, discover external PLCs, exploit vendor devices or transmit commands to non-local industrial endpoints.
