# Architecture

## Hosted MCP runtime
Customer MCP servers run behind a shared control plane but inside tenant-scoped runtime boundaries. Each tenant gets workload identity, network isolation, secret isolation, quotas, and telemetry labels.

## Telemetry path
OpenTelemetry-style logs, metrics, and traces flow through a tenant-aware collector pipeline. Tool-call latency, error rate, queue depth, saturation, deploy health, and per-tenant usage are first-class signals.

## Delivery path
Build once, produce immutable artifacts, deploy progressively, watch SLOs, and roll back automatically when guardrails fail.

## Private cloud
A portable contract keeps identity, encryption, telemetry, and runtime requirements constant while adapters map them to AWS, Azure, and GCP primitives.
