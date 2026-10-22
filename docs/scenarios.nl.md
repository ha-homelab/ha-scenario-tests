# Scenariocontract v1

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

De leidende validator is `src/ha_scenario_tests/schema.py`. Alleen JSON, maximaal 64 KiB. Onbekende sleutels, dubbele JSON-sleutels, symlinks als invoer, niet-eindige getallen en ongeldige typen worden geweigerd. Kopieer geen huishoudconfiguratie naar openbare voorbeelden.

Verplichte velden op hoofdniveau: `schema: "ha-scenario/v1"`, een korte `name` in kleine letters, `seed`, `automations`, `timeline`, `expect`. Het optionele `settle_seconds` is standaard 0.1. Alle entiteits-ID’s gebruiken het voorvoegsel `scenario_` en moeten in de seed zijn gedeclareerd. Ondersteunde domeinen: `light`, `switch`, `input_boolean`, `binary_sensor`. Ondersteunde toestanden: `on`, `off`, `unknown`, `unavailable`.

Een automatisering heeft `id`, `triggers`, `actions`, optioneel `conditions` en `mode` (`single` of `restart`). Toestandstriggers vereisen `trigger`, `entity_id`, `to`; `from` en `for_seconds` zijn optioneel. Gebeurtenistriggers gebruiken `trigger: "event"` en `event_type: "scenario_name"`; ook `automation_reloaded` wordt ondersteund. Voorwaarden zijn uitsluitend toestandsvergelijkingen. Acties bevatten `action` en één `entity_id`: `turn_on`, `turn_off`, `toggle` op light/switch/input_boolean-entiteiten uit de seed. Sjablonen, selectors, apparaatacties, blueprints, scripts van schijf en servicedata zijn niet toegestaan.

Tijdlijnstappen bevatten `after` (relatieve seconden sinds de vorige voltooide stap) en precies één bewerking:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Andere bewerkingen: `"event": "scenario_manual_off"` of `"reload": true`. Herladen roept de echte automatiseringsservice van HA aan, die de gegenereerde tijdelijke `configuration.yaml` leest; de test bootst herladen niet na door de voltooiingsgebeurtenis uit te sturen.

`expect.calls` is de exacte geordende lijst van `{action, entity_id}`-records, inclusief herhalingen; een lege lijst verbiedt alle actuatoraanroepen. `expect.forbidden` vermeldt optioneel aanroepen die nooit mogen plaatsvinden. `expect.states` koppelt ID’s uit de seed aan eindtoestanden. Onverwachte aanroepen laten de test mislukken, zelfs als de eindtoestand toevallig overeenkomt.

Grenzen: 64 seed-entiteiten, 16 automatiseringen, 8 triggers en 8 voorwaarden per automatisering, 16 acties per automatisering, 32 tijdlijnstappen, in totaal 5 seconden aangevraagde wachttijd en 256 vastgelegde aanroepen. Fouten in achtergrondtaken en geblokkeerde I/O laten de uitvoering mislukken. Het rapport bevat monotoon verstreken aanroep- en staptijden, geladen componenten, eindtoestanden en foutcodes.

Het ouderproces valideert het volledige workerrapport voordat het wordt teruggegeven. `passed` moet werkelijk een booleaanse waarde zijn, `physical_validation` moet false zijn en schema, HA-versie, scenarionaam, velden en grenzen moeten overeenkomen met het protocol. De ouder controleert aanroep- en toestandsasserties ook tegen het scenario in plaats van een succesvlag te vertrouwen. Ongeldige uitvoer en elke workerexitcode ongelijk aan nul zijn uitvoeringsfouten, zelfs als het kind een succesvol ogend JSON-object heeft afgedrukt.

Het meegeleverde stale-voorbeeld geeft transportverlies weer met `unavailable`. Het leidt bronactualiteit niet af uit `last_changed`, test geen verwerking van sensortijdstempels en bewijst geen echt vervalgedrag van sensoren. Handmatige overname is een expliciet synthetisch beleid; het hulpmiddel voegt dat beleid niet toe aan een bestaande automatisering.
