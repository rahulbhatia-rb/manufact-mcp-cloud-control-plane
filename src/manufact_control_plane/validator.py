from dataclasses import dataclass

@dataclass
class Result:
    ok: bool
    violations: list[str]


def validate(contract):
    checks = []
    observability = contract.get("observability", {})
    checks.append((set(["logs", "metrics", "traces"]).issubset(set(observability.get("signals", []))), "logs, metrics, and traces are required"))
    checks.append((observability.get("alert_latency_seconds", 999) <= 60, "alerting must surface failures within 60 seconds"))
    checks.append((observability.get("tenant_labels") is True, "telemetry must include tenant attribution"))

    tenancy = contract.get("tenancy", {})
    checks.append((tenancy.get("network_isolation") is True, "tenant network isolation is required"))
    checks.append((tenancy.get("workload_identity") is True, "workload identity is required"))
    checks.append((tenancy.get("per_tenant_secrets") is True, "per-tenant secret isolation is required"))
    checks.append((tenancy.get("resource_quotas") is True, "per-tenant resource quotas are required"))

    runtime = contract.get("runtime", {})
    checks.append((runtime.get("max_tool_call_p95_ms", 10000) <= 2000, "tool-call p95 objective must be at most 2 seconds"))
    checks.append((runtime.get("error_rate_slo", 1.0) <= 0.01, "error-rate SLO must be at most 1 percent"))
    checks.append((runtime.get("autoscale_on_queue_depth") is True, "queue-depth autoscaling is required"))

    delivery = contract.get("delivery", {})
    checks.append((delivery.get("immutable_artifacts") is True, "release artifacts must be immutable"))
    checks.append((delivery.get("progressive_delivery") is True, "progressive delivery is required"))
    checks.append((delivery.get("automatic_rollback") is True, "automatic rollback is required"))

    private_cloud = contract.get("private_cloud", {})
    clouds = set(private_cloud.get("supported_clouds", []))
    checks.append((set(["aws", "azure", "gcp"]).issubset(clouds), "private-cloud blueprint must cover AWS, Azure, and GCP"))
    checks.append((private_cloud.get("customer_owned_kms") is True, "customer-owned encryption keys are required"))

    violations = [message for passed, message in checks if not passed]
    return Result(ok=len(violations) == 0, violations=violations)
