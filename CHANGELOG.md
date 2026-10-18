# Changelog

## Unreleased

- Synchronize Ruff 0.17.1 with the hash-locked validation dependencies; keep the Home Assistant runtime and other dependency versions unchanged.
- Update CI to pytest 9.0.3 (GHSA-6w46-j5rx-g56g) and the build backend to setuptools 83.0.0 (upstream fix for GHSA-h35f-9h28-mq5c).
- Document private reporting, review/release responsibilities, contribution rules and the current continuity limitation; include these policies in source distributions.

## 0.1.0

- Initial bounded JSON scenario contract with seed, elapsed timeline, exact and forbidden action assertions, and final states.
- Real Home Assistant 2026.10.0 automation execution in a fresh guarded worker and temporary configuration.
- Presence, manual override, unavailable sensor and actual reload examples.
- pytest fixture, stable JSON reports, four-language CLI/READMEs and English/Russian detailed docs/wiki.
- Reproducible synthetic SVG diagrams and optional network-disabled container recipe.
