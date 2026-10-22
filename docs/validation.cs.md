# Záznam validace

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

## 2026-10-15: validace běhu v Linuxu

[Běh GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) prošel na commitu `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` s CPythonem 3.14.8 na Ubuntu a Home Assistantem připnutým na 2026.10.0. Úplný příkaz `python3 -m pytest -q` skončil s výsledkem **54 úspěšných testů za 21.42 s**, bez přeskočených testů. Zahrnuje všech sedm běhových testů se skutečným HA: čtyři ukázkové scénáře, případ se záměrně selhávajícím očekáváním a zakázanou akcí, JSON zprávu lokalizovaného CLI a kontrakt předání role navazujícího projektu. Každý běhový test spouští nový řízený worker; očekávaná selhání se testují jako selhání, nikoli hlásí jako úspěšné scénáře.

V témže běhu prošly také Ruff, kontroly odkazů dokumentace a SVG, sestavení zdrojového balíčku a wheelu, pravidla publikace zdrojů a kontrola tajných údajů v celé historii. To ověřuje syntetické předávání službám a chování stavů pod zdokumentovanou ochranou I/O Pythonu. Neprokazuje bezpečnostní sandbox operačního systému, neověřuje spuštění Dockeru ani nedokazuje fyzické chování zařízení.

## 2026-10-15: vývojové kontroly v macOS

Zdrojový kód, přísná kontrola vstupu, auditní ochrana Pythonu, překlady CLI a regenerace SVG byly lokálně zkontrolovány Pythonem 3.14.7 na macOS arm64. `python -m pytest -q -m 'not runtime'` prošel **47 testy**; sedm případů se skutečným HA tento příkaz výslovně vylučuje. `python -m ruff check src tests scripts` prošel. To nenahrazuje úplnou běhovou sadu.

Skutečný engine Home Assistant 2026.10.0 načetl `automation`, `blueprint` a `trace` a provedl scénáře timeoutu přítomnosti a ručního přepsání s očekávanými syntetickými voláními služeb, koncovými stavy a bez blokovaného I/O. Místní proces Pythonu následně při ukončování interpretu skončil nativní chybou segmentace. Rodičovský runner správně považuje nenulový návratový kód za běhové selhání, i když mu předcházel úspěšný JSON. **Úplný úspěšný běhový test v macOS se netvrdí.**

Před přijetím vydání je povinná úplná sada Linux CI. Spusťte `python -m pytest -q --junitxml=junit.xml`; chybějící HA, nesprávné verze HA, timeouty potomků a nenulové návratové kódy znamenají selhání, nikdy tiché přeskočení. Výše odkazovaný běh je linuxovým důkazem této implementace; pozdější změny vyžadují vlastní úspěšný běh. Tento záznam netvrdí spuštění Dockeru ani validaci fyzických zařízení.

## Řízená zaváděcí metadata

Worker poskytuje syntetickou hodnotu `synthetic` pro procesorová metadata v cache Pythonu a před importem HA vypíná `socket.has_ipv6`. Tím brání inicializaci platformy HA spouštět `uname -p` a zabraňuje zkoušce navázání lokálního IPv6 při importu urllib3. V Linuxu se ifaddr importuje pod ochranou pomocí `ctypes.CDLL(None)`, která řeší symboly libc již načtené v procesu; obejde se tak podproces `ldconfig` při hledání knihovny. Běžné hledání knihoven se okamžitě obnoví. Ochrana I/O nemá pro tyto operace výjimku v seznamu povolených. Tyto změny ovlivňují jen metadata a sondy hostitele; triggery, podmínky, časovače, reload, skripty a předávání službám HA jsou skutečné. Závisí na verzích a pokrývá je připnutá běhová sada.

## Reprodukce

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Žádná zpráva neprokazuje skutečný stav relé, doručení rádiem, přesnost přítomnosti v domácnosti ani časování s produkčními délkami. Časová osa SVG ukazuje syntetická očekávání, nikoli benchmarková měření.

Běhová sada zahrnuje také `tests/fixtures/role_transfer.json`, syntetický kontrakt navazujícího projektu: současná role se vypne a zásuvka vyřazená z role zůstane zapnutá. Nejde o test fyzického předání zátěže.
