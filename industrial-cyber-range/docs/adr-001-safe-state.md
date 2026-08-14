# ADR-001: Safe state belongs to the controller layer

## Status

Accepted.

## Decision

Safety decisions are implemented in the PLC controller/process layer rather than in SCADA, MQTT, OPC UA or the detection engine.

## Rationale

Observability and detection components may be unavailable during an incident. The simulated process must still enforce its own pressure and tank-level boundaries. Protocol gateways can report a state or request a valid operation, but they do not override the process safety contract.

## Consequences

- the same safety behavior applies to every protocol adapter;
- unit tests can verify the safety contract without starting network services;
- detections provide evidence but are not a prerequisite for entering safe state;
- recovery requires an explicit process reset rather than a monitoring-side action.
