import copy
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from ha_scenario_tests import runner
from ha_scenario_tests.i18n import MESSAGES
from ha_scenario_tests.report import validate_report
from ha_scenario_tests.runner import run_scenario
from ha_scenario_tests.schema import InvalidScenario, load, validate
from ha_scenario_tests.versions import HA_VERSION

ROOT = Path(__file__).resolve().parents[1]


def synthetic_success_report(document):
    """Protocol fixture only: this is never a claim that HA executed."""
    return {
        "schema": "ha-scenario-report/v1",
        "name": document["name"],
        "passed": True,
        "failures": [],
        "ha_version": HA_VERSION,
        "clock": "elapsed_monotonic",
        "physical_validation": False,
        "isolation": "fresh_worker_temp_config_python_audit_guard",
        "calls": [
            dict(call, elapsed_seconds=(i + 1) / 10)
            for i, call in enumerate(document["expect"]["calls"])
        ],
        "states": {**document["seed"], **document["expect"].get("states", {})},
        "timeline": [
            {
                "operation": next(key for key in ("set", "event", "reload") if key in step),
                "elapsed_seconds": (i + 1) / 10,
            }
            for i, step in enumerate(document["timeline"])
        ],
        "blocked_io": [],
        "components": ["automation", "blueprint", "trace"],
    }


@pytest.mark.parametrize("path", sorted((ROOT / "examples").glob("*.json")), ids=lambda p: p.stem)
@pytest.mark.runtime
def test_real_ha_scenario(path, scenario_runner):
    report = scenario_runner(load(path))
    assert report["passed"], report
    assert report["ha_version"] == HA_VERSION
    assert report["physical_validation"] is False
    assert not report["blocked_io"]
    assert "automation" in report["components"]
    assert not {"mqtt", "esphome", "zha", "zeroconf"} & set(report["components"])


@pytest.mark.runtime
def test_wrong_expectation_and_forbidden_action_fail(scenario_runner):
    doc = load(ROOT / "examples/presence_timeout.json")
    doc["expect"]["forbidden"] = [doc["expect"]["calls"][0]]
    doc["expect"]["calls"] = []
    report = scenario_runner(doc)
    assert not report["passed"]
    assert "calls_mismatch" in report["failures"]
    assert "forbidden_call" in report["failures"]


@pytest.mark.runtime
def test_downstream_role_transfer_contract(scenario_runner):
    """A renamed role must not dispatch a command to the retired synthetic plug."""
    report = scenario_runner(load(ROOT / "tests/fixtures/role_transfer.json"))
    assert report["passed"], report
    assert not report["blocked_io"]
    assert report["states"]["switch.scenario_table"] == "off"
    assert report["states"]["switch.scenario_retired_plug"] == "on"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d.update({"config_dir": "/existing/home"}),
        lambda d: d.update({"schema": "other"}),
        lambda d: d["seed"].update({"switch.real_pump": "on"}),
        lambda d: d["automations"][0]["actions"][0].update({"action": "shell_command.run"}),
        lambda d: d["automations"][0]["actions"][0].update({"entity_id": "all"}),
        lambda d: d["automations"][0]["triggers"][0].update({"trigger": "mqtt"}),
        lambda d: d["automations"][0]["conditions"][0].update({"condition": "template"}),
        lambda d: d["timeline"][0].update({"after": float("nan")}),
        lambda d: d["timeline"][0].update({"after": True}),
        lambda d: d["timeline"][0].update({"after": 6}),
        lambda d: d["timeline"][0].update({"event": "homeassistant_start"}),
        lambda d: d["timeline"][0].update({"reload": True}),
        lambda d: d["automations"].append(copy.deepcopy(d["automations"][0])),
    ],
)
def test_admission_rejects_unsafe_or_invalid_input(mutation):
    doc = load(ROOT / "examples/presence_timeout.json")
    mutation(doc)
    with pytest.raises(InvalidScenario):
        validate(doc)


