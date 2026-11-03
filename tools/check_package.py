"""Bound package expansion and verify its full source/metadata closure."""

import argparse
import base64
import configparser
import csv
import email.parser
import fnmatch
import gzip
import hashlib
import io
import os
import pathlib
import stat
import tarfile
import tomllib
import zipfile
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    path = pathlib.PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def tar_files(raw):
    result = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        for count, member in enumerate(archive, 1):
            require(count <= 1000, "Too many tar members")
            require(
                safe_name(member.name) and (member.isdir() or member.isfile()), "Unsafe tar member"
            )
            require(
                member.sparse is None
                and not any(k.startswith("GNU.sparse.") for k in member.pax_headers),
                "Sparse tar member",
            )
            require(0 <= member.size <= 8 * 1024**2, "Tar member size cap")
            total += member.size
            require(total <= 20 * 1024**2, "Tar logical byte cap")
            if member.isdir():
                continue
            require(
                member.name not in result and len(result) < 1000,
                "Duplicate or excessive tar members",
            )
            data = archive.extractfile(member).read(member.size + 1)
            require(len(data) == member.size, "Tar member length mismatch")
            result[member.name] = data
    return result


def ini(raw):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string(raw.decode())
    require(not parser.defaults(), "Unexpected INI defaults")
    return {s: dict(parser[s]) for s in parser.sections()}


def manifest_paths(source_files):
    required = {
        "pyproject.toml",
        "MANIFEST.in",
        "requirements-build.in",
        "requirements-build.lock",
    } | {n for n in source_files if n.startswith("src/") and n.endswith(".py")}
    for line in source_files["MANIFEST.in"].decode().splitlines():
        parts = line.split()
        if not parts or parts[0].startswith("#"):
            continue
        require(parts[0] in ("include", "recursive-include"), "Unsupported MANIFEST directive")
        require(
            len(parts) >= 2 and all(safe_name(part) for part in parts[1:]),
            "Unsafe manifest pattern",
        )
        if parts[0] == "include":
            for pattern in parts[1:]:
                matches = {
                    n for n in source_files if "/" not in n and fnmatch.fnmatchcase(n, pattern)
                }
                require(matches, "Unmatched MANIFEST include")
                required |= matches
        else:
            require(len(parts) >= 3, "Invalid recursive include")
            root = parts[1] + "/"
            required |= {
                n
                for n in source_files
                if n.startswith(root)
                and any(fnmatch.fnmatchcase(n.rsplit("/", 1)[-1], pattern) for pattern in parts[2:])
            }
    return required


