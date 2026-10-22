# Řešení problémů

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

- Návratový kód 2 při instalaci nebo spuštění: ověřte Python 3.14.2–3.14.x, přesnou připnutou verzi HA a čisté virtuální prostředí. Runner odmítá jiné verze HA. Před nahlášením chyby znovu nainstalujte uzamčené závislosti.
- Selhání nebo timeout workeru: selhal import závislosti nebo inicializace HA. Spusťte izolovaný worker přímo se **syntetickým** souborem pro získání místního tracebacku: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Nezveřejňujte nezkontrolovanou diagnostiku prostředí.
- `calls_mismatch`: porovnejte pořadí a duplicitní volání, nejen koncový stav. Stavy seedu se nastavují před startem; automaticky se nepočítají jako nový stavový trigger po startu.
- `forbidden_call`: zachycený příkaz syntetického akčního členu odpovídal negativnímu kontraktu. Jde o skutečné předání automatizací, nikoli fyzickou aktivaci.
- `states_mismatch`: přiřazení na časové ose nebo syntetický akční člen zanechal jiný stav.
- `blocked_io` nebo `background_exception`: nikdy nevypínejte ochranu kvůli zelenému výsledku. Tato verze nepovoluje síťové integrace. Nahlaste syntetickou reprodukci a verzi.
- Nestabilní testy časovačů: zvětšete odstup mezi změnou stavu a ověřovanou lhůtou. Měří se skutečné plánování smyčky událostí; virtuální hodiny ani přesnost plánování na mikrosekundy se neslibují.
- Reload: časovače `for` může skutečné znovunačtení zrušit. Pokud politika vyžaduje obnovu, je nutná výslovná usmiřovací automatizace; porovnejte `reload_reconcile.json`.
- Existující zpráva: `--report` ji záměrně odmítá přepsat. Zvolte novou cestu.

Pokud po needitovatelné instalaci používáte zdrojový strom, před testováním změn balíček přeinstalujte. Pro vývoj instalujte s `--no-deps -e .`.
