# Validatieverslag

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

## 2026-10-15: Linux-runtimevalidatie

[GitHub Actions-run 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) slaagde op commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, met CPython 3.14.8 op Ubuntu en Home Assistant vastgezet op 2026.10.0. De volledige opdracht `python3 -m pytest -q` eindigde met **54 geslaagde tests in 21.42 s**, zonder overgeslagen tests. Dit omvat alle zeven runtimetests met echte HA: vier voorbeeldscenario’s, een bewust falende verwachting met verboden actie, het JSON-rapport van de gelokaliseerde CLI en het roloverdrachtcontract van een afnemend project. Elke runtimetest start een verse gecontroleerde worker; verwachte-foutasserties worden als fouten getest en niet als geslaagde scenario’s gerapporteerd.

Ook Ruff, documentatielinks en SVG-controles, bron- en wheelbuilds, het publicatiebeleid voor broncode en de geheimenscan over de volledige geschiedenis slaagden in die run. Dit valideert synthetische serviceafhandeling en toestandsgedrag onder de gedocumenteerde Python-I/O-beveiliging. Het bewijst geen beveiligingssandbox van het besturingssysteem, valideert geen Docker-uitvoering en bewijst geen fysiek apparaatgedrag.

## 2026-10-15: macOS-ontwikkelcontroles

De broncode, strikte invoertoelating, Python-auditbeveiliging, CLI-vertalingen en SVG-regeneratie zijn lokaal gecontroleerd met Python 3.14.7 op macOS arm64. `python -m pytest -q -m 'not runtime'` slaagde voor **47 tests**; zeven echte HA-gevallen zijn door die opdracht expliciet uitgesloten. `python -m ruff check src tests scripts` slaagde. Dit vervangt de volledige runtimesuite niet.

De echte Home Assistant-engine 2026.10.0 laadde `automation`, `blueprint` en `trace` en voerde de scenario’s voor aanwezigheidstimeout en handmatige overname uit met de verwachte synthetische serviceaanroepen, eindtoestanden en zonder geblokkeerde I/O. Het lokale Python-proces eindigde daarna met een native segmentatiefout tijdens het afsluiten van de interpreter. De ouderrunner behandelt die exitcode ongelijk aan nul terecht als runtimefout, ook als daarvoor een geslaagde JSON-uitvoer verscheen. **Er wordt geen volledig geslaagde macOS-runtimetest geclaimd.**

De volledige Linux-CI-suite is vereist voordat een release wordt aanvaard. Voer `python -m pytest -q --junitxml=junit.xml` uit; ontbrekende HA, onjuiste HA-versies, kindtimeouts en kindexitcodes ongelijk aan nul veroorzaken fouten, nooit stilzwijgende overslagen. De hierboven gelinkte run is het Linux-bewijs voor deze implementatie; latere wijzigingen vereisen hun eigen geslaagde run. Dit verslag claimt geen Docker-uitvoering of validatie van fysieke apparaten.

## Gecontroleerde opstartmetadata

De worker gebruikt de synthetische waarde `synthetic` voor Pythons gecachte processormetadata en schakelt `socket.has_ipv6` uit voordat HA wordt geïmporteerd. Dit voorkomt dat HA’s platforminitialisatie `uname -p` start en voorkomt de lokale IPv6-bindprobe tijdens de import van urllib3. Op Linux wordt ifaddr onder de beveiliging geïmporteerd met `ctypes.CDLL(None)`, waardoor al in het proces geladen libc-symbolen worden gevonden; dit vermijdt het `ldconfig`-subproces van de bibliotheekzoeker. De normale bibliotheekzoeker wordt onmiddellijk hersteld. De I/O-beveiliging kent geen uitzonderingen op de toelatingslijst voor deze bewerkingen. Deze wijzigingen raken alleen hostmetadata en -probes; HA-triggers, voorwaarden, timers, herladen, scripts en serviceafhandeling zijn echt. Ze zijn versiegevoelig en gedekt door de vastgezette runtimesuite.

## Reproduceren

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Geen rapport bewijst echte relaistoestand, radioaflevering, nauwkeurigheid van huishoudelijke aanwezigheidsdetectie of timing met productieduren. De SVG-tijdlijn toont synthetische verwachtingen, geen benchmarkmetingen.

De runtimesuite bevat ook `tests/fixtures/role_transfer.json`, het synthetische contract voor het afnemende project: de huidige rol schakelt uit en de uit die rol genomen stekker blijft aan. Dit is geen test van fysieke belastingoverdracht.
