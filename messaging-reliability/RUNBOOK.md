# RabbitMQ failure drill

1. Confirm cluster and queue health before changing anything.
2. Record ready/unacked counts, publish rate, consumer count and disk/memory alarms.
3. Stop one node only after confirming quorum queues still have a majority.
4. Verify publishers continue routing and consumers continue acknowledging.
5. Check DLQ growth for retry storms or poison messages.
6. Restore the node and verify it rejoins before taking another node down.
7. Never purge a DLQ during an incident without preserving or classifying the messages first.

Suggested alerts: node unavailable, quorum queue lost leader, disk alarm, memory alarm, unroutable messages, rapidly growing ready/unacked counts and DLQ growth.
