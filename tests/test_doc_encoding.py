"""Documentation validation must not depend on the host text encoding."""

import os
import subprocess
import sys
from pathlib import Path


def test_documentation_checks_use_utf8_under_ascii_locale():
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ, LC_ALL="C", PYTHONUTF8="0", PYTHONCOERCECLOCALE="0")
    subprocess.run(
        [sys.executable, "tools/check_docs.py"],
        cwd=root,
        env=env,
        check=True,
        capture_output=True,
    )
