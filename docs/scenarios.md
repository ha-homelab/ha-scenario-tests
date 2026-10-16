# Scenario contract v1

The authoritative validator is `src/ha_scenario_tests/schema.py`. JSON only, at most 64 KiB. Unknown keys, duplicate JSON keys, symlink input, non-finite numbers and invalid types are rejected. Do not copy household configuration into public examples.

Required root fields: `schema: "ha-scenario/v1"`, a short lowercase `name`, `seed`, `automations`, `timeline`, `expect`. Optional `settle_seconds` defaults to 0.1. All entity IDs use the `scenario_` prefix and must be declared in the seed. Supported domains: `light`, `switch`, `input_boolean`, `binary_sensor`. Supported states: `on`, `off`, `unknown`, `unavailable`.

An automation has `id`, `triggers`, `actions`, optional `conditions` and `mode` (`single` or `restart`). State triggers require `trigger`, `entity_id`, `to`; optionally `from` and `for_seconds`. Event triggers use `trigger: "event"` and `event_type: "scenario_name"`; `automation_reloaded` is also supported. Conditions are state comparisons only. Actions contain `action` and one `entity_id`: `turn_on`, `turn_off`, `toggle` on seeded light/switch/input_boolean entities. No templates, selectors, device actions, blueprints, scripts from disk or service data are admitted.

Timeline steps contain `after` (relative seconds since the prior completed step), and exactly one operation:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Other operations: `"event": "scenario_manual_off"`, or `"reload": true`. Reload calls HA's real automation service, which reads the generated temporary `configuration.yaml`; the test does not imitate reload by firing its completion event.

`expect.calls` is the exact ordered list of `{action, entity_id}` records, including repeats; an empty list forbids all actuator calls. `expect.forbidden` optionally lists calls that must never occur. `expect.states` maps seeded IDs to final states. Unexpected calls fail even if the final state happens to match.

Limits: 64 seed entities, 16 automations, 8 triggers and 8 conditions per automation, 16 actions per automation, 32 timeline steps, 5 seconds total requested waits, 256 captured calls. Background task errors and blocked I/O fail the run. The report includes monotonic elapsed call/step times, loaded components, final states and failure codes.

The supplied stale example represents transport loss by `unavailable`. It does not infer source freshness from `last_changed`, test sensor timestamp parsing or prove real sensor expiry behavior. The manual override is an explicit synthetic policy; the tool does not add that policy to an existing automation.
