# Probleemoplossing

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

- Exitcode 2 tijdens installatie of uitvoering: controleer Python 3.14.2–3.14.x, de exacte vastgezette HA-versie en een schone virtuele omgeving. De runner weigert andere HA-versies. Installeer het lockbestand opnieuw voordat u een fout meldt.
- Workerfout of -timeout: een afhankelijkheidsimport of HA-initialisatie is mislukt. Start de geïsoleerde worker rechtstreeks met een **synthetisch** bestand voor een lokale traceback: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Publiceer geen ongecontroleerde omgevingsdiagnose.
- `calls_mismatch`: vergelijk volgorde en dubbele aanroepen, niet alleen de eindtoestand. Seed-toestanden worden vóór het opstarten ingesteld; ze tellen niet automatisch als een nieuwe toestandstrigger na het opstarten.
- `forbidden_call`: een vastgelegd synthetisch actuatorcommando voldeed aan het negatieve contract. Dit is echte afhandeling van automatisering, geen fysieke activering.
- `states_mismatch`: een tijdlijntoewijzing of synthetische actuator liet een andere toestand achter.
- `blocked_io` of `background_exception`: schakel de beveiliging nooit uit om een groen resultaat te krijgen. Deze versie staat geen netwerkintegraties toe. Meld de synthetische reproductie en de versie.
- Instabiele timertests: vergroot de afstand tussen een toestandsovergang en de getoetste deadline. Werkelijke event-loopplanning wordt gemeten; een virtuele klok of exacte microsecondeplanning wordt niet beloofd.
- Herladen: `for`-timers kunnen door het echte herladen worden geannuleerd. Er is een expliciete reconciliatieautomatisering nodig als het beleid herstel vereist; vergelijk `reload_reconcile.json`.
- Bestaand rapport: `--report` weigert dit bewust te overschrijven. Kies een nieuw pad.

Gebruikt u de bronboom na een niet-bewerkbare installatie, installeer het pakket dan opnieuw voordat u wijzigingen test. Installeer voor ontwikkeling met `--no-deps -e .`.
