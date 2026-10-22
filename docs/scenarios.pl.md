# Kontrakt scenariusza v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="scenarios.md" lang="en" dir="ltr">English</a> ·
<a href="scenarios.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="scenarios.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="scenarios.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="scenarios.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="scenarios.es.md" lang="es" dir="ltr">Español</a> ·
<a href="scenarios.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="scenarios.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="scenarios.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="scenarios.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="scenarios.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="scenarios.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="scenarios.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="scenarios.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="scenarios.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="scenarios.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="scenarios.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="scenarios.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="scenarios.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="scenarios.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="scenarios.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="scenarios.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="scenarios.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="scenarios.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

Wiążącym walidatorem jest `src/ha_scenario_tests/schema.py`. Tylko JSON, najwyżej 64 KiB. Nieznane klucze, powtórzone klucze JSON, dowiązania symboliczne jako wejście, liczby nieskończone lub NaN oraz nieprawidłowe typy są odrzucane. Nie kopiuj konfiguracji domowej do publicznych przykładów.

Wymagane pola główne: `schema: "ha-scenario/v1"`, krótka nazwa `name` małymi literami, `seed`, `automations`, `timeline`, `expect`. Opcjonalne `settle_seconds` ma domyślną wartość 0.1. Wszystkie ID encji używają prefiksu `scenario_` i muszą być zadeklarowane w seed. Obsługiwane domeny: `light`, `switch`, `input_boolean`, `binary_sensor`. Obsługiwane stany: `on`, `off`, `unknown`, `unavailable`.

Automatyzacja ma `id`, `triggers`, `actions` oraz opcjonalnie `conditions` i `mode` (`single` lub `restart`). Wyzwalacze stanu wymagają `trigger`, `entity_id`, `to`; opcjonalne są `from` i `for_seconds`. Wyzwalacze zdarzeń używają `trigger: "event"` oraz `event_type: "scenario_name"`; obsługiwane jest także `automation_reloaded`. Warunki mogą jedynie porównywać stany. Akcje zawierają `action` i jedno `entity_id`: `turn_on`, `turn_off`, `toggle` dla encji light/switch/input_boolean zadeklarowanych w seed. Szablony, selektory, akcje urządzeń, blueprinty, skrypty z dysku i dane usług nie są dopuszczone.

Kroki osi czasu zawierają `after` (sekundy względne od zakończenia poprzedniego kroku) i dokładnie jedną operację:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Inne operacje: `"event": "scenario_manual_off"` lub `"reload": true`. Przeładowanie wywołuje prawdziwą usługę automatyzacji HA, która odczytuje wygenerowany tymczasowy `configuration.yaml`; test nie imituje przeładowania przez wysłanie zdarzenia jego zakończenia.

`expect.calls` to dokładna uporządkowana lista rekordów `{action, entity_id}`, łącznie z powtórzeniami; pusta lista zabrania wszystkich wywołań wykonawczych. `expect.forbidden` opcjonalnie wymienia wywołania, które nigdy nie mogą wystąpić. `expect.states` mapuje ID z seed na stany końcowe. Nieoczekiwane wywołania powodują błąd, nawet jeśli stan końcowy przypadkiem się zgadza.

Limity: 64 encje seed, 16 automatyzacji, 8 wyzwalaczy i 8 warunków na automatyzację, 16 akcji na automatyzację, 32 kroki osi czasu, 5 sekund łącznego żądanego oczekiwania, 256 przechwyconych wywołań. Błędy zadań w tle i zablokowane I/O powodują niepowodzenie wykonania. Raport zawiera monotoniczne czasy upływu dla wywołań i kroków, załadowane komponenty, stany końcowe i kody błędów.

Rodzic weryfikuje cały raport workera przed jego zwróceniem. `passed` musi być rzeczywistą wartością typu boolean, `physical_validation` musi mieć wartość false, a schemat, wersja HA, nazwa scenariusza, pola i granice muszą odpowiadać protokołowi. Rodzic sprawdza też asercje wywołań i stanów względem scenariusza, zamiast ufać fladze sukcesu. Nieprawidłowe wyjście i każdy niezerowy kod zakończenia workera to błędy wykonania, nawet jeśli potomek wypisał obiekt JSON wyglądający na sukces.

Dołączony przykład stale reprezentuje utratę transportu przez `unavailable`. Nie wyznacza aktualności źródła na podstawie `last_changed`, nie testuje parsowania znaczników czasu czujnika ani nie dowodzi rzeczywistego wygasania danych czujnika. Ręczne nadpisanie jest jawną polityką syntetyczną; narzędzie nie dodaje jej do istniejącej automatyzacji.
