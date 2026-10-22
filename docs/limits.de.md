# Umfang und Nachweise

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

Diese Version validiert eine begrenzte Teilmenge mit echten Home-Assistant-Triggern, Bedingungen, Timern, Reload und der Weiterleitung von Skriptaktionen. Die Aktorempfänger und Eingangszustände sind synthetisch. Sie belegt weder Drahtprotokolle, Stromaufnahme, Sensorgenauigkeit, den physischen Zustand eines Relais oder Sicherheit noch das Verhalten jeder möglichen HA-Konfiguration.

Die Uhr misst echte verstrichene monotone Zeit. Tests verwenden absichtlich kurze Intervalle und einen Spielraum für die Ablaufplanung. Wir verändern weder interne HA-Verzögerungsmethoden noch produktive Timerdauern und behaupten keine Gleichwertigkeit mit virtueller Zeit. Sommerzeitwechsel, Planung nach der Wanduhr, vollständige HA-Prozessneustarts und Recorder-Persistenz gehören nicht zu v1. Reload wird getestet; es ist kein Prozessneustart.

Die Eingabe enthält keine ausführbaren Vorlagen oder Integrationskonfiguration. Jeder Worker verwendet ein sauberes temporäres Verzeichnis, eine bereinigte Umgebung und einen globalen Audit-Schutz. Dies verhindert versehentliche Netzwerk- und Unterprozess-E/A durch Python über den zugelassenen Pfad. Es ist keine Sandbox für feindlichen Code: Python- und native Abhängigkeiten, Interpreter und Host gelten als vertrauenswürdig. Führen Sie nicht vertrauenswürdigen Quellcode oder Abhängigkeiten nur in einer separat abgesicherten Umgebung aus. Die optionale Docker-Anleitung ohne Netzwerk verstärkt die Netzwerkisolation, belegt aber kein Hardwareverhalten.

Öffentliche Berichte dürfen nur synthetische Fixtures enthalten. Echte Zustandsverläufe verraten Anwesenheit und Gewohnheiten auch ohne Token. Hier sind weder Haushaltsinventar noch Aufzeichnungen oder produktive Konfiguration enthalten. Alle Diagramme sind als synthetisch gekennzeichnet und mit `python scripts/render_diagrams.py` reproduzierbar.

Die gemessenen, für diese Version ausgeführten Prüfungen stehen unter [Validierung](validation.de.md). Die Installationsunterstützung beschränkt sich auf die dort genannten Umgebungen; die Containeranleitung behauptet nicht, dass jede Plattform getestet wurde.
