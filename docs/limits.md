# Scope and evidence

<!-- language-navigation:start -->
<p dir="ltr">
<a href="limits.md" lang="en" dir="ltr">English</a> ·
<a href="limits.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="limits.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="limits.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="limits.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="limits.es.md" lang="es" dir="ltr">Español</a> ·
<a href="limits.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="limits.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="limits.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="limits.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="limits.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="limits.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="limits.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="limits.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="limits.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="limits.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="limits.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="limits.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="limits.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="limits.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="limits.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="limits.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="limits.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="limits.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

This release validates a bounded subset with actual Home Assistant triggers, conditions, timers, reload and script action dispatch. The actuator sinks and input states are synthetic. It does not prove wire protocols, current draw, sensor accuracy, a relay's physical state, safety, or behavior of every possible HA configuration.

The clock is real elapsed monotonic time. Tests intentionally use short intervals and scheduling margin. We do not patch internal HA delay methods, rewrite production timer durations or claim virtual-time equivalence. DST, wall-clock scheduling, full HA process restart and Recorder persistence are outside v1. Reload is tested; it is not a process restart.

Input contains no executable templates or integration configuration. Each worker uses a clean temporary directory, a stripped environment and a global audit guard. This prevents accidental Python network/subprocess I/O through the admitted path. It is not a hostile-code sandbox: Python/native dependencies, the interpreter and host are trusted. Run untrusted source or dependencies only in a separately secured environment. The optional Docker network-none recipe strengthens network isolation but does not prove hardware behavior.

Public reports should contain only synthetic fixtures. Real state timelines reveal occupancy and habits even without a token. No household inventory, recordings or production configuration is included here. All diagrams are labelled synthetic and reproducible with `python scripts/render_diagrams.py`.

See [validation](validation.md) for the measured checks performed on this release. Installation support is limited to environments in that record; the container recipe is not a claim that every platform was tested.
