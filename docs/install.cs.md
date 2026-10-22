# Instalace a omezení prostředí

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

Použijte pevně určenou verzi běhového prostředí Home Assistant s Pythonem 3.14.2–3.14.x. Nainstalujte `requirements.lock` s `--require-hashes` a pak tento balíček pomocí `--no-deps .`, jak ukazuje hlavní README. Soubor zámku zahrnuje závislosti aplikace i testů. Je nutné čisté prostředí; neinstalujte do produkčního prostředí Home Assistant. Při úpravách zdrojového kódu použijte místo toho `pip install --no-deps -e .`.

Nejprve spusťte `ha-scenario validate examples/stale_sensor.json`. Validace neimportuje běhové prostředí HA. Poté spusťte `ha-scenario run examples/stale_sensor.json --report result.json`. Nenastavuje se žádný cílový server. Jediná výstupní cesta pochází z vašeho výslovného argumentu `--report`, nikoli ze scénáře.

Pro silnější síťové oddělení:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Sestavení vyžaduje internetový přístup kvůli závislostem. Spuštěný kontejner nemá síť a používá jednorázový zapisovatelný `/tmp`; nepřipojuje domácí konfiguraci, socket Dockeru ani přihlašovací údaje. Jde o volitelný postup nasazení; v záznamu validace ověřte, zda byl spuštěn právě tento kontejner. Nepřidávejte síť hostitele ani produkční svazky.

Rozhraní podprocesu odstraňuje zděděné přihlašovací údaje a `PYTHONPATH`. Worker s `-I` používá nainstalovaný balíček. Dědí se pouze PATH, SYSTEMROOT a LANG; seed hašování je pevný. V Linuxu se cesta ke knihovnám workeru odvozuje z `LIBDIR` spuštěné instalace Pythonu, což přemístitelným sestavením Pythonu umožňuje najít libpython. Zděděný `LD_LIBRARY_PATH` se nikdy nekopíruje. Potomek má časový limit rodiče 30 sekund, vnitřní limit 20 sekund, nejvýše 5 sekund požadovaných čekání na časové ose a 256 zachycených akcí. Zaseknuté nativní závislosti ukončí časový limit rodiče.

Plugin pytest se instaluje automaticky. Test může načíst scénář přes `ha_scenario_tests.schema.load` a zavolat fixture `scenario_runner`. JUnit generuje samotný pytest. `run_scenario` lze importovat i v běžném Pythonu.
