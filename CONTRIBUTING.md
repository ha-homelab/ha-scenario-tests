# Contributing

Use a clean Python 3.14 environment and the hashed lock. Install source with `pip install --no-deps -e .`. Run `python -m ruff check .`, `python -m ruff format --check .`, `python -m pytest -q --junitxml=junit.xml` and `python scripts/render_diagrams.py --check`.

Changes to the admitted language need negative validation tests and a real-HA scenario proving the behavior. Do not silently broaden services, templates, network integrations or config loading. Keep all four message catalogues in parity and update English/Russian detailed docs plus all four READMEs when user behavior changes. Keep synthetic fixtures portable and clearly marked.

Regenerate dependencies with a reviewed resolver: `uv pip compile pyproject.toml --extra test --universal --generate-hashes -o requirements.lock`. HA upgrades require the full runtime suite; version equality is intentional. Do not copy a home configuration, token, MAC address, floorplan or occupancy history into an issue or PR.


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
