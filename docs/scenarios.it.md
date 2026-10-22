# Contratto dello scenario v1

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

Il validatore autorevole è `src/ha_scenario_tests/schema.py`. Solo JSON, al massimo 64 KiB. Chiavi sconosciute, chiavi JSON duplicate, ingressi tramite link simbolici, numeri non finiti e tipi non validi vengono rifiutati. Non copiare configurazioni domestiche negli esempi pubblici.

Campi radice obbligatori: `schema: "ha-scenario/v1"`, un `name` breve e minuscolo, `seed`, `automations`, `timeline`, `expect`. Il campo facoltativo `settle_seconds` vale 0.1 per impostazione predefinita. Tutti gli ID di entità usano il prefisso `scenario_` e devono essere dichiarati nel seed. Domini supportati: `light`, `switch`, `input_boolean`, `binary_sensor`. Stati supportati: `on`, `off`, `unknown`, `unavailable`.

Un’automazione contiene `id`, `triggers`, `actions`, eventualmente `conditions` e `mode` (`single` o `restart`). I trigger di stato richiedono `trigger`, `entity_id`, `to`; `from` e `for_seconds` sono facoltativi. I trigger di evento usano `trigger: "event"` e `event_type: "scenario_name"`; è supportato anche `automation_reloaded`. Le condizioni sono soltanto confronti di stato. Le azioni contengono `action` e un solo `entity_id`: `turn_on`, `turn_off`, `toggle` su entità light/switch/input_boolean del seed. Non sono ammessi template, selettori, azioni di dispositivo, blueprint, script da disco o dati dei servizi.

I passi della cronologia contengono `after` (secondi relativi dal completamento del passo precedente) ed esattamente un’operazione:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Altre operazioni: `"event": "scenario_manual_off"` oppure `"reload": true`. Reload chiama il vero servizio di automazione HA, che legge il `configuration.yaml` temporaneo generato; il test non imita il ricaricamento emettendo il suo evento di completamento.

`expect.calls` è l’esatta lista ordinata di record `{action, entity_id}`, incluse le ripetizioni; una lista vuota vieta ogni chiamata agli attuatori. `expect.forbidden` elenca facoltativamente chiamate che non devono mai verificarsi. `expect.states` associa gli ID del seed agli stati finali. Le chiamate inattese causano un errore anche se lo stato finale coincide per caso.

Limiti: 64 entità nel seed, 16 automazioni, 8 trigger e 8 condizioni per automazione, 16 azioni per automazione, 32 passi nella cronologia, 5 secondi complessivi di attese richieste, 256 chiamate registrate. Errori delle attività in background e I/O bloccato fanno fallire l’esecuzione. Il rapporto include i tempi monotoni trascorsi di chiamate e passi, componenti caricati, stati finali e codici di errore.

Il padre valida l’intero rapporto del worker prima di restituirlo. `passed` deve essere un vero booleano, `physical_validation` deve essere false e schema, versione HA, nome dello scenario, campi e limiti devono rispettare il protocollo. Il padre verifica inoltre le asserzioni su chiamate e stati rispetto allo scenario, senza fidarsi di un indicatore di successo. Un’uscita non valida e qualsiasi codice di uscita non nullo del worker sono errori di esecuzione, anche se il figlio ha stampato un oggetto JSON dall’aspetto positivo.

L’esempio stale fornito rappresenta la perdita del trasporto tramite `unavailable`. Non deduce l’attualità della sorgente da `last_changed`, non testa l’analisi delle marche temporali del sensore né dimostra la reale scadenza di un sensore. L’override manuale è una politica sintetica esplicita; lo strumento non aggiunge tale politica a un’automazione esistente.
