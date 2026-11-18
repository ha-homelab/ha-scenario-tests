# Documentation

Guides for running bounded, synthetic household scenarios in a real Home Assistant
automation and script engine, with no Home Assistant URL, token, device connection or
production configuration.

## English guides

- [Installation and containment](install.md) — pinned Python and Home Assistant runtime, validate and run commands, and the container and worker isolation recipe.
- [Scenario contract v1](scenarios.md) — the JSON scenario format: seed entities, automations, timeline steps, expected and forbidden calls.
- [Troubleshooting](troubleshooting.md) — failure codes, worker timeouts, timer flakiness and the report-overwrite refusal.
- [Scope and evidence](limits.md) — what the synthetic engine can establish, what stays unproven, and the trusted-host boundary.
- [Validation record](validation.md) — the dated Linux CI run and the macOS development checks, including the native teardown failure.

## Translations and maintenance

- [Translated guides](translations/README.md) — the five guides in each of the other 23 documentation languages.
- [Maintaining guide translations](translations.md) — how the language catalog, source digests and translation reviews are kept in step.
