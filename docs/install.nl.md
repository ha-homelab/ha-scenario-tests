# Installatie en begrenzing

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

Gebruik de vastgezette Home Assistant-runtime met Python 3.14.2–3.14.x. Installeer `requirements.lock` met `--require-hashes` en daarna dit pakket met `--no-deps .`, zoals in het README in de hoofdmap. Het lockbestand omvat applicatie- en testafhankelijkheden. Een schone omgeving is vereist; installeer niet in uw Home Assistant-productieomgeving. Gebruik bij het aanpassen van broncode in plaats daarvan `pip install --no-deps -e .`.

Voer eerst `ha-scenario validate examples/stale_sensor.json` uit. De validatie importeert geen HA-runtime. Voer daarna `ha-scenario run examples/stale_sensor.json --report result.json` uit. Er wordt geen doelserver ingesteld. Het enige uitvoerpad komt uit uw expliciete argument `--report`, niet uit het scenario.

Voor een sterkere netwerkgrens:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

De build heeft internettoegang nodig voor afhankelijkheden. De uitvoering heeft geen netwerk en een tijdelijk beschrijfbaar `/tmp`; de thuisconfiguratie, Docker-socket en inloggegevens worden niet aangekoppeld. Dit is een optioneel implementatierecept; raadpleeg het validatieverslag om te zien of precies deze container is uitgevoerd. Voeg geen hostnetwerk of productiemounts toe.

De subprocesinterface verwijdert geërfde inloggegevens en `PYTHONPATH`. De worker gebruikt met `-I` het geïnstalleerde pakket. Alleen PATH, SYSTEMROOT en LANG worden geërfd; de hashseed staat vast. Op Linux wordt het bibliotheekpad van de worker afgeleid van `LIBDIR` van de actieve Python-installatie, zodat verplaatsbare Python-builds libpython kunnen vinden. Een geërfde `LD_LIBRARY_PATH` wordt nooit overgenomen. Het kindproces heeft een oudertimeout van 30 seconden, een interne timeout van 20 seconden, hoogstens 5 seconden aangevraagde wachttijd op de tijdlijn en 256 vastgelegde acties. De oudertimeout beëindigt vastgelopen native afhankelijkheden.

De pytest-plugin wordt automatisch geïnstalleerd. Een test kan een scenario laden met `ha_scenario_tests.schema.load` en de fixture `scenario_runner` aanroepen. pytest zelf maakt JUnit. `run_scenario` kan ook in gewone Python-code worden geïmporteerd.
