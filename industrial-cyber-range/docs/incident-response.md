# Incident response

## Unauthorized control write

1. preserve the protocol event and source asset identity;
2. confirm the PLC rejected the operation;
3. verify the current process state before taking any control action;
4. validate segmentation between the source zone and OT-Control;
5. review recent engineering and SCADA writes;
6. keep the controller in its existing safe condition unless the process requires a predefined safe-state procedure.

## Unsafe process condition

1. confirm the measurement from more than one signal where possible;
2. verify the simulator entered its predefined safe state;
3. preserve the PLC audit trail and telemetry around the transition;
4. identify whether the cause was process drift, an authorized command or an unauthorized command;
5. return to normal operation only after the modeled process is stable.

CI writes structured reports for both drills to `artifacts/` and uploads them as workflow evidence.
