# Validierungsprotokoll

<!-- language-navigation:start -->
<p dir="ltr">
<a href="validation.md" lang="en" dir="ltr">English</a> ·
<a href="validation.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="validation.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="validation.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="validation.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="validation.es.md" lang="es" dir="ltr">Español</a> ·
<a href="validation.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="validation.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="validation.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="validation.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="validation.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="validation.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="validation.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="validation.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="validation.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="validation.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="validation.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="validation.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="validation.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="validation.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="validation.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="validation.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="validation.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="validation.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

## 2026-10-15: Laufzeitvalidierung unter Linux

[GitHub-Actions-Lauf 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) war bei Commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` erfolgreich, mit CPython 3.14.8 unter Ubuntu und festgelegtem Home Assistant 2026.10.0. Der vollständige Befehl `python3 -m pytest -q` endete mit **54 bestandenen Tests in 21.42 s**, ohne übersprungene Tests. Dies umfasst alle sieben Laufzeittests mit echtem HA: vier Beispielszenarien, einen absichtlich fehlschlagenden Fall mit Erwartung beziehungsweise verbotener Aktion, den JSON-Bericht der lokalisierten CLI und den Rollenübergabevertrag eines nachgelagerten Projekts. Jeder Laufzeittest startet einen frischen kontrollierten Worker; erwartete Fehlschläge werden als Fehlschläge getestet und nicht als erfolgreiche Szenarien gemeldet.

Ruff, Dokumentationslinks und SVG-Prüfungen, Quell- und Wheel-Builds, die Veröffentlichungsrichtlinie für Quellen und die Geheimnissuche über die gesamte Historie waren in diesem Lauf ebenfalls erfolgreich. Dies validiert synthetische Serviceweiterleitung und Zustandsverhalten unter dem dokumentierten Python-E/A-Schutz. Es belegt weder eine Sicherheits-Sandbox des Betriebssystems noch eine Docker-Ausführung oder physisches Geräteverhalten.

## 2026-10-15: Entwicklungsprüfungen unter macOS

Quellcode, strenge Eingabezulassung, Python-Audit-Schutz, CLI-Übersetzungen und SVG-Neuerzeugung wurden lokal mit Python 3.14.7 unter macOS arm64 geprüft. `python -m pytest -q -m 'not runtime'` bestand **47 Tests**; sieben Fälle mit echtem HA schließt dieser Befehl ausdrücklich aus. `python -m ruff check src tests scripts` war erfolgreich. Dies ersetzt nicht die vollständige Laufzeittestsuite.

Die echte Home-Assistant-Engine 2026.10.0 lud `automation`, `blueprint` und `trace` und führte die Szenarien für Anwesenheitstimeout und manuelle Übersteuerung mit den erwarteten synthetischen Serviceaufrufen, Endzuständen und ohne blockierte E/A aus. Anschließend endete der lokale Python-Prozess beim Herunterfahren des Interpreters mit einem nativen Segmentierungsfehler. Der übergeordnete Runner behandelt diesen von null verschiedenen Exitcode korrekt als Laufzeitfehler, selbst wenn zuvor eine erfolgreiche JSON-Ausgabe erfolgte. **Ein vollständig bestandener macOS-Laufzeittest wird nicht behauptet.**

Vor Annahme einer Version ist die vollständige Linux-CI-Suite erforderlich. Führen Sie `python -m pytest -q --junitxml=junit.xml` aus; fehlendes HA, falsche HA-Versionen, Kindprozess-Timeouts und Exitcodes ungleich null führen zum Fehlschlag, niemals zum stillen Überspringen. Der oben verlinkte Lauf ist der Linux-Nachweis für diese Implementierung; spätere Änderungen benötigen ihren eigenen erfolgreichen Lauf. Dieses Protokoll behauptet weder eine Docker-Ausführung noch eine Prüfung physischer Geräte.

## Kontrollierte Bootstrap-Metadaten

Der Worker setzt für die zwischengespeicherten Prozessormetadaten von Python den synthetischen Wert `synthetic` und deaktiviert `socket.has_ipv6` vor dem HA-Import. Dies verhindert, dass die HA-Plattforminitialisierung `uname -p` startet, und unterbindet die lokale IPv6-Bindungsprobe beim Import von urllib3. Unter Linux wird ifaddr unter dem Schutz mit `ctypes.CDLL(None)` importiert, wodurch bereits im Prozess geladene libc-Symbole aufgelöst werden; so entfällt der `ldconfig`-Unterprozess der Bibliothekssuche. Die normale Bibliothekssuche wird sofort wiederhergestellt. Der E/A-Schutz hat keine Ausnahmeliste für diese Vorgänge. Diese Änderungen betreffen ausschließlich Hostmetadaten und -proben; HA-Trigger, Bedingungen, Timer, Reload, Skripte und Serviceweiterleitung sind echt. Sie sind versionsabhängig und durch die festgelegte Laufzeitsuite abgedeckt.

## Reproduzieren

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Kein Bericht belegt den echten Relaiszustand, Funkzustellung, die Genauigkeit der Anwesenheitserkennung im Haushalt oder produktive Zeitdauern. Die SVG-Zeitleiste zeigt synthetische Erwartungen, keine Benchmarkmessungen.

Die Laufzeitsuite enthält außerdem `tests/fixtures/role_transfer.json`, den synthetischen Vertrag eines nachgelagerten Projekts: Die aktuelle Rolle schaltet aus und die ausgemusterte Steckdose bleibt an. Dies ist kein Test einer physischen Lastübergabe.
