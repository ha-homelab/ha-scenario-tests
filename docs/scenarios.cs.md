# Kontrakt scénáře v1

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

Rozhodujícím validátorem je `src/ha_scenario_tests/schema.py`. Pouze JSON, nejvýše 64 KiB. Neznámé klíče, duplicitní klíče JSON, symbolické odkazy jako vstup, nekonečná či nečíselná číselná hodnota a neplatné typy se odmítají. Nekopírujte domácí konfiguraci do veřejných příkladů.

Povinná kořenová pole: `schema: "ha-scenario/v1"`, krátké `name` malými písmeny, `seed`, `automations`, `timeline`, `expect`. Volitelné `settle_seconds` má výchozí hodnotu 0.1. Všechna ID entit používají předponu `scenario_` a musí být deklarována v seedu. Podporované domény: `light`, `switch`, `input_boolean`, `binary_sensor`. Podporované stavy: `on`, `off`, `unknown`, `unavailable`.

Automatizace má `id`, `triggers`, `actions`, volitelně `conditions` a `mode` (`single` nebo `restart`). Stavové triggery vyžadují `trigger`, `entity_id`, `to`; volitelně `from` a `for_seconds`. Triggery událostí používají `trigger: "event"` a `event_type: "scenario_name"`; podporováno je také `automation_reloaded`. Podmínky jsou pouze porovnání stavů. Akce obsahují `action` a jedno `entity_id`: `turn_on`, `turn_off`, `toggle` u entit light/switch/input_boolean ze seedu. Nejsou povoleny šablony, selektory, akce zařízení, blueprinty, skripty z disku ani data služeb.

Kroky časové osy obsahují `after` (relativní sekundy od dokončení předchozího kroku) a právě jednu operaci:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Další operace: `"event": "scenario_manual_off"` nebo `"reload": true`. Reload volá skutečnou službu automatizací HA, která čte vytvořený dočasný `configuration.yaml`; test nenapodobuje znovunačtení pouhým vyvoláním události jeho dokončení.

`expect.calls` je přesný uspořádaný seznam záznamů `{action, entity_id}` včetně opakování; prázdný seznam zakazuje všechna volání akčních členů. `expect.forbidden` volitelně uvádí volání, která nikdy nesmějí nastat. `expect.states` mapuje ID ze seedu na koncové stavy. Neočekávaná volání způsobí neúspěch, i když koncový stav náhodou odpovídá.

Limity: 64 entit v seedu, 16 automatizací, 8 triggerů a 8 podmínek na automatizaci, 16 akcí na automatizaci, 32 kroků časové osy, celkem 5 sekund požadovaného čekání, 256 zachycených volání. Chyby úloh na pozadí a blokované I/O způsobí selhání běhu. Zpráva obsahuje monotónní uplynulé časy volání a kroků, načtené komponenty, koncové stavy a kódy selhání.

Rodič před vrácením ověřuje celou zprávu workeru. `passed` musí být skutečná booleovská hodnota, `physical_validation` musí být false a schéma, verze HA, název scénáře, pole i meze musí odpovídat protokolu. Rodič navíc kontroluje tvrzení o voláních a stavech proti scénáři místo důvěry v příznak úspěchu. Neplatný výstup i každý nenulový návratový kód workeru jsou běhové chyby, i když potomek vypsal JSON vypadající jako úspěšný výsledek.

Přiložený příklad stale představuje ztrátu přenosu stavem `unavailable`. Neodvozuje čerstvost zdroje z `last_changed`, netestuje parsování časových značek senzoru ani neprokazuje skutečné chování při vypršení platnosti senzoru. Ruční přepsání je výslovná syntetická politika; nástroj ji nepřidává do existující automatizace.
