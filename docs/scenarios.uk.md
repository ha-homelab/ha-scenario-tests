# Контракт сценарію v1

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

Основний валідатор — `src/ha_scenario_tests/schema.py`. Лише JSON, не більш як 64 KiB. Невідомі й повторювані ключі JSON, вхідні символьні посилання, нескінченні числа та NaN, а також неправильні типи відхиляються. Не копіюйте домашню конфігурацію до публічних прикладів.

Обов’язкові кореневі поля: `schema: "ha-scenario/v1"`, коротке `name` малими літерами, `seed`, `automations`, `timeline`, `expect`. Необов’язкове `settle_seconds` типово дорівнює 0.1. Усі ID сутностей використовують префікс `scenario_` і мають бути оголошені в seed. Підтримувані домени: `light`, `switch`, `input_boolean`, `binary_sensor`. Підтримувані стани: `on`, `off`, `unknown`, `unavailable`.

Автоматизація містить `id`, `triggers`, `actions`, необов’язкові `conditions` і `mode` (`single` або `restart`). Тригери стану вимагають `trigger`, `entity_id`, `to`; `from` і `for_seconds` необов’язкові. Тригери подій використовують `trigger: "event"` і `event_type: "scenario_name"`; також підтримується `automation_reloaded`. Умови допускають лише порівняння станів. Дії містять `action` і один `entity_id`: дозволені `turn_on`, `turn_off`, `toggle` для оголошених у seed сутностей light/switch/input_boolean. Шаблони, селектори, дії пристроїв, blueprints, скрипти з диска та дані сервісів не допускаються.

Кроки часової шкали містять `after` (відносні секунди від завершення попереднього кроку) і рівно одну операцію:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Інші операції: `"event": "scenario_manual_off"` або `"reload": true`. Reload викликає справжній сервіс автоматизацій HA, який читає створений тимчасовий `configuration.yaml`; тест не імітує перезавантаження надсиланням події його завершення.

`expect.calls` — точний впорядкований список записів `{action, entity_id}`, включно з повторами; порожній список забороняє всі виклики виконавчих пристроїв. Необов’язкове `expect.forbidden` перелічує виклики, які ніколи не повинні відбутися. `expect.states` зіставляє оголошені в seed ID з кінцевими станами. Неочікувані виклики спричиняють помилку, навіть якщо кінцевий стан випадково збігається.

Обмеження: 64 сутності seed, 16 автоматизацій, по 8 тригерів і 8 умов на автоматизацію, 16 дій на автоматизацію, 32 кроки часової шкали, 5 секунд загального запитаного очікування, 256 записаних викликів. Помилки фонових завдань і заблокований ввід-вивід спричиняють невдале виконання. Звіт містить монотонні минулі часи викликів і кроків, завантажені компоненти, кінцеві стани та коди помилок.

Батьківський процес перевіряє весь звіт worker перед поверненням. `passed` має бути справжнім булевим значенням, `physical_validation` має дорівнювати false, а схема, версія HA, назва сценарію, поля й межі — відповідати протоколу. Батьківський процес також звіряє твердження про виклики й стани зі сценарієм, а не довіряє прапорцю успіху. Неправильний вивід і будь-який ненульовий код завершення worker є помилками виконання, навіть якщо дочірній процес надрукував JSON, схожий на успішний результат.

Наданий приклад stale позначає втрату транспорту через `unavailable`. Він не визначає актуальність джерела за `last_changed`, не перевіряє розбір часових міток датчика й не доводить його справжнє протермінування. Ручне перевизначення — явно задана синтетична політика; інструмент не додає її до наявної автоматизації.
