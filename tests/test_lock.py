"""Regression: CI must not test an old HA after a metadata-only update."""
import pytest

from tools.check_lock import check


def project():
    return {"project": {"dependencies": ["homeassistant==2026.10.3"],
                        "optional-dependencies": {"test": ["pytest==9.1.1"]}}}


def test_rejects_previous_home_assistant_runtime():
    with pytest.raises(ValueError, match="Lockfile differs for homeassistant"):
        check(project(), "homeassistant==2026.10.0\npytest==9.1.1\n")


def test_rejects_stale_test_tool_pin():
    with pytest.raises(ValueError, match="Lockfile differs for pytest"):
        check(project(), "homeassistant==2026.10.3\npytest==9.0.3\n")


def test_accepts_current_runtime_and_test_pins():
    check(project(), "homeassistant==2026.10.3 \\\n    --hash=sha256:fixture\npytest==9.1.1\n")
