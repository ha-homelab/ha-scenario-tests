"""Exercise actual archive omissions and byte changes without rebuilding dependencies."""

import io
import tarfile
import zipfile

import pytest

from tools.check_package import check


@pytest.fixture
def package(tmp_path):
    root = tmp_path / "source"
    dist = tmp_path / "dist"
    dist.mkdir()
    files = {
        "pyproject.toml": '[project]\nname = "sample"\nversion = "1.0.0"\n',
        "version": "1.0.0\n",
        "README.md": "Example\n",
        "LICENSE": "Example license\n",
        "src/sample/__init__.py": 'VALUE = "original"\n',
        "docs/languages.json": '[{"code":"en"}]\n',
        "docs/translations.json": '{"version":1}\n',
        "docs/guide.md": "Guide\n",
    }
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def build(*, omit=None, changed_module=False, duplicate=False):
        with zipfile.ZipFile(dist / "sample-1.0.0-py3-none-any.whl", "w") as archive:
            text = "changed" if changed_module else files["src/sample/__init__.py"]
            archive.writestr("sample/__init__.py", text)
        with tarfile.open(dist / "sample-1.0.0.tar.gz", "w:gz") as archive:
            for name, text in files.items():
                if name == omit:
                    continue
                data = text.encode()
                info = tarfile.TarInfo("sample-1.0.0/" + name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
                if duplicate and name == "docs/languages.json":
                    archive.addfile(info, io.BytesIO(data))

    return root, dist, build


def test_accepts_complete_matching_packages(package):
    root, dist, build = package
    build()
    check(root, dist)


@pytest.mark.parametrize("path", ["docs/languages.json", "docs/translations.json"])
def test_rejects_omitted_documentation_metadata(package, path):
    root, dist, build = package
    build(omit=path)
    with pytest.raises(ValueError, match="Missing or changed source archive member"):
        check(root, dist)


def test_rejects_changed_wheel_source(package):
    root, dist, build = package
    build(changed_module=True)
    with pytest.raises(ValueError, match="Wheel source mismatch"):
        check(root, dist)


def test_rejects_duplicate_source_member(package):
    root, dist, build = package
    build(duplicate=True)
    with pytest.raises(ValueError, match="Duplicate source archive member"):
        check(root, dist)