def verify_packages(files, source_files, version):
    project = tomllib.loads(source_files["pyproject.toml"].decode())["project"]
    name = project["name"].replace("-", "_")
    wheel_name, sdist_name = f"{name}-{version}-py3-none-any.whl", f"{name}-{version}.tar.gz"
    require(set(files) == {wheel_name, sdist_name}, "Unexpected package asset set")
    require(all(0 < len(data) <= 10 * 1024**2 for data in files.values()), "Compressed package cap")
    with gzip.GzipFile(fileobj=io.BytesIO(files[sdist_name])) as compressed:
        expanded = compressed.read(20 * 1024**2 + 1)
    require(len(expanded) <= 20 * 1024**2, "Expanded sdist cap")
    packaged = tar_files(expanded)
    prefix = f"{name}-{version}/"
    require(all(n.startswith(prefix) for n in packaged), "Wrong sdist prefix")
    packaged = {n[len(prefix) :]: b for n, b in packaged.items()}
    generated = {"PKG-INFO", "setup.cfg"} | {
        f"src/{name}.egg-info/{n}"
        for n in (
            "PKG-INFO",
            "SOURCES.txt",
            "dependency_links.txt",
            "entry_points.txt",
            "requires.txt",
            "top_level.txt",
        )
    }
    require(set(packaged) - set(source_files) <= generated, "Untracked sdist payload")
    for n, b in packaged.items():
        if n in source_files:
            require(b == source_files[n], "Source archive differs from exact Git source: " + n)
    required = manifest_paths(source_files)
    require(set(packaged) == required | generated, "Source package/manifest inventory mismatch")
    require(packaged["version"].decode().strip() == version, "Version marker mismatch")
    with zipfile.ZipFile(io.BytesIO(files[wheel_name])) as archive:
        names = archive.namelist()
        require(
            len(names) == len(set(names)) <= 100 and all(safe_name(n) for n in names),
            "Unsafe wheel inventory",
        )
        require(sum(i.file_size for i in archive.infolist()) <= 8 * 1024**2, "Expanded wheel cap")
        wheel = {}
        for info in archive.infolist():
            kind = stat.S_IFMT(info.external_attr >> 16)
            require(
                kind in (0, stat.S_IFREG) and not info.is_dir() and not info.flag_bits & 1,
                "Special/encrypted wheel member",
            )
            require(0 <= info.file_size <= 8 * 1024**2, "Wheel member cap")
            with archive.open(info) as member:
                data = member.read(info.file_size + 1)
            require(len(data) == info.file_size, "Wheel member size mismatch")
            wheel[info.filename] = data
    modules = {
        n[4:]: b
        for n, b in source_files.items()
        if n.startswith(f"src/{name}/") and n.endswith(".py")
    }
    dist = f"{name}-{version}.dist-info/"
    required_metadata = {
        dist + n
        for n in (
            "METADATA",
            "WHEEL",
            "entry_points.txt",
            "top_level.txt",
            "RECORD",
            "licenses/LICENSE",
        )
    }
    require(set(wheel) == set(modules) | required_metadata, "Wheel complete inventory mismatch")
    require(all(wheel[n] == b for n, b in modules.items()), "Wheel source mismatch")
    metadata = email.parser.BytesParser().parsebytes(wheel[dist + "METADATA"])
    project = tomllib.loads(source_files["pyproject.toml"].decode())["project"]
    for field, expected in (("Name", project["name"]), ("Version", version)):
        require(metadata.get_all(field, []) == [expected], "Package identity metadata mismatch")
    require(project["version"] == version, "Source version mismatch")
    python = metadata.get_all("Requires-Python", [])
    require(
        len(python) == 1
        and set(python[0].replace(" ", "").split(","))
        == set(project["requires-python"].replace(" ", "").split(",")),
        "Python support mismatch",
    )
    extras = project.get("optional-dependencies", {})
    expected_dependencies = list(project.get("dependencies", []))
    for extra, requirements in extras.items():
        expected_dependencies.extend(
            f'{requirement}; extra == "{extra}"' for requirement in requirements
        )

    def normalize(text):
        return "".join(text.split()).replace("'", '"')

    require(
        sorted(map(normalize, metadata.get_all("Requires-Dist", [])))
        == sorted(map(normalize, expected_dependencies)),
        "Dependency metadata mismatch",
    )
    require(
        sorted(metadata.get_all("Provides-Extra", [])) == sorted(extras), "Extra metadata mismatch"
    )
    require(
        packaged["PKG-INFO"]
        == packaged[f"src/{name}.egg-info/PKG-INFO"]
        == wheel[dist + "METADATA"],
        "Package metadata differs across archives",
    )
    expected_entry_points = dict(project.get("entry-points", {}))
    expected_entry_points["console_scripts"] = project.get("scripts", {})
    require(ini(wheel[dist + "entry_points.txt"]) == expected_entry_points, "Entry point mismatch")
    require(
        packaged[f"src/{name}.egg-info/entry_points.txt"] == wheel[dist + "entry_points.txt"],
        "sdist entry point mismatch",
    )
    require(
        wheel[dist + "top_level.txt"]
        == packaged[f"src/{name}.egg-info/top_level.txt"]
        == (name + "\n").encode(),
        "Top-level package mismatch",
    )
    require(wheel[dist + "licenses/LICENSE"] == source_files["LICENSE"], "Wheel license mismatch")
    require(
        ini(packaged["setup.cfg"]) == {"egg_info": {"tag_build": "", "tag_date": "0"}},
        "Generated setup configuration mismatch",
    )
    require(
        packaged[f"src/{name}.egg-info/dependency_links.txt"].strip() == b"",
        "Dependency link injection",
    )
    requires = "\n".join(project.get("dependencies", [])) + "\n"
    for extra, requirements in extras.items():
        requires += "\n[" + extra + "]\n" + "\n".join(requirements) + "\n"
    require(
        packaged[f"src/{name}.egg-info/requires.txt"] == requires.encode(),
        "sdist dependency metadata mismatch",
    )
    wheel_metadata = email.parser.BytesParser().parsebytes(wheel[dist + "WHEEL"])
    for field, expected in (
        ("Wheel-Version", "1.0"),
        ("Root-Is-Purelib", "true"),
        ("Tag", "py3-none-any"),
    ):
        require(wheel_metadata.get_all(field, []) == [expected], "Wheel format metadata mismatch")
    sources = packaged[f"src/{name}.egg-info/SOURCES.txt"].decode().splitlines()
    require(
        len(sources) == len(set(sources))
        and set(sources) == set(packaged) - {"PKG-INFO", "setup.cfg"},
        "Generated source manifest mismatch",
    )
    record = list(csv.reader(io.StringIO(wheel[dist + "RECORD"].decode())))
    require(
        len(record) == len(wheel) and {r[0] for r in record} == set(wheel), "Wheel RECORD coverage"
    )
    for n, digest, size in record:
        if n == dist + "RECORD":
            require(not digest and not size, "Unexpected RECORD self hash")
        else:
            expected = "sha256=" + base64.urlsafe_b64encode(
                hashlib.sha256(wheel[n]).digest()
            ).decode().rstrip("=")
            require(digest == expected and size == str(len(wheel[n])), "Wheel RECORD mismatch")
    return {
        "source_members": len(packaged),
        "wheel_members": len(wheel),
        "source_modules": len(modules),
    }


