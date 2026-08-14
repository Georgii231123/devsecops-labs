# Recovery objectives

This lab uses logical backups, so the recovery objectives are illustrative rather than claims about a production system.

- **Target RPO:** 24 hours with a daily logical backup schedule.
- **Target RTO:** 60 minutes for a small database when the latest dump and a healthy PostgreSQL instance are available.

A production system requiring lower RPO would normally add WAL archiving / point-in-time recovery and off-host encrypted backup storage. Lower RTO would require measured restore drills, automation and capacity planning based on actual dataset size.
