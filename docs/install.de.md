# Installation und Begrenzung der Umgebung

<!-- language-navigation:start -->
<p dir="ltr">
<a href="install.md" lang="en" dir="ltr">English</a> ·
<a href="install.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="install.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="install.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="install.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="install.es.md" lang="es" dir="ltr">Español</a> ·
<a href="install.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="install.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="install.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="install.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="install.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="install.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="install.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="install.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="install.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="install.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="install.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="install.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="install.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="install.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="install.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="install.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="install.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="install.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Verwenden Sie die festgelegte Home-Assistant-Laufzeit mit Python 3.14.2–3.14.x. Installieren Sie `requirements.lock` mit `--require-hashes` und anschließend dieses Paket mit `--no-deps .`, wie im README im Stammverzeichnis gezeigt. Die Lockdatei umfasst Anwendungs- und Testabhängigkeiten. Eine saubere Umgebung ist erforderlich; installieren Sie nicht in Ihrer produktiven Home-Assistant-Umgebung. Verwenden Sie beim Bearbeiten des Quellcodes stattdessen `pip install --no-deps -e .`.

Führen Sie zuerst `ha-scenario validate examples/stale_sensor.json` aus. Die Validierung importiert keine HA-Laufzeit. Führen Sie danach `ha-scenario run examples/stale_sensor.json --report result.json` aus. Es wird kein Zielserver konfiguriert. Der einzige Ausgabepfad stammt aus Ihrem ausdrücklich angegebenen Argument `--report`, nicht aus dem Szenario.

Für eine stärkere Netzwerkbegrenzung:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Der Build benötigt Internetzugriff für Abhängigkeiten. Die Ausführung hat kein Netzwerk und ein beschreibbares, nach Gebrauch verworfenes `/tmp`; sie bindet weder die Heimkonfiguration noch Docker-Socket oder Zugangsdaten ein. Dies ist eine optionale Bereitstellungsanleitung; dem Validierungsprotokoll entnehmen Sie, ob genau dieser Container ausgeführt wurde. Fügen Sie kein Hostnetzwerk und keine produktiven Mounts hinzu.

Die Unterprozessschnittstelle entfernt geerbte Zugangsdaten und `PYTHONPATH`. Der Worker verwendet mit `-I` das installierte Paket. Nur PATH, SYSTEMROOT und LANG werden geerbt; der Hash-Seed ist festgelegt. Unter Linux wird der Bibliothekspfad des Workers aus `LIBDIR` der laufenden Python-Installation abgeleitet, damit verschiebbare Python-Builds libpython finden. Ein geerbtes `LD_LIBRARY_PATH` wird niemals kopiert. Für das Kind gelten ein übergeordneter Timeout von 30 Sekunden, ein interner Timeout von 20 Sekunden, höchstens 5 Sekunden angeforderte Wartezeit in der Zeitleiste und 256 erfasste Aktionen. Hängende native Abhängigkeiten beendet der übergeordnete Timeout.

Das pytest-Plugin wird automatisch installiert. Ein Test kann ein Szenario mit `ha_scenario_tests.schema.load` laden und die Fixture `scenario_runner` aufrufen. JUnit erzeugt pytest selbst. `run_scenario` kann auch in gewöhnlichem Python importiert werden.
