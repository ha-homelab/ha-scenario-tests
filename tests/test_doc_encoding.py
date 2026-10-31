"""Documentation validation must not depend on the host text encoding."""

import os
import subprocess
import sys
from pathlib import Path


def documentation_environment(environ):
    """Pass only process lookup and explicit Git context, never host secrets."""
    allowed = ("PATH", "SYSTEMROOT", "SystemRoot", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")
    result = {key: environ[key] for key in allowed if key in environ}
    result.update(LC_ALL="C", PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
    return result


def test_documentation_environment_excludes_unrelated_host_values():
    result = documentation_environment({"PATH": "/usr/bin", "SYNTHETIC_SECRET": "fixture"})
    assert result == {
        "PATH": "/usr/bin",
        "LC_ALL": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
    }


def test_documentation_checks_use_utf8_under_ascii_locale():
    root = Path(__file__).resolve().parents[1]
    env = documentation_environment(os.environ)
    subprocess.run(
        [sys.executable, "tools/check_docs.py"],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
    )
