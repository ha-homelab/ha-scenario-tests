# Risoluzione dei problemi

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

- Uscita 2 durante installazione o esecuzione: verifica Python 3.14.2–3.14.x, l’esatta versione HA fissata e un ambiente virtuale pulito. Il runner rifiuta altre versioni HA. Reinstalla il lock prima di segnalare un errore.
- Errore o timeout del worker: l’importazione di una dipendenza o l’inizializzazione HA è fallita. Esegui direttamente il worker isolato con un file **sintetico** per ottenere un traceback locale: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Non pubblicare diagnostica dell’ambiente non revisionata.
- `calls_mismatch`: confronta ordine e chiamate duplicate, non soltanto lo stato finale. Gli stati del seed sono impostati prima dell’avvio; non valgono automaticamente come nuovo trigger di stato dopo l’avvio.
- `forbidden_call`: un comando registrato di un attuatore sintetico corrisponde al contratto negativo. È un vero inoltro di automazione, non un’attuazione fisica.
- `states_mismatch`: un’assegnazione nella cronologia o un attuatore sintetico ha lasciato uno stato differente.
- `blocked_io` o `background_exception`: non disattivare mai la protezione per ottenere un risultato verde. Questa versione non ammette integrazioni di rete. Segnala la riproduzione sintetica e la versione.
- Test dei timer instabili: aumenta la separazione tra la transizione di stato e la scadenza verificata. Si misura la pianificazione reale dell’event loop; non sono promessi un orologio virtuale o una precisione al microsecondo.
- Reload: i timer `for` possono essere cancellati dal vero ricaricamento. Serve un’automazione esplicita di riconciliazione quando la politica richiede il recupero; confronta `reload_reconcile.json`.
- Rapporto esistente: `--report` rifiuta intenzionalmente di sovrascriverlo. Scegli un nuovo percorso.

Se usi l’albero sorgente dopo un’installazione non modificabile, reinstalla il pacchetto prima di provare le modifiche. Per lo sviluppo installa con `--no-deps -e .`.
