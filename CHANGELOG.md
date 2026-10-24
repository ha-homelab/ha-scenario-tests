# Changelog

## Unreleased

No pending changes.

## 0.1.1rc1 — 2026-10-24

- Package the complete 24-language guides and checked-in wiki sources.
- Preserve executable examples and source digests in documentation parity checks; read multilingual files explicitly as UTF-8.
- Retain the beta runtime behavior, dependency pins and offline/synthetic acceptance boundaries.

## 0.1.1b1 — 2026-10-20

- First GitHub beta: source archive, wheel and SHA-256 checksums; no PyPI publication.
- Keep package metadata, source version and root version aligned. This prerelease retains the existing report/schema contracts.

- Pin Home Assistant 2026.10.1 with the reviewed hash-locked dependency set; verify the packaged runtime with a network-disabled Docker smoke test.
- Synchronize Ruff 0.17.1 with the hash-locked validation dependencies; keep the Home Assistant runtime and other dependency versions unchanged.
- Retain pytest 9.1.1 and setuptools 84.0.0 from the reviewed dependency updates.
- Document private reporting, review/release responsibilities, contribution rules and the current continuity limitation; include these policies in source distributions.

## 0.1.0

- Initial bounded JSON scenario contract with seed, elapsed timeline, exact and forbidden action assertions, and final states.
- Real Home Assistant 2026.10.0 automation execution in a fresh guarded worker and temporary configuration.
- Presence, manual override, unavailable sensor and actual reload examples.
- pytest fixture, stable JSON reports, four-language CLI/READMEs and English/Russian detailed docs/wiki.
- Reproducible synthetic SVG diagrams and optional network-disabled container recipe.
