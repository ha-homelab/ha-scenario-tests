# Validation record

## 2026-10-15 Linux runtime validation

[GitHub Actions run 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) passed at commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, using CPython 3.14.8 on Ubuntu and pinned Home Assistant 2026.10.0. The full command `python3 -m pytest -q` completed with **54 passed in 21.42s**, with no skipped tests. This includes all seven actual-HA runtime tests: four example scenarios, an intentionally failing expectation/forbidden-action case, the localized CLI JSON report, and the downstream role-transfer contract. Each runtime test starts a fresh controlled worker; expected-failure assertions are tested as failures, not reported as successful scenarios.

Ruff, documentation links/SVG checks, source and wheel builds, the source publication policy and full-history secret scan also passed in that run. This validates synthetic service dispatch and state behavior under the documented Python I/O guard. It does not establish an OS security sandbox, validate a Docker execution, or prove physical device behavior.

## 2026-10-15 macOS development checks

The source, strict input admission, Python audit guard, CLI translations and SVG regeneration were checked locally with Python 3.14.7 on macOS arm64. `python -m pytest -q -m 'not runtime'` passed **47 tests**; seven real-HA cases are explicitly excluded by that command. `python -m ruff check src tests scripts` passed. This is not a substitute for the full runtime suite.

The actual Home Assistant 2026.10.0 engine loaded `automation`, `blueprint` and `trace` and executed the presence timeout and manual override scenarios with expected synthetic service calls, final states and no blocked I/O. The local Python process then exited with a native segmentation fault during interpreter teardown. The parent runner correctly treats that nonzero exit as a runtime failure, even when a successful JSON payload preceded it. **A complete passing macOS runtime test is not claimed.**

The full Linux CI suite is required before a release is accepted. Run `python -m pytest -q --junitxml=junit.xml`; missing HA, wrong HA versions, child timeouts and nonzero child exits fail, never silently skip. The linked run above is the Linux evidence for this implementation; later changes require their own passing run. No Docker run or physical device validation is claimed in this record.

## Controlled bootstrap metadata

The worker supplies the synthetic value `synthetic` for Python's cached processor metadata and disables `socket.has_ipv6` before importing HA. This prevents HA's platform initialization from spawning `uname -p`, and prevents urllib3's import-time localhost IPv6 bind probe. On Linux, ifaddr is imported under the guard using `ctypes.CDLL(None)`, resolving libc symbols already loaded in the process; this avoids the library-finder's `ldconfig` subprocess. The ordinary library finder is immediately restored. The I/O guard has no allow-list exception for these operations. These changes affect host metadata/probing only; HA triggers, conditions, timers, reload, scripts and service dispatch are real. They are version-sensitive and covered by the pinned runtime suite.

## Reproduce

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

No report proves real relay state, radio delivery, household presence accuracy or production-duration timing. The SVG timeline shows synthetic expectations, not benchmark measurements.

The runtime suite also includes `tests/fixtures/role_transfer.json`, the synthetic downstream contract: the current role turns off and the retired plug remains on. This is not a physical load transfer test.