def test_duplicate_keys_and_symlink_rejected(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"schema":1,"schema":2}')
    with pytest.raises(InvalidScenario):
        load(path)
    link = tmp_path / "link.json"
    link.symlink_to(ROOT / "examples/presence_timeout.json")
    with pytest.raises(InvalidScenario):
        load(link)


def test_fifo_large_file_and_giant_integer_rejected(tmp_path):
    fifo = tmp_path / "pipe"
    os.mkfifo(fifo)
    with pytest.raises(InvalidScenario):
        load(fifo)
    large = tmp_path / "large.json"
    large.write_bytes(b" " * 65537)
    with pytest.raises(InvalidScenario):
        load(large)
    integer = tmp_path / "integer.json"
    integer.write_text("9" * 10000)
    with pytest.raises(InvalidScenario):
        load(integer)


def test_guard_blocks_tcp_udp_dns_and_process_before_io():
    code = """
import socket, subprocess
from ha_scenario_tests.isolation import install_guard
v = install_guard()
calls = [lambda: socket.getaddrinfo("example.invalid", 80),
         lambda: socket.socket().connect(("192.0.2.1", 80)),
         lambda: socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b"x", ("192.0.2.1", 9)),
         lambda: socket.socket().bind(("127.0.0.1", 0)),
         lambda: subprocess.run(["echo", "forbidden"])]
for f in calls:
    try: f()
    except RuntimeError: pass
    else: raise AssertionError("I/O was not blocked")
assert len(v) == len(calls), v
"""
    result = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_interface_library_import_uses_loaded_libc_without_subprocess():
    code = """
import ctypes.util
from ha_scenario_tests.isolation import install_guard
from ha_scenario_tests.worker import prime_interface_library
original = ctypes.util.find_library
violations = install_guard()
prime_interface_library()
import ifaddr._posix
assert ifaddr._posix.libc._name is None
assert ifaddr._posix.libc.getifaddrs
assert ctypes.util.find_library is original
assert not violations
"""
    result = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("language", sorted(MESSAGES))
