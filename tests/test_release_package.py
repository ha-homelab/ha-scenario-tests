"""Keep the released distribution and its source-version labels in agreement."""

import importlib.metadata
import tomllib
from pathlib import Path

from ha_scenario_tests import __version__


def test_distribution_version_matches_source_and_release_marker():
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["version"] == __version__
    assert (root / "version").read_text(encoding="utf-8").strip() == __version__
    assert importlib.metadata.version("ha-scenario-tests") == __version__
