# Zakres i dowody

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

Ta wersja weryfikuje ograniczony podzbiór funkcji z rzeczywistymi wyzwalaczami, warunkami, timerami, przeładowaniem i dystrybucją akcji skryptów Home Assistant. Odbiorniki poleceń wykonawczych i stany wejściowe są syntetyczne. Nie dowodzi to działania protokołów komunikacyjnych, poboru prądu, dokładności czujników, fizycznego stanu przekaźnika, bezpieczeństwa ani zachowania każdej możliwej konfiguracji HA.

Zegar mierzy rzeczywisty upływ czasu monotonicznego. Testy celowo używają krótkich okresów i marginesu planowania. Nie modyfikujemy wewnętrznych metod opóźnień HA, nie przepisujemy czasów timerów produkcyjnych i nie deklarujemy równoważności z czasem wirtualnym. Zmiany czasu letniego, planowanie według zegara cywilnego, pełny restart procesu HA i trwałość Recorder są poza zakresem v1. Testowane jest przeładowanie, nie restart procesu.

Wejście nie zawiera wykonywalnych szablonów ani konfiguracji integracji. Każdy worker używa czystego katalogu tymczasowego, oczyszczonego środowiska i globalnej ochrony audytowej. Zapobiega to przypadkowemu sieciowemu I/O i uruchamianiu podprocesów Pythona przez dozwoloną ścieżkę. To nie piaskownica dla wrogiego kodu: zależnościom Pythona i natywnym, interpreterowi oraz hostowi ufa się. Niezaufane źródła lub zależności uruchamiaj tylko w oddzielnie zabezpieczonym środowisku. Opcjonalny wariant Docker bez sieci wzmacnia izolację sieci, ale nie dowodzi zachowania sprzętu.

Publiczne raporty powinny zawierać tylko syntetyczne fixture. Rzeczywiste osie czasu stanów ujawniają obecność i nawyki nawet bez tokenu. Nie ma tu domowego inwentarza, nagrań ani konfiguracji produkcyjnej. Wszystkie diagramy są oznaczone jako syntetyczne i odtwarzalne przez `python scripts/render_diagrams.py`.

Zobacz [walidację](validation.pl.md), aby sprawdzić zmierzone kontrole wykonane dla tej wersji. Obsługa instalacji ogranicza się do środowisk z tego protokołu; instrukcja kontenera nie oznacza, że przetestowano każdą platformę.
