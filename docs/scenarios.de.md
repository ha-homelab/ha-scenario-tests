# Szenariovertrag v1

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

Der maßgebliche Validator ist `src/ha_scenario_tests/schema.py`. Nur JSON, höchstens 64 KiB. Unbekannte und doppelte JSON-Schlüssel, Symlinks als Eingabe, nicht endliche Zahlen und ungültige Typen werden abgewiesen. Kopieren Sie keine Haushaltskonfiguration in öffentliche Beispiele.

Erforderliche Felder auf oberster Ebene: `schema: "ha-scenario/v1"`, ein kurzer kleingeschriebener `name`, `seed`, `automations`, `timeline`, `expect`. Das optionale `settle_seconds` hat den Standardwert 0.1. Alle Entitäts-IDs verwenden das Präfix `scenario_` und müssen im Seed deklariert sein. Unterstützte Domänen: `light`, `switch`, `input_boolean`, `binary_sensor`. Unterstützte Zustände: `on`, `off`, `unknown`, `unavailable`.

Eine Automation enthält `id`, `triggers`, `actions`, optional `conditions` und `mode` (`single` oder `restart`). Zustandstrigger benötigen `trigger`, `entity_id`, `to`; optional sind `from` und `for_seconds`. Ereignistrigger verwenden `trigger: "event"` und `event_type: "scenario_name"`; auch `automation_reloaded` wird unterstützt. Bedingungen sind ausschließlich Zustandsvergleiche. Aktionen enthalten `action` und eine `entity_id`: `turn_on`, `turn_off`, `toggle` für im Seed angelegte light/switch/input_boolean-Entitäten. Vorlagen, Selektoren, Geräteaktionen, Blueprints, Skripte von der Festplatte und Servicedaten sind nicht zugelassen.

Zeitleistenschritte enthalten `after` (relative Sekunden seit Abschluss des vorherigen Schritts) und genau eine Operation:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Weitere Operationen: `"event": "scenario_manual_off"` oder `"reload": true`. Reload ruft den echten Automationsdienst von HA auf, der die erzeugte temporäre `configuration.yaml` liest; der Test ahmt Reload nicht durch Auslösen seines Abschlussereignisses nach.

`expect.calls` ist die genaue geordnete Liste von `{action, entity_id}`-Datensätzen einschließlich Wiederholungen; eine leere Liste verbietet alle Aktoraufrufe. `expect.forbidden` listet optional Aufrufe auf, die niemals auftreten dürfen. `expect.states` ordnet im Seed angelegte IDs ihren Endzuständen zu. Unerwartete Aufrufe führen zum Fehlschlag, selbst wenn der Endzustand zufällig passt.

Grenzen: 64 Seed-Entitäten, 16 Automationen, je 8 Trigger und 8 Bedingungen pro Automation, 16 Aktionen pro Automation, 32 Zeitleistenschritte, insgesamt 5 Sekunden angeforderte Wartezeit und 256 erfasste Aufrufe. Fehler in Hintergrundaufgaben und blockierte E/A lassen die Ausführung fehlschlagen. Der Bericht enthält monotone verstrichene Aufruf- und Schrittzeiten, geladene Komponenten, Endzustände und Fehlercodes.

Der Elternprozess validiert den gesamten Worker-Bericht vor der Rückgabe. `passed` muss ein tatsächlicher boolescher Wert und `physical_validation` muss false sein; Schema, HA-Version, Szenarioname, Felder und Grenzen müssen dem Protokoll entsprechen. Der Elternprozess prüft außerdem Aufruf- und Zustandsbedingungen gegen das Szenario, statt einer Erfolgsmarkierung zu vertrauen. Ungültige Ausgabe und jeder von null verschiedene Worker-Exitcode sind Laufzeitfehler, auch wenn das Kind ein erfolgreich wirkendes JSON-Objekt ausgegeben hat.

Das mitgelieferte stale-Beispiel stellt einen Transportverlust durch `unavailable` dar. Es leitet die Aktualität der Quelle nicht aus `last_changed` ab, testet keine Verarbeitung von Sensorzeitstempeln und belegt kein echtes Ablaufverhalten eines Sensors. Die manuelle Übersteuerung ist eine ausdrücklich definierte synthetische Richtlinie; das Werkzeug fügt diese keiner bestehenden Automation hinzu.
