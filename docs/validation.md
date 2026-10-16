# Validation record

## 2026-10-15 development checks

The source, strict input admission, Python audit guard, CLI translations and SVG regeneration were checked locally with Python 3.14.7 on macOS arm64. `python -m pytest -q -m 'not runtime'` passed **47 tests**; seven real-HA cases are explicitly excluded by that command. `python -m ruff check src tests scripts` passed. This is not a substitute for the full runtime suite.

The actual Home Assistant 2026.10.0 engine loaded `automation`, `blueprint` and `trace` and executed the presence timeout and manual override scenarios with expected synthetic service calls, final states and no blocked I/O. The local Python process then exited with a native segmentation fault during interpreter teardown. The parent runner correctly treats that nonzero exit as a runtime failure, even when a successful JSON payload preceded it. **A complete passing macOS runtime test is not claimed.**

The full Linux CI suite is required before a release is accepted. Run `python -m pytest -q --junitxml=junit.xml`; missing HA, wrong HA versions, child timeouts and nonzero child exits fail, never silently skip. Check the repository's CI result for current Linux evidence. No Docker run or physical device validation is claimed in this record.

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