def test_localized_cli_and_message_parity(language):
    assert MESSAGES[language].keys() == MESSAGES["en"].keys()
    assert all(MESSAGES[language].values())
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ha_scenario_tests.cli",
            "--lang",
            language,
            "validate",
            str(ROOT / "examples/presence_timeout.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert MESSAGES[language]["valid"] in result.stdout


@pytest.mark.parametrize("language", sorted(MESSAGES))
def test_localized_help_with_equals_language_syntax(language):
    result = subprocess.run(
        [sys.executable, "-m", "ha_scenario_tests.cli", f"--lang={language}", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    for key in ("description", "usage", "commands", "options"):
        assert MESSAGES[language][key] in result.stdout


@pytest.mark.runtime
def test_cli_json_report_is_language_independent(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ha_scenario_tests.cli",
            "--lang",
            "ru",
            "run",
            str(ROOT / "examples/stale_sensor.json"),
            "--report",
            str(tmp_path / "report.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert report["schema"] == "ha-scenario-report/v1"
    assert report["passed"]


def test_documentation_translations_and_svg_sources_exist():
    for path in [
        "README.md",
        "README.ru.md",
        "README.de.md",
        "README.es.md",
        "docs/install.md",
        "docs/install.ru.md",
        "docs/scenarios.md",
        "docs/scenarios.ru.md",
        "docs/troubleshooting.md",
        "docs/troubleshooting.ru.md",
        "docs/limits.md",
        "docs/limits.ru.md",
        "wiki/Home.md",
        "wiki/Home.ru.md",
        "wiki/_Sidebar.md",
        "scripts/render_diagrams.py",
    ]:
        assert (ROOT / path).is_file(), path


@pytest.mark.parametrize("field,value", [("action", []), ("entity_id", {}), ("action", None)])
def test_malformed_action_types_fail_closed(field, value):
    doc = load(ROOT / "examples/presence_timeout.json")
    doc["automations"][0]["actions"][0][field] = value
    with pytest.raises(InvalidScenario):
        validate(doc)


def test_huge_duration_and_bad_mode_fail_closed():
    doc = load(ROOT / "examples/presence_timeout.json")
    doc["timeline"][0]["after"] = 10**1000
    with pytest.raises(InvalidScenario):
        validate(doc)
    doc["timeline"][0]["after"] = 0
    doc["automations"][0]["mode"] = []
    with pytest.raises(InvalidScenario):
        validate(doc)


def test_timeout_is_a_runtime_error(monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("synthetic-worker", 30)

    monkeypatch.setattr(subprocess, "run", timeout)
    with pytest.raises(RuntimeError, match="timed out"):
        run_scenario(load(ROOT / "examples/presence_timeout.json"))


def test_linux_worker_environment_does_not_inherit_credentials_or_library_path(
    monkeypatch, tmp_path
):
    captured = {}

    def child(args, **kwargs):
        captured.update(kwargs["env"])
        document = json.loads(kwargs["input"])
        return subprocess.CompletedProcess(
            args, 0, json.dumps(synthetic_success_report(document)), ""
        )

    monkeypatch.setenv("LD_LIBRARY_PATH", "/untrusted/synthetic/library")
    monkeypatch.setenv("SYNTHETIC_PRIVATE_KEY", "not-a-real-secret")
    monkeypatch.setattr(runner.sys, "platform", "linux")
    monkeypatch.setattr(runner.sysconfig, "get_config_var", lambda name: str(tmp_path))
    monkeypatch.setattr(runner.subprocess, "run", child)
    run_scenario(load(ROOT / "examples/presence_timeout.json"))
    assert captured["LD_LIBRARY_PATH"] == str(tmp_path)
    assert "SYNTHETIC_PRIVATE_KEY" not in captured
    assert "PYTHONPATH" not in captured


def test_success_payload_before_native_crash_is_rejected(monkeypatch):
    monkeypatch.setattr(
        runner.subprocess,
        "run",
        lambda args, **kwargs: subprocess.CompletedProcess(args, -11, '{"passed": true}', ""),
    )
    with pytest.raises(RuntimeError, match="native_signal"):
        run_scenario(load(ROOT / "examples/presence_timeout.json"))


@pytest.mark.parametrize(
    "mutate",
    [
        lambda r: r.update(passed="false"),
        lambda r: r.update(passed=1),
        lambda r: r.update(physical_validation=0),
        lambda r: r.update(physical_validation=True),
        lambda r: r.update(ha_version="other"),
        lambda r: r.update(ha_version="2026.10.0"),
        lambda r: r.update(clock="virtual"),
        lambda r: r.pop("states"),
        lambda r: r.update(calls=[]),
        lambda r: r.update(components=["automation", "esphome", "trace"]),
        lambda r: r["calls"][0].update(elapsed_seconds=float("nan")),
        lambda r: r["states"].update({"light.unseeded": "on"}),
        lambda r: r.update(blocked_io=["socket.connect"]),
        lambda r: r.update(failures=["calls_mismatch"]),
    ],
)
def test_malformed_success_worker_report_rejected(mutate, monkeypatch):
    document = load(ROOT / "examples/presence_timeout.json")
    report = synthetic_success_report(document)
    assert validate_report(report, document) == report
    mutate(report)
    monkeypatch.setattr(
        runner.subprocess,
        "run",
        lambda args, **kwargs: subprocess.CompletedProcess(args, 0, json.dumps(report), ""),
    )
    with pytest.raises(RuntimeError, match="invalid worker report"):
        run_scenario(document)


def test_svg_regeneration_is_deterministic():
    assets = [ROOT / "docs/images" / name for name in ("timeline.svg", "isolation.svg")]
    before = [path.read_bytes() for path in assets]
    subprocess.run([sys.executable, str(ROOT / "scripts/render_diagrams.py")], check=True)
    assert before == [path.read_bytes() for path in assets]


def test_worker_protocol_version_matches_declared_runtime():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert f"homeassistant=={HA_VERSION}" in project["project"]["dependencies"]
