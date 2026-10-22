# Ambito e prove

<!-- language-navigation:start -->
<p dir="ltr">
<a href="limits.md" lang="en" dir="ltr">English</a> ·
<a href="limits.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="limits.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="limits.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="limits.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="limits.es.md" lang="es" dir="ltr">Español</a> ·
<a href="limits.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="limits.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="limits.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="limits.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="limits.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="limits.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="limits.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="limits.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="limits.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="limits.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="limits.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="limits.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="limits.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="limits.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="limits.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="limits.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="limits.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="limits.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Questa versione valida un sottoinsieme limitato con trigger, condizioni, timer, ricaricamento e inoltro delle azioni di script reali di Home Assistant. I destinatari dei comandi degli attuatori e gli stati di ingresso sono sintetici. Non dimostra protocolli fisici, assorbimento di corrente, precisione dei sensori, stato fisico di un relè, sicurezza o comportamento di ogni configurazione HA possibile.

L’orologio misura il tempo monotono realmente trascorso. I test usano intenzionalmente intervalli brevi e margine per la pianificazione. Non modifichiamo i metodi interni di ritardo di HA, non riscriviamo le durate dei timer di produzione e non dichiariamo equivalenza con il tempo virtuale. Cambi d’ora legale, pianificazione sull’orologio civile, riavvio completo del processo HA e persistenza di Recorder sono fuori da v1. Viene testato il reload, che non è un riavvio del processo.

L’ingresso non contiene template eseguibili o configurazioni di integrazione. Ogni worker usa una directory temporanea pulita, un ambiente ripulito e una protezione globale di audit. Questo impedisce I/O accidentale di rete o sottoprocessi Python attraverso il percorso ammesso. Non è una sandbox per codice ostile: dipendenze Python e native, interprete e host sono considerati affidabili. Esegui sorgenti o dipendenze non attendibili soltanto in un ambiente protetto separato. La ricetta Docker facoltativa senza rete rafforza l’isolamento di rete, ma non dimostra il comportamento dell’hardware.

I rapporti pubblici devono contenere soltanto fixture sintetiche. Cronologie di stati reali rivelano presenza e abitudini anche senza token. Qui non sono inclusi inventari domestici, registrazioni o configurazioni di produzione. Tutti i diagrammi sono etichettati come sintetici e riproducibili con `python scripts/render_diagrams.py`.

Consulta la [validazione](validation.it.md) per le verifiche misurate effettuate su questa versione. Il supporto all’installazione è limitato agli ambienti di quel registro; la ricetta del container non dichiara che ogni piattaforma sia stata testata.
