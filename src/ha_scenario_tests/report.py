"""Validate the worker boundary before any caller interprets a success flag."""

import math

from .isolation import BLOCKED
from .schema import action, obj, seq, state
from .versions import HA_VERSION

FIELDS = {
    "schema",
    "name",
    "passed",
    "failures",
    "ha_version",
    "clock",
    "physical_validation",
    "isolation",
    "calls",
    "states",
    "timeline",
    "blocked_io",
    "components",
}
FAILURES = {
    "calls_mismatch",
    "forbidden_call",
    "states_mismatch",
    "blocked_io",
    "background_exception",
    "sink_contract",
    "ha_logged_error",
}


def invalid():
    raise ValueError("invalid worker report")


def elapsed(value):
    if type(value) not in (int, float) or not 0 <= value <= 30 or not math.isfinite(value):
        invalid()


def validate_report(report, document):
    """Require exact protocol fields, bounded types and self-consistent assertions."""
    obj(report, FIELDS, set(), "report")
    expected = {
        "schema": "ha-scenario-report/v1",
        "name": document["name"],
        "ha_version": HA_VERSION,
        "clock": "elapsed_monotonic",
        "isolation": "fresh_worker_temp_config_python_audit_guard",
    }
    if any(report[key] != value for key, value in expected.items()):
        invalid()
    if type(report["passed"]) is not bool or report["physical_validation"] is not False:
        invalid()
    seq(report["failures"], len(FAILURES), "report.failures")
    if any(type(item) is not str or item not in FAILURES for item in report["failures"]):
        invalid()
    if len(set(report["failures"])) != len(report["failures"]):
        invalid()
    if report["passed"] is not (not report["failures"]):
        invalid()
    seq(report["components"], 3, "report.components", 3)
    if any(type(item) is not str for item in report["components"]):
        invalid()
    if set(report["components"]) != {"automation", "blueprint", "trace"}:
        invalid()
    seq(report["blocked_io"], 256, "report.blocked_io")
    if any(type(item) is not str or item not in BLOCKED for item in report["blocked_io"]):
        invalid()
    entities = set(document["seed"])
    seq(report["calls"], 256, "report.calls")
    previous = 0
    actual = []
    for call in report["calls"]:
        obj(call, {"action", "entity_id", "elapsed_seconds"}, set(), "report.call")
        command = {key: call[key] for key in ("action", "entity_id")}
        action(command, entities, "report.call")
        elapsed(call["elapsed_seconds"])
        if call["elapsed_seconds"] < previous:
            invalid()
        previous = call["elapsed_seconds"]
        actual.append(command)
    if not isinstance(report["states"], dict) or set(report["states"]) != entities:
        invalid()
    for value in report["states"].values():
        state(value, "report.states")
    seq(report["timeline"], 32, "report.timeline")
    if len(report["timeline"]) != len(document["timeline"]):
        invalid()
    previous = 0
    for recorded, requested in zip(report["timeline"], document["timeline"], strict=True):
        obj(recorded, {"operation", "elapsed_seconds"}, set(), "report.step")
        operation = next(key for key in ("set", "event", "reload") if key in requested)
        if recorded["operation"] != operation:
            invalid()
        elapsed(recorded["elapsed_seconds"])
        if recorded["elapsed_seconds"] < previous:
            invalid()
        previous = recorded["elapsed_seconds"]
    assertions = {
        "calls_mismatch": actual != document["expect"]["calls"],
        "forbidden_call": any(call in document["expect"].get("forbidden", []) for call in actual),
        "states_mismatch": any(
            report["states"][key] != value
            for key, value in document["expect"].get("states", {}).items()
        ),
        "blocked_io": bool(report["blocked_io"]),
    }
    if any(failed != (code in report["failures"]) for code, failed in assertions.items()):
        invalid()
    return report
