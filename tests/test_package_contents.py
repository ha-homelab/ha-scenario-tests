"""Reject concrete archive omissions, injected wheel code, and metadata drift."""

import base64
import csv
import gzip
import hashlib
import io
import tarfile
import zipfile

import pytest

from tools.check_package import check, tar_files


@pytest.fixture
def package(tmp_path):
    root, dist = tmp_path / "source", tmp_path / "dist"
    dist.mkdir()
    files = {
        "pyproject.toml": (
            '[project]\nname = "sample"\nversion = "1.0.0"\n'
            'requires-python = ">=3.14.2,<3.15"\n'
            'dependencies = ["homeassistant==2026.11.0b3"]\n'
            '[project.optional-dependencies]\ntest = ["pytest==9.2.0"]\n'
            '[project.scripts]\nsample = "sample:main"\n'
        ),
        "MANIFEST.in": (
            "include README.md LICENSE version requirements.lock "
            "requirements-build.in requirements-build.lock\n"
            "recursive-include docs *.md *.json\n"
        ),
        "version": "1.0.0\n",
        "README.md": "Example\n",
        "LICENSE": "Example license\n",
        "requirements.lock": "homeassistant==2026.11.0b3\n",
        "requirements-build.in": "setuptools==84.2.1\n",
        "requirements-build.lock": "setuptools==84.2.1\n",
        "src/sample/__init__.py": 'VALUE = "original"\n',
        "docs/languages.json": '[{"code":"en"}]\n',
        "docs/translations.json": '{"version":1}\n',
        "docs/guide.md": "Guide\n",
    }
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    metadata = (
        b"Metadata-Version: 2.4\nName: sample\nVersion: 1.0.0\n"
        b"Requires-Python: >=3.14.2,<3.15\n"
        b"Requires-Dist: homeassistant==2026.11.0b3\nProvides-Extra: test\n"
        b'Requires-Dist: pytest==9.2.0; extra == "test"\n\nExample\n'
    )
    entries = b"[console_scripts]\nsample = sample:main\n"
    prefix = "sample-1.0.0.dist-info/"

    def build(
        *,
        omit=None,
        changed_module=False,
        duplicate=False,
        wheel_change=None,
        extra_wheel=None,
        sparse=False,
        special=False,
    ):
        wheel = {
            "sample/__init__.py": (
                b"changed" if changed_module else files["src/sample/__init__.py"].encode()
            ),
            prefix + "METADATA": metadata,
            prefix + "WHEEL": b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
            prefix + "entry_points.txt": entries,
            prefix + "top_level.txt": b"sample\n",
            prefix + "licenses/LICENSE": files["LICENSE"].encode(),
        }
        if wheel_change:
            name, transform = wheel_change
            wheel[prefix + name] = transform(wheel[prefix + name])
        if extra_wheel:
            wheel[extra_wheel] = b"harmless adversarial fixture\n"
        record = io.StringIO()
        writer = csv.writer(record, lineterminator="\n")
        for name, data in wheel.items():
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
            writer.writerow([name, "sha256=" + digest, str(len(data))])
        writer.writerow([prefix + "RECORD", "", ""])
        wheel[prefix + "RECORD"] = record.getvalue().encode()
        with zipfile.ZipFile(dist / "sample-1.0.0-py3-none-any.whl", "w") as archive:
            for name, data in wheel.items():
                if special and name == "sample/__init__.py":
                    info = zipfile.ZipInfo(name)
                    info.create_system = 3
                    info.external_attr = 0o120777 << 16
                    archive.writestr(info, data)
                else:
                    archive.writestr(name, data)
        sources = {name: text.encode() for name, text in files.items()}
        egg = "src/sample.egg-info/"
        sources.update(
            {
                "PKG-INFO": metadata,
                "setup.cfg": b"[egg_info]\ntag_build =\ntag_date = 0\n",
                egg + "PKG-INFO": metadata,
                egg + "entry_points.txt": entries,
                egg + "top_level.txt": b"sample\n",
                egg + "dependency_links.txt": b"\n",
                egg + "requires.txt": b"homeassistant==2026.11.0b3\n\n[test]\npytest==9.2.0\n",
                egg + "SOURCES.txt": b"",
            }
        )
        sources[egg + "SOURCES.txt"] = (
            "\n".join(sorted(set(sources) - {"PKG-INFO", "setup.cfg"})) + "\n"
        ).encode()
        with tarfile.open(
            dist / "sample-1.0.0.tar.gz", "w:gz", format=tarfile.PAX_FORMAT
        ) as archive:
            for name, data in sources.items():
                if name == omit:
                    continue
                info = tarfile.TarInfo("sample-1.0.0/" + name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
                if duplicate and name == "docs/languages.json":
                    archive.addfile(info, io.BytesIO(data))
            if sparse:
                info = tarfile.TarInfo("sample-1.0.0/extra-sparse")
                info.size = 1
                info.pax_headers = {"GNU.sparse.map": "0,1", "GNU.sparse.size": "1048576"}
                archive.addfile(info, io.BytesIO(b"x"))

    return root, dist, build


def test_accepts_complete_matching_packages(package):
    root, dist, build = package
    build()
    check(root, dist)


@pytest.mark.parametrize(
    "path",
    [
        "docs/languages.json",
        "docs/translations.json",
        "requirements-build.in",
        "requirements-build.lock",
        "requirements.lock",
        "README.md",
    ],
)
def test_rejects_omitted_manifest_inputs(package, path):
    root, dist, build = package
    build(omit=path)
    with pytest.raises(ValueError):
        check(root, dist)


def test_rejects_changed_wheel_source(package):
    root, dist, build = package
    build(changed_module=True)
    with pytest.raises(ValueError, match="Wheel source mismatch"):
        check(root, dist)


def test_rejects_duplicate_source_member(package):
    root, dist, build = package
    build(duplicate=True)
    with pytest.raises(ValueError, match="Duplicate"):
        check(root, dist)


@pytest.mark.parametrize("path", ["review_probe.pth", "other_package/__init__.py"])
def test_rejects_unexpected_wheel_code_with_valid_record(package, path):
    root, dist, build = package
    build(extra_wheel=path)
    with pytest.raises(ValueError, match="complete inventory"):
        check(root, dist)


@pytest.mark.parametrize(
    "field,old,new",
    [
        ("METADATA", b"Name: sample", b"Name: other"),
        ("METADATA", b"Requires-Python: >=3.14.2,<3.15", b"Requires-Python: >=3.9"),
        ("METADATA", b"\n\nExample", b"\nRequires-Dist: review-probe==0\n\nExample"),
        ("entry_points.txt", b"sample:main", b"sample:other"),
        ("top_level.txt", b"sample", b"other"),
        ("licenses/LICENSE", b"Example license", b"Other license"),
        ("WHEEL", b"py3-none-any", b"cp314-none-linux_x86_64"),
    ],
)
def test_rejects_metadata_drift_with_valid_record(package, field, old, new):
    root, dist, build = package
    build(wheel_change=(field, lambda data: data.replace(old, new)))
    with pytest.raises(ValueError):
        check(root, dist)


def test_rejects_sparse_tar_without_expanding_logical_payload(package):
    root, dist, build = package
    build(sparse=True)
    with pytest.raises(ValueError, match="Sparse"):
        check(root, dist)


def test_rejects_symlink_wheel_member(package):
    root, dist, build = package
    build(special=True)
    with pytest.raises(ValueError, match="Special"):
        check(root, dist)


def test_rejects_oversized_tar_header_before_reading_payload():
    info = tarfile.TarInfo("large")
    info.size = 9 * 1024**2
    raw = info.tobuf() + b"\0" * 1024
    with pytest.raises(ValueError, match="member size cap"):
        tar_files(raw)


def test_rejects_gzip_expansion_over_total_cap(package):
    root, dist, build = package
    build()
    (dist / "sample-1.0.0.tar.gz").write_bytes(gzip.compress(b"\0" * (20 * 1024**2 + 1)))
    with pytest.raises(ValueError, match="Expanded sdist cap"):
        check(root, dist)


def test_rejects_traversal_before_payload_read():
    info = tarfile.TarInfo("../outside")
    with pytest.raises(ValueError, match="Unsafe"):
        tar_files(info.tobuf() + b"\0" * 1024)


@pytest.mark.parametrize("kind", [tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.CHRTYPE])
def test_rejects_special_tar_members(kind):
    info = tarfile.TarInfo("special")
    info.type = kind
    info.linkname = "elsewhere"
    with pytest.raises(ValueError, match="Unsafe"):
        tar_files(info.tobuf() + b"\0" * 1024)


def test_rejects_cumulative_tar_size_before_third_payload():
    raw = io.BytesIO()
    for number in range(3):
        info = tarfile.TarInfo(f"file-{number}")
        info.size = 8 * 1024**2
        raw.write(info.tobuf())
        if number < 2:
            raw.write(b"\0" * info.size)
    with pytest.raises(ValueError, match="logical byte cap"):
        tar_files(raw.getvalue())


def test_rejects_excessive_empty_directories():
    raw = io.BytesIO()
    for number in range(1001):
        info = tarfile.TarInfo(f"directory-{number}")
        info.type = tarfile.DIRTYPE
        raw.write(info.tobuf())
    raw.write(b"\0" * 1024)
    with pytest.raises(ValueError, match="Too many tar members"):
        tar_files(raw.getvalue())
