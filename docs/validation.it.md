# Registro di validazione

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

## 2026-10-15: validazione del runtime Linux

L’[esecuzione GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) è passata al commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, usando CPython 3.14.8 su Ubuntu e Home Assistant fissato a 2026.10.0. Il comando completo `python3 -m pytest -q` ha terminato con **54 test superati in 21.42 s**, senza test saltati. Include tutti e sette i test di runtime con HA reale: quattro scenari di esempio, un caso intenzionalmente errato di aspettativa e azione proibita, il rapporto JSON della CLI localizzata e il contratto di trasferimento di ruolo per un progetto a valle. Ogni test di runtime avvia un nuovo worker controllato; le asserzioni di errore atteso sono verificate come errori, non riportate come scenari riusciti.

Nella stessa esecuzione sono passati anche Ruff, i controlli dei link della documentazione e degli SVG, le build sorgente e wheel, la politica di pubblicazione dei sorgenti e la scansione dei segreti nell’intera cronologia. Ciò valida l’inoltro sintetico dei servizi e il comportamento degli stati sotto la protezione I/O Python documentata. Non dimostra una sandbox di sicurezza del sistema operativo, non valida un’esecuzione Docker e non prova il comportamento di dispositivi fisici.

## 2026-10-15: controlli di sviluppo macOS

Sorgenti, ammissione rigorosa degli ingressi, protezione di audit Python, traduzioni CLI e rigenerazione SVG sono stati controllati localmente con Python 3.14.7 su macOS arm64. `python -m pytest -q -m 'not runtime'` ha superato **47 test**; sette casi con HA reale sono esplicitamente esclusi da quel comando. `python -m ruff check src tests scripts` è passato. Non sostituisce la suite completa di runtime.

Il vero motore Home Assistant 2026.10.0 ha caricato `automation`, `blueprint` e `trace` ed eseguito gli scenari di timeout della presenza e override manuale con le chiamate sintetiche attese, gli stati finali e senza I/O bloccato. Il processo Python locale è poi terminato con un errore di segmentazione nativo durante la chiusura dell’interprete. Il runner padre tratta correttamente tale uscita non nulla come un errore di runtime, anche se preceduta da un JSON positivo. **Non viene dichiarato il superamento completo di un test di runtime macOS.**

La suite Linux CI completa è necessaria prima di accettare una versione. Esegui `python -m pytest -q --junitxml=junit.xml`: HA mancante, versioni HA errate, timeout e uscite non nulle dei figli causano errori, mai esclusioni silenziose. L’esecuzione collegata sopra è la prova Linux per questa implementazione; modifiche successive richiedono una propria esecuzione superata. In questo registro non si dichiara alcuna esecuzione Docker o validazione di dispositivi fisici.

## Metadati di bootstrap controllati

Il worker fornisce il valore sintetico `synthetic` ai metadati del processore memorizzati nella cache di Python e disattiva `socket.has_ipv6` prima di importare HA. Questo impedisce all’inizializzazione di piattaforma HA di avviare `uname -p` ed evita la prova di bind IPv6 locale durante l’importazione di urllib3. Su Linux ifaddr viene importato sotto protezione usando `ctypes.CDLL(None)`, risolvendo simboli libc già caricati nel processo; si evita così il sottoprocesso `ldconfig` della ricerca librerie. La ricerca ordinaria viene subito ripristinata. La protezione I/O non ha eccezioni di autorizzazione per queste operazioni. Le modifiche riguardano solo metadati e sonde dell’host; trigger, condizioni, timer, reload, script e inoltro dei servizi HA sono reali. Dipendono dalle versioni e sono coperti dalla suite di runtime fissata.

## Riproduzione

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Nessun rapporto prova lo stato reale del relè, la consegna radio, la precisione della presenza domestica o i tempi di durata della produzione. La cronologia SVG mostra aspettative sintetiche, non misurazioni di benchmark.

La suite di runtime include anche `tests/fixtures/role_transfer.json`, il contratto sintetico a valle: il ruolo attuale si spegne e la presa dismessa dal ruolo rimane accesa. Non è un test di trasferimento fisico del carico.
