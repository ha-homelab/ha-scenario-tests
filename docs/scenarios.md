# Scenario contract v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="scenarios.md" lang="en" dir="ltr">English</a> ·
<a href="scenarios.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="scenarios.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="scenarios.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="scenarios.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="scenarios.es.md" lang="es" dir="ltr">Español</a> ·
<a href="scenarios.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="scenarios.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="scenarios.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="scenarios.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="scenarios.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="scenarios.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="scenarios.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="scenarios.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="scenarios.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="scenarios.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="scenarios.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="scenarios.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="scenarios.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="scenarios.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="scenarios.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="scenarios.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="scenarios.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="scenarios.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

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

The parent validates the complete worker report before returning it. `passed` must be an actual Boolean, `physical_validation` must be false, and schema, HA version, scenario name, fields and bounds must match the protocol. The parent also checks call/state assertions against the scenario rather than trusting a success flag. Invalid output and any nonzero worker exit are runtime errors, even if the child printed a success-looking JSON object.

The supplied stale example represents transport loss by `unavailable`. It does not infer source freshness from `last_changed`, test sensor timestamp parsing or prove real sensor expiry behavior. The manual override is an explicit synthetic policy; the tool does not add that policy to an existing automation.
