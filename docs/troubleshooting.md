# Troubleshooting

- Exit 2 during installation/run: check Python 3.14.2–3.14.x, the exact HA pin and a clean virtual environment. The runner rejects other HA versions. Reinstall the lock before reporting a failure.
- Worker failure/timeout: a dependency import or HA setup failed. Run the isolated worker directly with a **synthetic** file to obtain a local traceback: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Do not publish unreviewed environment diagnostics.
- `calls_mismatch`: compare order and duplicate calls, not just final state. Seeded states are set before startup; they do not automatically count as a new state trigger after startup.
- `forbidden_call`: a captured synthetic actuator command matched the negative contract. This is a real automation dispatch, not physical actuation.
- `states_mismatch`: a timeline assignment or synthetic actuator left a different state.
- `blocked_io` or `background_exception`: never turn off the guard to get a green result. This release admits no network integrations. Report the synthetic reproduction and version.
- Timer flakes: increase separation between a state transition and the asserted deadline. Actual event-loop scheduling is measured; no virtual clock or exact microsecond scheduling is promised.
- Reload: `for` timers may be cancelled by the real reload. An explicit reconciliation automation is needed when the policy requires recovery; compare `reload_reconcile.json`.
- Existing report: `--report` deliberately refuses to overwrite it. Select a new path.

If using the source tree after a non-editable install, reinstall the package before testing changes. For development install with `--no-deps -e .`.
