# Nginx & HAProxy Load Balancing Lab

A practical reverse-proxy and failover lab with two backends and two independent load balancers.

## What is exercised

- Nginx least-connection upstream balancing;
- HAProxy round-robin balancing with active HTTP health checks;
- connection, client and server timeouts;
- retry/failover behavior;
- backend health endpoint;
- HAProxy statistics endpoint;
- CI failure drill: send traffic to both nodes, stop one backend, verify both proxies continue serving through the surviving backend.

## Run

```bash
cd edge-load-balancing
docker compose up --build -d
./scripts/failure_drill.sh
```

Nginx: `http://localhost:8080`, HAProxy: `http://localhost:8081`, HAProxy stats: `http://localhost:8404/stats`.

## Production considerations

A real edge tier also needs TLS policy, certificate automation, request/body limits, trusted proxy configuration, rate limiting, WAF strategy where appropriate, access-log correlation, observability, capacity tests and multiple proxy instances behind an external load balancer or anycast/L4 tier.