def read_file(path, limit):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), "Nonregular input file")
        data = stream.read(limit + 1)
    require(len(data) <= limit, "Input byte cap")
    return data


def check(root: Path, dist: Path) -> None:
    project_bytes = read_file(root / "pyproject.toml", 1024**2)
    project = tomllib.loads(project_bytes.decode("utf-8"))["project"]
    name, version = project["name"].replace("-", "_"), project["version"]
    require(
        name.replace("_", "").isalnum() and "/" not in version and "\\" not in version,
        "Invalid package identity",
    )
    manifest = read_file(root / "MANIFEST.in", 1024**2)
    paths = {"pyproject.toml", "MANIFEST.in", "requirements-build.in", "requirements-build.lock"}
    paths.update(str(path.relative_to(root)) for path in (root / "src" / name).rglob("*.py"))
    for line in manifest.decode().splitlines():
        parts = line.split()
        if not parts or parts[0].startswith("#"):
            continue
        require(parts[0] in ("include", "recursive-include"), "Unsupported MANIFEST directive")
        require(all(safe_name(part) for part in parts[1:]), "Unsafe manifest pattern")
        if parts[0] == "include":
            for pattern in parts[1:]:
                paths.update(
                    str(path.relative_to(root)) for path in root.glob(pattern) if path.is_file()
                )
        else:
            require(len(parts) >= 3, "Invalid recursive include")
            for pattern in parts[2:]:
                paths.update(
                    str(path.relative_to(root))
                    for path in (root / parts[1]).rglob(pattern)
                    if path.is_file()
                )
    require(len(paths) <= 1000, "Source file count cap")
    source = {}
    total = 0
    for relative in sorted(paths):
        path = root / relative
        require(
            not path.is_symlink() and path.is_file(),
            "Missing or symlinked source input: " + relative,
        )
        source[relative] = read_file(path, 8 * 1024**2)
        total += len(source[relative])
        require(total <= 20 * 1024**2, "Source byte cap")
    files = {
        filename: read_file(dist / filename, 10 * 1024**2)
        for filename in (f"{name}-{version}-py3-none-any.whl", f"{name}-{version}.tar.gz")
    }
    verify_packages(files, source, version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path)
    args = parser.parse_args()
    check(Path(__file__).resolve().parents[1], args.dist)
    print("PASS: bounded package content and metadata match the complete source manifest")
