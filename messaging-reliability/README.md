# Messaging Reliability Lab

RabbitMQ operations lab focused on delivery guarantees, dead-letter handling and failure recovery rather than a hello-world producer.

## Demonstrated patterns

- durable topic exchange;
- quorum queues for replicated message storage;
- dead-letter exchange and DLQ;
- explicit acknowledgement/rejection behavior;
- management and Prometheus endpoints;
- a three-node cluster bootstrap example;
- automated smoke test that publishes a message, rejects it and verifies arrival in the DLQ;
- failure-drill runbook.

## Local lab

```bash
cd messaging-reliability
docker compose up -d
python3 scripts/bootstrap_and_test.py
```

Management UI: `http://localhost:15672` (`lab` / `lab`). Credentials are lab-only defaults.

## High availability

`ha/docker-compose.yml` and `ha/bootstrap-cluster.sh` model a three-node RabbitMQ cluster. Quorum queues should use three voting members in a real production topology spread across independent failure domains.

## Reliability discussion

For an interview, distinguish broker availability from message correctness. A healthy cluster does not replace publisher confirms, consumer idempotency, bounded retries, DLQs, poison-message handling, monitoring and tested recovery procedures.
