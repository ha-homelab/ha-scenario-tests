# Instalacja i ograniczenie środowiska

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

Użyj przypiętego środowiska Home Assistant z Pythonem 3.14.2–3.14.x. Zainstaluj `requirements.lock` z `--require-hashes`, a następnie ten pakiet przy użyciu `--no-deps .`, zgodnie z głównym README. Plik blokady obejmuje zależności aplikacji i testów. Wymagane jest czyste środowisko; nie instaluj w produkcyjnym środowisku Home Assistant. Podczas edycji źródeł użyj zamiast tego `pip install --no-deps -e .`.

Najpierw uruchom `ha-scenario validate examples/stale_sensor.json`. Walidacja nie importuje środowiska HA. Następnie uruchom `ha-scenario run examples/stale_sensor.json --report result.json`. Nie konfiguruje się serwera docelowego. Jedyna ścieżka wyjściowa pochodzi z jawnego argumentu `--report`, nie ze scenariusza.

Dla silniejszej izolacji sieciowej:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Budowanie wymaga dostępu do Internetu w celu pobrania zależności. Uruchomienie nie ma sieci i korzysta z jednorazowego zapisywalnego `/tmp`; nie montuje konfiguracji domowej, gniazda Docker ani danych uwierzytelniających. To opcjonalna instrukcja wdrożenia; sprawdź w protokole walidacji, czy wykonano dokładnie ten kontener. Nie dodawaj sieci hosta ani montowań produkcyjnych.

Interfejs podprocesu usuwa odziedziczone dane uwierzytelniające i `PYTHONPATH`. Worker z `-I` używa zainstalowanego pakietu. Dziedziczone są tylko PATH, SYSTEMROOT i LANG; ziarno haszowania jest stałe. W Linuksie ścieżka bibliotek workera wynika z `LIBDIR` uruchomionej instalacji Pythona, dzięki czemu przenośne kompilacje Pythona mogą znaleźć libpython. Odziedziczony `LD_LIBRARY_PATH` nigdy nie jest kopiowany. Proces potomny ma limit rodzica 30 sekund, limit wewnętrzny 20 sekund, najwyżej 5 sekund żądanych oczekiwań na osi czasu i 256 przechwyconych akcji. Zawieszone zależności natywne kończy limit czasu rodzica.

Wtyczka pytest instaluje się automatycznie. Test może wczytać scenariusz przez `ha_scenario_tests.schema.load` i wywołać fixture `scenario_runner`. JUnit generuje sam pytest. `run_scenario` można też importować w zwykłym kodzie Pythona.
