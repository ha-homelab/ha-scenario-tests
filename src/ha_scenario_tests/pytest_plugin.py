"""Opt-in callable fixture; every call creates a separate HA worker."""

import pytest

from .runner import run_scenario


@pytest.fixture
def scenario_runner():
    return run_scenario
