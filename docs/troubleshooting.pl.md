# Rozwiązywanie problemów

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

- Kod zakończenia 2 podczas instalacji lub uruchomienia: sprawdź Python 3.14.2–3.14.x, dokładną przypiętą wersję HA i czyste środowisko wirtualne. Runner odrzuca inne wersje HA. Przed zgłoszeniem błędu przeinstaluj zależności z pliku blokady.
- Błąd lub przekroczenie czasu workera: nie powiódł się import zależności lub inicjalizacja HA. Uruchom izolowany worker bezpośrednio z **syntetycznym** plikiem, aby uzyskać lokalny traceback: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Nie publikuj niesprawdzonej diagnostyki środowiska.
- `calls_mismatch`: porównaj kolejność i powtórzone wywołania, nie tylko stan końcowy. Stany seed ustawia się przed uruchomieniem; nie liczą się automatycznie jako nowy wyzwalacz stanu po uruchomieniu.
- `forbidden_call`: przechwycone syntetyczne polecenie wykonawcze pasowało do negatywnego kontraktu. To rzeczywista dystrybucja automatyzacji, nie fizyczne zadziałanie.
- `states_mismatch`: przypisanie na osi czasu lub syntetyczny element wykonawczy pozostawił inny stan.
- `blocked_io` lub `background_exception`: nigdy nie wyłączaj ochrony, aby uzyskać zielony wynik. Ta wersja nie dopuszcza integracji sieciowych. Zgłoś syntetyczny przykład odtworzenia i wersję.
- Niestabilne testy timerów: zwiększ odstęp między zmianą stanu a sprawdzanym terminem. Mierzone jest rzeczywiste planowanie pętli zdarzeń; nie ma obietnicy zegara wirtualnego ani dokładności planowania do mikrosekundy.
- Przeładowanie: timery `for` mogą zostać anulowane przez prawdziwe przeładowanie. Gdy polityka wymaga odzyskania stanu, potrzebna jest jawna automatyzacja uzgadniająca; porównaj `reload_reconcile.json`.
- Istniejący raport: `--report` celowo odmawia nadpisania. Wybierz nową ścieżkę.

Jeśli korzystasz z drzewa źródeł po instalacji nieedytowalnej, przeinstaluj pakiet przed testowaniem zmian. Do pracy programistycznej instaluj z `--no-deps -e .`.
