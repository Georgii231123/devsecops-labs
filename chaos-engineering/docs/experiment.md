# Experiment definition

**Steady state:** `/healthz` is reachable through the proxy and local latency is close to its measured baseline.

**Fault:** add 1200 ms downstream latency with Toxiproxy.

**Expected observation:** the same health request takes at least 900 ms longer than baseline.

**Recovery:** removing the toxic returns latency to within 600 ms of baseline. A backend container restart is then followed by successful retry through the unchanged proxy path.

**Blast radius:** local Docker Compose network only. No external systems are targeted.
