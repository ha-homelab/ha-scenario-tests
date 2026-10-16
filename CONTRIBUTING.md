# Contributing

Use a clean Python 3.14 environment and the hashed lock. Install source with `pip install --no-deps -e .`. Run `python -m ruff check .`, `python -m ruff format --check .`, `python -m pytest -q --junitxml=junit.xml` and `python scripts/render_diagrams.py --check`.

Changes to the admitted language need negative validation tests and a real-HA scenario proving the behavior. Do not silently broaden services, templates, network integrations or config loading. Keep all four message catalogues in parity and update English/Russian detailed docs plus all four READMEs when user behavior changes. Keep synthetic fixtures portable and clearly marked.

Regenerate dependencies with a reviewed resolver: `uv pip compile pyproject.toml --extra test --universal --generate-hashes -o requirements.lock`. HA upgrades require the full runtime suite; version equality is intentional. Do not copy a home configuration, token, MAC address, floorplan or occupancy history into an issue or PR.
