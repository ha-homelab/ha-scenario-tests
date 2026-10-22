# Protokół walidacji

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

## 2026-10-15: walidacja wykonania w Linuksie

[Uruchomienie GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) przeszło na commicie `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, przy użyciu CPython 3.14.8 w Ubuntu i Home Assistant przypiętego do 2026.10.0. Pełne polecenie `python3 -m pytest -q` zakończyło się wynikiem **54 testy zaliczone w 21.42 s**, bez pominiętych testów. Obejmuje to wszystkie siedem testów z prawdziwym HA: cztery scenariusze przykładowe, celowo błędne oczekiwanie z zakazaną akcją, raport JSON zlokalizowanego CLI oraz kontrakt przekazania roli dla projektu zależnego. Każdy test uruchamia świeży kontrolowany worker; asercje oczekiwanego niepowodzenia są testowane jako niepowodzenia, a nie raportowane jako udane scenariusze.

W tym samym uruchomieniu przeszły też Ruff, kontrole odnośników dokumentacji i SVG, budowanie pakietów źródłowych i wheel, zasady publikacji źródeł oraz skanowanie całej historii w poszukiwaniu sekretów. Weryfikuje to syntetyczne wywołania usług i zachowanie stanów pod udokumentowaną ochroną I/O Pythona. Nie ustanawia piaskownicy bezpieczeństwa systemu operacyjnego, nie potwierdza wykonania Dockera i nie dowodzi fizycznego zachowania urządzeń.

## 2026-10-15: kontrole programistyczne w macOS

Źródła, ścisłe dopuszczanie wejścia, ochronę audytową Pythona, tłumaczenia CLI i regenerację SVG sprawdzono lokalnie Pythonem 3.14.7 w macOS arm64. `python -m pytest -q -m 'not runtime'` zaliczył **47 testów**; to polecenie jawnie wyklucza siedem przypadków z prawdziwym HA. `python -m ruff check src tests scripts` przeszedł. To nie zastępuje pełnego zestawu testów wykonania.

Prawdziwy silnik Home Assistant 2026.10.0 załadował `automation`, `blueprint` i `trace`, a następnie wykonał scenariusze czasu obecności i ręcznego nadpisania z oczekiwanymi syntetycznymi wywołaniami usług, stanami końcowymi i bez zablokowanego I/O. Lokalny proces Pythona zakończył się później natywnym błędem segmentacji podczas zamykania interpretera. Runner rodzica prawidłowo traktuje taki niezerowy kod jako błąd wykonania, nawet gdy poprzedził go udany JSON. **Nie deklaruje się pełnego udanego testu wykonania w macOS.**

Przed przyjęciem wydania wymagany jest pełny zestaw Linux CI. Uruchom `python -m pytest -q --junitxml=junit.xml`; brak HA, niewłaściwe wersje HA, timeouty potomków i niezerowe kody ich zakończenia powodują błędy, nigdy ciche pominięcie. Powyższy odnośnik jest dowodem linuksowym dla tej implementacji; późniejsze zmiany wymagają własnego udanego uruchomienia. Ten protokół nie deklaruje wykonania Dockera ani walidacji fizycznego urządzenia.

## Kontrolowane metadane inicjalizacji

Worker podaje wartość syntetyczną `synthetic` jako buforowane metadane procesora Pythona i wyłącza `socket.has_ipv6` przed importem HA. Zapobiega to uruchomieniu `uname -p` przez inicjalizację platformy HA oraz próbnemu powiązaniu lokalnego IPv6 podczas importu urllib3. W Linuksie ifaddr importuje się pod ochroną z użyciem `ctypes.CDLL(None)`, rozwiązując symbole libc już załadowane w procesie; pozwala to uniknąć podprocesu `ldconfig` używanego przy wyszukiwaniu biblioteki. Zwykłe wyszukiwanie biblioteki jest natychmiast przywracane. Ochrona I/O nie ma dla tych operacji wyjątków na liście dozwolonych. Zmiany wpływają tylko na metadane i sondy hosta; wyzwalacze, warunki, timery, przeładowanie, skrypty i dystrybucja usług HA są prawdziwe. Zależą od wersji i są objęte przypiętym zestawem testów wykonania.

## Odtworzenie

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Żaden raport nie dowodzi rzeczywistego stanu przekaźnika, dostarczenia przez radio, dokładności wykrywania obecności domowników ani działania przy produkcyjnych długościach czasu. Oś czasu SVG pokazuje oczekiwania syntetyczne, nie pomiary wydajności.

Zestaw testów wykonania obejmuje też `tests/fixtures/role_transfer.json`, syntetyczny kontrakt projektu zależnego: aktualna rola wyłącza się, a gniazdko wycofane z tej roli pozostaje włączone. To nie test fizycznego przenoszenia obciążenia.
