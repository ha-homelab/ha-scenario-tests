# Rozsah a důkazy

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

Tato verze ověřuje omezenou podmnožinu se skutečnými triggery, podmínkami, časovači, znovunačtením a předáváním akcí skriptů Home Assistant. Příjemci příkazů akčních členů a vstupní stavy jsou syntetické. Neprokazuje komunikační protokoly, proudový odběr, přesnost senzorů, fyzický stav relé, bezpečnost ani chování všech možných konfigurací HA.

Hodiny měří skutečný uplynulý monotónní čas. Testy záměrně používají krátké intervaly a rezervu pro plánování. Neupravujeme interní metody zpoždění HA, nepřepisujeme produkční délky časovačů a netvrdíme rovnocennost s virtuálním časem. Změny letního času, plánování podle nástěnných hodin, úplný restart procesu HA a perzistence Recorderu nejsou součástí v1. Testuje se reload; nejde o restart procesu.

Vstup neobsahuje spustitelné šablony ani konfiguraci integrací. Každý worker používá čistý dočasný adresář, očištěné prostředí a globální auditní ochranu. To zabraňuje náhodnému síťovému I/O a spouštění podprocesů Pythonem přes povolenou cestu. Není to sandbox pro škodlivý kód: důvěřuje se závislostem Pythonu i nativním závislostem, interpretu a hostiteli. Nedůvěryhodné zdroje nebo závislosti spouštějte jen v samostatně zabezpečeném prostředí. Volitelný postup Dockeru bez sítě posiluje síťovou izolaci, ale neprokazuje chování hardwaru.

Veřejné zprávy mají obsahovat pouze syntetické fixture. Skutečné časové průběhy stavů odhalují přítomnost a návyky i bez tokenu. Nejsou zde zahrnuty inventáře domácnosti, záznamy ani produkční konfigurace. Všechny diagramy jsou označené jako syntetické a reprodukovatelné pomocí `python scripts/render_diagrams.py`.

Naměřené kontroly provedené u této verze uvádí [validace](validation.md). Podpora instalace se omezuje na prostředí v tomto záznamu; návod pro kontejner netvrdí, že byly testovány všechny platformy.
