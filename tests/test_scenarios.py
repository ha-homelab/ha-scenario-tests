import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ha_scenario_tests.i18n import MESSAGES
from ha_scenario_tests.runner import run_scenario
from ha_scenario_tests.schema import InvalidScenario, load, validate

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("path", sorted((ROOT / "examples").glob("*.json")), ids=lambda p: p.stem)
@pytest.mark.runtime
def test_real_ha_scenario(path, scenario_runner):
    report = scenario_runner(load(path))
    assert report["passed"], report
    assert report["ha_version"] == "2026.10.0"
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


def test_svg_regeneration_is_deterministic():
    assets = [ROOT / "docs/images" / name for name in ("timeline.svg", "isolation.svg")]
    before = [path.read_bytes() for path in assets]
    subprocess.run([sys.executable, str(ROOT / "scripts/render_diagrams.py")], check=True)
    assert before == [path.read_bytes() for path in assets]
