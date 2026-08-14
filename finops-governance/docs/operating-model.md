# FinOps operating model

1. **Allocate:** require stable team, environment and cost-center metadata.
2. **Observe:** export actual allocation from the organization's cost tooling.
3. **Forecast:** apply an explicit, reviewable multiplier or replace it with a forecasting feed.
4. **Guard:** fail changes when a team has no approved budget or forecast exceeds it.
5. **Optimize:** investigate idle capacity, oversized requests, replica ceilings, storage retention and commitment coverage.
6. **Review:** treat exceptions as time-bounded policy changes in Git rather than silent overrides.

This lab deliberately separates cost-source data from policy logic so it can be adapted to OpenCost, cloud billing exports or another allocation system.
