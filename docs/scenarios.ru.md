# Контракт сценария v1

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

Авторитетный валидатор — `src/ha_scenario_tests/schema.py`. Принимается только JSON размером не более 64 KiB. Неизвестные и повторяющиеся ключи JSON, входные файлы-симлинки, неконечные числа и неверные типы отклоняются. Не копируйте домашнюю конфигурацию в публичные примеры.

Обязательные корневые поля: `schema: "ha-scenario/v1"`, короткое имя `name` в нижнем регистре, `seed`, `automations`, `timeline`, `expect`. Необязательное `settle_seconds` по умолчанию равно 0.1. Все ID сущностей используют префикс `scenario_` и должны быть объявлены в seed. Поддерживаемые домены: `light`, `switch`, `input_boolean`, `binary_sensor`. Поддерживаемые состояния: `on`, `off`, `unknown`, `unavailable`.

Автоматизация содержит `id`, `triggers`, `actions`, необязательные `conditions` и `mode` (`single` или `restart`). Триггеры состояния требуют `trigger`, `entity_id`, `to`; поля `from` и `for_seconds` необязательны. Триггеры событий используют `trigger: "event"` и `event_type: "scenario_name"`; также поддерживается `automation_reloaded`. Условия допускают только сравнение состояний. Действие содержит `action` и один `entity_id`: разрешены `turn_on`, `turn_off`, `toggle` для объявленных в seed сущностей light/switch/input_boolean. Шаблоны, селекторы, действия устройств, blueprints, скрипты с диска и данные сервисов не допускаются.

Шаг шкалы времени содержит `after` (относительное число секунд после завершения предыдущего шага) и ровно одну операцию:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Другие операции: `"event": "scenario_manual_off"` или `"reload": true`. Reload вызывает настоящий сервис автоматизаций HA, читающий сгенерированный временный `configuration.yaml`; тест не имитирует перезагрузку отправкой события её завершения.

`expect.calls` — точный упорядоченный список записей `{action, entity_id}`, включая повторы; пустой список запрещает все вызовы исполнительных устройств. Необязательное `expect.forbidden` перечисляет вызовы, которые не должны происходить. `expect.states` сопоставляет объявленные в seed ID с конечными состояниями. Неожиданные вызовы приводят к ошибке, даже если итоговое состояние случайно совпало.

Ограничения: 64 сущности seed, 16 автоматизаций, по 8 триггеров и 8 условий на автоматизацию, 16 действий на автоматизацию, 32 шага шкалы времени, 5 секунд суммарных запрошенных ожиданий, 256 записанных вызовов. Ошибки фоновых задач и заблокированный ввод-вывод приводят к провалу запуска. Отчёт содержит монотонное время вызовов и шагов, загруженные компоненты, конечные состояния и коды ошибок.

Родитель проверяет весь отчёт worker перед возвратом. `passed` должен быть настоящим логическим значением, `physical_validation` должен быть false, а схема, версия HA, имя сценария, поля и границы — соответствовать протоколу. Родитель также проверяет утверждения о вызовах и состояниях по сценарию, а не доверяет флагу успеха. Неверный вывод и любой ненулевой код завершения worker считаются ошибками выполнения, даже если дочерний процесс напечатал JSON, похожий на успешный результат.

Пример stale обозначает потерю транспорта состоянием `unavailable`. Он не выводит актуальность источника из `last_changed`, не проверяет разбор временных меток датчика и не доказывает реальное истечение срока актуальности датчика. Ручное переопределение — явно заданная синтетическая политика; инструмент не добавляет её в существующую автоматизацию.
