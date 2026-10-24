"""Verify built packages retain their source modules and documentation metadata."""

import argparse
import tarfile
import tomllib
import zipfile
from pathlib import Path, PurePosixPath


def check(root: Path, dist: Path) -> None:
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    name = project["name"].replace("-", "_")
    version = project["version"]
    wheel = dist / f"{name}-{version}-py3-none-any.whl"
    sdist = dist / f"{name}-{version}.tar.gz"
    modules = {
        path.relative_to(root / "src").as_posix(): path.read_bytes()
        for path in (root / "src" / name).rglob("*.py")
    }
    if not modules:
        raise ValueError("No source modules found")
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate wheel member")
        packaged = {path for path in names if path.startswith(name + "/")}
        if packaged != set(modules):
            raise ValueError("Wheel modules differ from the source tree")
        for path, expected in modules.items():
            if archive.read(path) != expected:
                raise ValueError(f"Wheel source mismatch: {path}")
    required = {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in (root / "docs").rglob("*")
        if path.is_file() and path.suffix in {".md", ".svg", ".json"}
    }
    required.update({"src/" + path: data for path, data in modules.items()})
    for path in ("LICENSE", "README.md", "pyproject.toml", "version"):
        required[path] = (root / path).read_bytes()
    prefix = f"{name}-{version}/"
    packaged = {}
    with tarfile.open(sdist) as archive:
        for member in archive:
            if member.isdir():
                continue
            if not member.isfile() or not member.name.startswith(prefix):
                raise ValueError(f"Invalid source archive member: {member.name}")
            path = member.name[len(prefix):]
            if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
                raise ValueError(f"Unsafe source archive member: {member.name}")
            if path in packaged:
                raise ValueError(f"Duplicate source archive member: {path}")
            packaged[path] = archive.extractfile(member).read()
    for path, expected in required.items():
        if packaged.get(path) != expected:
            raise ValueError(f"Missing or changed source archive member: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path)
    args = parser.parse_args()
    check(Path(__file__).resolve().parents[1], args.dist)
    print("PASS: built wheel modules and source documentation match the source tree")
