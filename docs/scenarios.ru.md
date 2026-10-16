# Контракт сценария v1

Авторитетный валидатор — `src/ha_scenario_tests/schema.py`. Только JSON, максимум 64 КиБ. Неизвестные поля, повторяющиеся JSON-ключи, symlink, нечисловые бесконечности и неверные типы отклоняются.

Обязательные поля: `schema: "ha-scenario/v1"`, короткое имя `name` в нижнем регистре, `seed`, `automations`, `timeline`, `expect`. Необязательный `settle_seconds` по умолчанию 0.1. Все entity IDs имеют префикс `scenario_` и объявляются в seed. Домены: light, switch, input_boolean, binary_sensor. Состояния: on, off, unknown, unavailable.

Автоматизация содержит `id`, `triggers`, `actions`, необязательные `conditions` и `mode` (single/restart). State trigger задаёт entity_id и to, опционально from и for_seconds. Event trigger принимает событие scenario_* или automation_reloaded. Условия — только сравнение состояния. Действия — turn_on/turn_off/toggle для одной объявленной light/switch/input_boolean. Шаблоны, selectors, device actions, blueprints и внешние скрипты не допускаются.

Шаг timeline: относительная пауза `after` и ровно одна операция:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Другие операции: `"event": "scenario_manual_off"` или `"reload": true`. Reload вызывает настоящий сервис HA, читающий созданный временный configuration.yaml. Событие завершения не подделывается.

`expect.calls` — точный упорядоченный список `{action, entity_id}`, включая повторы. Пустой список запрещает все команды. `expect.forbidden` явно перечисляет недопустимые команды, `expect.states` — итоговые состояния. Лишняя команда нарушает тест даже при правильном итоге.

Лимиты: 64 сущности, 16 автоматизаций, 8 триггеров и условий, 16 действий на автоматизацию, 32 шага, 5 секунд суммарных пауз, 256 команд. Ошибки фоновых задач и попытки I/O нарушают тест. Отчёт содержит фактическое монотонное время команд и шагов, компоненты, состояния и коды ошибок.

Stale-пример задаёт unavailable, но не проверяет timestamp реального датчика. Ручной override описан в самом синтетическом правиле: инструмент не исправляет вашу автоматизацию автоматически.
