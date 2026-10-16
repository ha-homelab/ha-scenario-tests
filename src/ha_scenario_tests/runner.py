"""Parent process interface, suitable for pytest and command-line callers."""

import json
import os
import subprocess
import sys

from .schema import validate


def run_scenario(document):
    """Run in a fresh child; no HA address, token, or live configuration is accepted."""
    validate(document)
    env = {k: os.environ[k] for k in ("PATH", "SYSTEMROOT", "LANG") if k in os.environ}
    env["PYTHONHASHSEED"] = "0"
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-m", "ha_scenario_tests.worker"],
            input=json.dumps(document),
            text=True,
            capture_output=True,
            env=env,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("scenario worker timed out") from exc
    if proc.returncode or not proc.stdout:
        # Do not propagate raw HA logs or private environment into public reports.
        raise RuntimeError("scenario worker failed; verify the pinned runtime installation")
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("invalid worker report") from exc
    return report
