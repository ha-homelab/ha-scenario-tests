"""Refuse a lockfile that differs from declared runtime and test versions."""
from pathlib import Path
import re
import tomllib


def check(project, lock):
    def normalized(name):
        return re.sub(r"[-_.]+", "-", name).lower()
    pins = {}
    for line in lock.splitlines():
        match = re.match(r"^([A-Za-z0-9_.-]+)==([^\s;]+)", line)
        if match:
            name = normalized(match[1])
            if name in pins:
                raise ValueError(f"Duplicate lock entry: {name}")
            pins[name] = match[2]
    declared = project["project"].get("dependencies", [])[:]
    declared += project["project"].get("optional-dependencies", {}).get("test", [])
    for requirement in declared:
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s;]+)", requirement)
        if not match:
            raise ValueError(f"Expected an exact direct dependency pin: {requirement}")
        name, expected = normalized(match[1]), match[2]
        if pins.get(name) != expected:
            raise ValueError(f"Lockfile differs for {name}: expected {expected}, got {pins.get(name)}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    check(tomllib.loads((root / "pyproject.toml").read_text()),
          (root / "requirements.lock").read_text())
    print("Runtime and test dependency pins match the lockfile")
