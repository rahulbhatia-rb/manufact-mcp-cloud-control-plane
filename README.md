# Manufact MCP Cloud Control Plane

A small executable proof-of-concept for the infrastructure problems in Manufact's cloud-platform role: hosting customer MCP servers, observing millions of tool calls, isolating tenants, shipping safely, and making the platform portable into customer-owned AWS, Azure, and GCP environments.

## Why this project
Manufact is effectively building a PaaS for MCP servers and apps. That creates a tight coupling between infrastructure reliability and end-user AI-agent behavior: a slow or failed tool call becomes a bad agent experience immediately.

This POC turns the platform expectations into an **executable deployment contract**. A customer MCP workload is considered production-ready only if it satisfies reliability, observability, tenancy, release, and private-cloud requirements.

## What the gate checks

### Observability
- logs, metrics, and traces are all required
- telemetry must be tenant-attributed
- alerting must surface failures within 60 seconds

### Tenant isolation
- network isolation
- workload identity instead of static credentials
- per-tenant secrets
- resource quotas to contain noisy neighbors

### MCP runtime reliability
- p95 tool-call latency objective <= 2 seconds
- error-rate SLO <= 1%
- queue-depth-driven autoscaling

### Release engineering
- immutable artifacts
- progressive delivery
- automatic rollback

### Private-cloud portability
- AWS, Azure, and GCP support
- customer-owned encryption keys

## Repository structure

```text
src/manufact_control_plane/
  validator.py        executable readiness policy
  cli.py              command-line evaluator
examples/
  production.json     production-ready MCP workload contract
  unsafe.json         intentionally incomplete workload
tests/
  test_validator.py   acceptance/rejection tests
docs/
  architecture.md     platform architecture notes
  30-60-90.md         first-infra-engineer execution plan
```

## Run it

```bash
PYTHONPATH=src python -m manufact_control_plane.cli examples/production.json
PYTHONPATH=src python -m manufact_control_plane.cli examples/unsafe.json
pytest -q
```

Expected behavior:

```text
READY: contract satisfies Manufact Cloud platform requirements
```

The unsafe example is blocked with explicit violations rather than a generic failure.

## Production architecture I would evolve this toward

```text
                         +----------------------+
Claude / ChatGPT / Agent | Manufact Edge / API  |
------------------------>| auth + rate controls |
                         +----------+-----------+
                                    |
                         +----------v-----------+
                         | MCP Runtime Router   |
                         | tenant + version     |
                         +-----+------------+---+
                               |            |
                    +----------v--+      +--v-----------+
                    | Tenant A MCP|      | Tenant B MCP |
                    | runtime     |      | runtime      |
                    +------+------+
                           |
        +------------------+-------------------+
        |                  |                   |
   metrics/logs         traces/events       queue depth
        |                  |                   |
        +------------+-----+-------------------+
                     |
              +------v-------+
              | OTel pipeline|
              +------+-------+
                     |
       +-------------+----------------+
       | dashboards | alerts | SLOs   |
       +-------------+----------------+
```

## Observability model
For every MCP tool call I would want, at minimum:
- tenant ID
- MCP server ID and version
- tool name
- request outcome
- total latency and upstream latency
- retry count
- queue delay
- runtime saturation
- deployment version
- trace/span identifiers

The goal is to answer three questions quickly: **what broke, which customers are affected, and what changed?**

## Scaling model
A tool-call platform should avoid scaling only on CPU. MCP workloads can become queue-bound, concurrency-bound, or upstream-API-bound before CPU saturates. The contract therefore models queue-depth autoscaling as mandatory; in production I would combine queue depth, concurrency, saturation, and latency signals.

## Multi-tenant security
The control plane is shared, but trust is not. The runtime design assumes:
- tenant-scoped identities
- least-privilege access to data stores and queues
- deny-by-default network boundaries
- tenant-specific secrets
- customer-owned keys for private-cloud deployments
- quotas and rate controls to reduce cross-tenant blast radius

## Private-cloud blueprint
The platform contract intentionally separates requirements from provider primitives. The same contract can map to:
- AWS: EKS/ECS, IAM roles, KMS, CloudWatch/OTel, ALB/API Gateway
- Azure: AKS, Managed Identity, Key Vault, Azure Monitor
- GCP: GKE, Workload Identity, Cloud KMS, Cloud Monitoring

That makes customer-hosted deployments reproducible without creating three unrelated products.

## Release engineering
For a platform carrying customer tool calls, shipping fast only works if rollback is faster than failure propagation. The target release path is:
1. build immutable artifact
2. policy and test gates
3. progressive rollout
4. compare error/latency SLOs
5. automatically promote or roll back
6. retain release provenance for incident review

## Design exercise readiness
Manufact's interview includes architecting the hosting and observability layer. This repo is intentionally structured around that problem: runtime isolation, telemetry, failure detection, autoscaling, and customer-owned cloud deployment.

## 30 / 60 / 90
See [`docs/30-60-90.md`](docs/30-60-90.md) for how I would approach ownership as the first infrastructure-focused engineer.

## Author
Rahul H Bhatia

- LinkedIn: https://www.linkedin.com/in/rahul-h-bhatia/
- Portfolio: https://rahulhbhatia.vercel.app
- AWS badges: https://www.credly.com/users/rahul-h-bhatia/badges
