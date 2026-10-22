# Reikwijdte en bewijs

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

Deze versie valideert een begrensde deelverzameling met echte Home Assistant-triggers, voorwaarden, timers, herladen en afhandeling van scriptacties. De ontvangers van actuatorcommando’s en de invoertoestanden zijn synthetisch. Dit bewijst geen communicatieprotocollen, stroomverbruik, sensornauwkeurigheid, fysieke relaistoestand, veiligheid of gedrag van elke mogelijke HA-configuratie.

De klok meet werkelijk verstreken monotone tijd. Tests gebruiken bewust korte intervallen en planningsmarge. We passen geen interne HA-vertragingsmethoden aan, herschrijven geen productietimers en claimen geen gelijkwaardigheid met virtuele tijd. Zomertijd, planning volgens de wandklok, volledig opnieuw starten van het HA-proces en Recorder-persistentie vallen buiten v1. Herladen wordt getest; dat is geen procesherstart.

De invoer bevat geen uitvoerbare sjablonen of integratieconfiguratie. Elke worker gebruikt een schone tijdelijke map, een opgeschoonde omgeving en een globale auditbeveiliging. Dit voorkomt onbedoelde Python-netwerk- en subproces-I/O via het toegestane pad. Het is geen sandbox voor vijandige code: Python- en native afhankelijkheden, de interpreter en de host worden vertrouwd. Voer onbetrouwbare broncode of afhankelijkheden uitsluitend uit in een afzonderlijk beveiligde omgeving. Het optionele Docker-recept zonder netwerk versterkt de netwerkisolatie maar bewijst geen hardwaregedrag.

Openbare rapporten mogen alleen synthetische fixtures bevatten. Werkelijke toestandstijdlijnen onthullen aanwezigheid en gewoonten, ook zonder token. Hier zijn geen huishoudinventaris, opnamen of productieconfiguratie opgenomen. Alle diagrammen zijn als synthetisch gemarkeerd en reproduceerbaar met `python scripts/render_diagrams.py`.

Zie [validatie](validation.md) voor de gemeten controles van deze versie. Installatieondersteuning beperkt zich tot de omgevingen in dat verslag; het containerrecept beweert niet dat elk platform is getest.
