# Installazione e contenimento

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

Usa il runtime Home Assistant fissato con Python 3.14.2–3.14.x. Installa `requirements.lock` con `--require-hashes`, poi installa questo pacchetto con `--no-deps .`, come mostrato nel README principale. Il lock copre le dipendenze dell’applicazione e dei test. È richiesto un ambiente pulito: non installare nell’ambiente Home Assistant di produzione. Per modificare i sorgenti usa invece `pip install --no-deps -e .`.

Esegui prima `ha-scenario validate examples/stale_sensor.json`. La validazione non importa il runtime HA. Poi esegui `ha-scenario run examples/stale_sensor.json --report result.json`. Non viene configurato alcun server di destinazione. L’unico percorso di uscita deriva dall’argomento esplicito `--report`, non dallo scenario.

Per un isolamento di rete più forte:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

La compilazione richiede accesso a Internet per le dipendenze. L’esecuzione non dispone di rete e usa un `/tmp` scrivibile e temporaneo; non monta la configurazione domestica, il socket Docker o credenziali. È una ricetta di distribuzione facoltativa: consulta il registro di validazione per sapere se questo preciso container è stato eseguito. Non aggiungere la rete host o montaggi di produzione.

L’interfaccia dei sottoprocessi elimina le credenziali ereditate e `PYTHONPATH`. Il worker con `-I` usa il pacchetto installato. Eredita soltanto PATH, SYSTEMROOT e LANG; il seed dell’hash è fisso. Su Linux il percorso delle librerie del worker deriva dal `LIBDIR` dell’installazione Python in uso, consentendo alle build Python rilocabili di trovare libpython. Un `LD_LIBRARY_PATH` ereditato non viene mai copiato. Il processo figlio ha un timeout del padre di 30 secondi, uno interno di 20 secondi, al massimo 5 secondi di attese richieste nella cronologia e 256 azioni registrate. Il timeout del padre termina i blocchi delle dipendenze native.

Il plugin pytest si installa automaticamente. Un test può caricare uno scenario con `ha_scenario_tests.schema.load` e chiamare la fixture `scenario_runner`. JUnit è generato da pytest stesso. `run_scenario` può anche essere importato da normale codice Python.
