# Fehlerbehebung

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

- Exitcode 2 bei Installation oder Ausführung: Prüfen Sie Python 3.14.2–3.14.x, die genaue festgelegte HA-Version und eine saubere virtuelle Umgebung. Der Runner weist andere HA-Versionen ab. Installieren Sie die Lockdatei neu, bevor Sie einen Fehler melden.
- Worker-Fehler oder -Timeout: Ein Abhängigkeitsimport oder die HA-Einrichtung ist fehlgeschlagen. Führen Sie den isolierten Worker mit einer **synthetischen** Datei direkt aus, um einen lokalen Traceback zu erhalten: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Veröffentlichen Sie keine ungeprüfte Umgebungsdiagnose.
- `calls_mismatch`: Vergleichen Sie Reihenfolge und doppelte Aufrufe, nicht nur den Endzustand. Seed-Zustände werden vor dem Start gesetzt; sie gelten nicht automatisch als neuer Zustandstrigger nach dem Start.
- `forbidden_call`: Ein erfasster synthetischer Aktorbefehl entsprach dem negativen Vertrag. Das ist eine echte Automationsweiterleitung, keine physische Betätigung.
- `states_mismatch`: Eine Zeitleistenzuweisung oder ein synthetischer Aktor hinterließ einen anderen Zustand.
- `blocked_io` oder `background_exception`: Schalten Sie niemals den Schutz ab, um ein grünes Ergebnis zu erhalten. Diese Version lässt keine Netzwerkintegrationen zu. Melden Sie die synthetische Reproduktion und die Version.
- Instabile Timertests: Vergrößern Sie den Abstand zwischen einem Zustandsübergang und der geprüften Frist. Gemessen wird die echte Event-Loop-Planung; weder eine virtuelle Uhr noch eine mikrosekundengenaue Planung wird versprochen.
- Reload: `for`-Timer können durch das echte Reload abgebrochen werden. Falls die Richtlinie Wiederherstellung verlangt, ist eine ausdrückliche Abgleichautomation erforderlich; vergleichen Sie `reload_reconcile.json`.
- Vorhandener Bericht: `--report` verweigert absichtlich das Überschreiben. Wählen Sie einen neuen Pfad.

Wenn Sie nach einer nicht editierbaren Installation mit dem Quellbaum arbeiten, installieren Sie das Paket vor dem Testen von Änderungen neu. Installieren Sie für die Entwicklung mit `--no-deps -e .`.
