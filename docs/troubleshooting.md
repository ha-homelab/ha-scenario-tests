# Troubleshooting

<!-- language-navigation:start -->
<p dir="ltr">
<a href="troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="troubleshooting.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="troubleshooting.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="troubleshooting.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="troubleshooting.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="troubleshooting.es.md" lang="es" dir="ltr">Español</a> ·
<a href="troubleshooting.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="troubleshooting.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="troubleshooting.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="troubleshooting.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="troubleshooting.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="troubleshooting.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="troubleshooting.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="troubleshooting.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="troubleshooting.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="troubleshooting.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="troubleshooting.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="troubleshooting.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="troubleshooting.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="troubleshooting.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="troubleshooting.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="troubleshooting.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="troubleshooting.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="troubleshooting.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

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
