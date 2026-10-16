"""Parent process interface, suitable for pytest and command-line callers."""

import json
import os
import subprocess
import sys
import sysconfig

from .schema import validate


def run_scenario(document):
    """Run in a fresh child; no HA address, token, or live configuration is accepted."""
    validate(document)
    env = {k: os.environ[k] for k in ("PATH", "SYSTEMROOT", "LANG") if k in os.environ}
    env["PYTHONHASHSEED"] = "0"
    if sys.platform == "linux":
        # Relocatable CPython builds (including setup-python) need their own
        # libpython directory. Never inherit an arbitrary library search path.
        library_dir = sysconfig.get_config_var("LIBDIR")
        if library_dir and os.path.isabs(library_dir) and os.path.isdir(library_dir):
            env["LD_LIBRARY_PATH"] = library_dir
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
        category = "worker_failed"
        if "error while loading shared libraries" in proc.stderr:
            category = "shared_library_loader"
        elif "ModuleNotFoundError" in proc.stderr:
            category = "missing_dependency"
        elif proc.returncode < 0:
            category = "native_signal"
        raise RuntimeError(f"scenario worker failed (exit {proc.returncode}, {category})")
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("invalid worker report") from exc
    return report
