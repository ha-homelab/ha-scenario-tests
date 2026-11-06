# Contributing

Use a clean Python 3.14 environment and the hashed lock. Install source with `pip install --no-deps -e .`. Run `python -m ruff check .`, `python -m ruff format --check .`, `python -m pytest -q --junitxml=junit.xml` and `python scripts/render_diagrams.py --check`.

Changes to the admitted language need negative validation tests and a real-HA scenario proving the behavior. Do not silently broaden services, templates, network integrations or config loading. Keep all four message catalogues in parity and update all 24 editions of the detailed guides plus all four READMEs when user behavior changes; follow [translation maintenance](docs/translations.md). Keep synthetic fixtures portable and clearly marked.

Regenerate dependencies with a reviewed resolver: `uv pip compile pyproject.toml --extra test --python-version 3.14.7 --universal --generate-hashes --no-python-downloads -o requirements.lock`. HA upgrades require the full runtime suite; version equality is intentional. Do not copy a home configuration, token, MAC address, floorplan or occupancy history into an issue or PR.


## Feedback and review

Use [GitHub Issues](https://github.com/ha-homelab/ha-scenario-tests/issues) for bug reports,
questions and enhancement proposals; existing issues and pull requests retain
searchable discussion. Include the source revision, expected/actual behavior and
a minimal synthetic reproducer. English reports are welcome. Security reports
follow [SECURITY.md](SECURITY.md), and all participation follows our
[Code of Conduct](CODE_OF_CONDUCT.md).

Contributions are under the repository's MIT license. Submit only material you
have the right to contribute. Follow Python PEP 8 and the repository's Ruff
configuration. Every new major feature and behavior fix requires automated tests,
including a negative or regression case; update the interface documentation and
changelog in the same pull request. Run tests without Python optimization so
assertions remain enabled. The maintainer reviews the diff, test evidence and
open comments before a normal merge. Automated reviews assist this process.

See [RELEASING.md](RELEASING.md) for build and source-version instructions,
[GOVERNANCE.md](GOVERNANCE.md) for responsibilities, and
[ROADMAP.md](ROADMAP.md) for planned work.


## Locked package builds

`requirements-build.in` declares the package frontend and backend used by CI
and the synthetic runtime container. Regenerate its complete artifact hash lock
against the existing runtime constraints with uv 0.13.4:

```sh
uv pip compile .github/requirements-wheels-only.in requirements-build.in --constraint=requirements.lock --python-version=3.14.2 --universal --generate-hashes --output-file=requirements-build.lock
```

Install both lockfiles with `--require-hashes` before building. Local source
installation uses `--no-index --no-deps --no-build-isolation`, and distribution builds use
`--no-isolation`, so package building cannot silently fetch an unverified backend.
`tools/check_lock.py` rejects a build lock that differs from `pyproject.toml`.
The separate wheel-acceptance environment still installs only the runtime lock
and the newly built wheel.

Renovate regenerates the build-tool lock with its existing runtime constraint. The `setuptools` backend stays on the manual runtime update path because it must equal `pyproject.toml` exactly; independent build frontend updates remain automated.

## Security fixes for manually maintained locks

For a direct or transitive advisory in the manually maintained environment,
identify the affected package and the advisory's fixed version range. A plain
lock regeneration may retain the existing transitive pin. Replace
`AFFECTED_PACKAGE` below with the advisory's package name and request its update
explicitly in the existing reviewed build environment:

```sh
uv pip compile pyproject.toml --extra test --python-version 3.14.7 --universal --generate-hashes --no-python-downloads -o requirements.lock --upgrade-package AFFECTED_PACKAGE
```

Review any direct or parent constraint that prevents selection of a fixed
release; qualify that constraint change together with the lock. Preserve the
documented interpreter, platform, hash and build-isolation requirements.
Check the resulting affected-package versions against the advisory's affected
and fixed ranges in every applicable Python/platform marker branch and every
coupled lock or export. A successful resolver exit alone is not proof of a fix.
If no compatible fixed resolution exists, keep the advisory open and document
the blocker instead of marking it remediated.

Keep the fixed Python version and `--no-python-downloads` requirement. Regenerate `requirements-build.lock` afterward with the documented runtime constraint. If the backend changes, update the exact `setuptools` pins in `pyproject.toml` and `requirements-build.in` together and run `tools/check_lock.py` plus the full real-HA runtime suite.

Run the repository's complete existing dependency, runtime and CI qualification
before merging the source constraints and generated files together. GitHub
vulnerability alerts remain enabled for these manually maintained units.
