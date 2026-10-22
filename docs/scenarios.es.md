# Contrato de escenario v1

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

El validador de referencia es `src/ha_scenario_tests/schema.py`. Solo JSON, con un máximo de 64 KiB. Se rechazan claves desconocidas o duplicadas, entradas mediante enlaces simbólicos, números no finitos y tipos incorrectos. No copies configuración doméstica en ejemplos públicos.

Campos raíz obligatorios: `schema: "ha-scenario/v1"`, un `name` corto en minúsculas, `seed`, `automations`, `timeline`, `expect`. El campo opcional `settle_seconds` vale 0.1 por defecto. Todos los ID de entidad usan el prefijo `scenario_` y deben declararse en el seed. Dominios admitidos: `light`, `switch`, `input_boolean`, `binary_sensor`. Estados admitidos: `on`, `off`, `unknown`, `unavailable`.

Una automatización tiene `id`, `triggers`, `actions`, y opcionalmente `conditions` y `mode` (`single` o `restart`). Los disparadores de estado requieren `trigger`, `entity_id`, `to`; `from` y `for_seconds` son opcionales. Los disparadores de eventos usan `trigger: "event"` y `event_type: "scenario_name"`; también se admite `automation_reloaded`. Las condiciones solo comparan estados. Las acciones contienen `action` y un único `entity_id`: se admiten `turn_on`, `turn_off`, `toggle` sobre entidades light/switch/input_boolean del seed. No se admiten plantillas, selectores, acciones de dispositivos, blueprints, scripts del disco ni datos de servicio.

Los pasos de la cronología contienen `after` (segundos relativos desde la finalización del paso anterior) y exactamente una operación:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Otras operaciones: `"event": "scenario_manual_off"` o `"reload": true`. La recarga llama al servicio real de automatizaciones de HA, que lee el `configuration.yaml` temporal generado; la prueba no imita una recarga lanzando su evento de finalización.

`expect.calls` es la lista ordenada exacta de registros `{action, entity_id}`, incluidas las repeticiones; una lista vacía prohíbe todas las llamadas a actuadores. `expect.forbidden` enumera opcionalmente llamadas que nunca deben suceder. `expect.states` asigna estados finales a los ID del seed. Las llamadas inesperadas provocan un fallo aunque el estado final coincida por casualidad.

Límites: 64 entidades en el seed, 16 automatizaciones, 8 disparadores y 8 condiciones por automatización, 16 acciones por automatización, 32 pasos de cronología, 5 segundos totales de esperas solicitadas y 256 llamadas capturadas. Los errores de tareas en segundo plano y la E/S bloqueada hacen fallar la ejecución. El informe incluye los tiempos monótonos transcurridos de llamadas y pasos, los componentes cargados, los estados finales y los códigos de fallo.

El padre valida el informe completo del worker antes de devolverlo. `passed` debe ser un booleano real, `physical_validation` debe ser false, y el esquema, la versión de HA, el nombre del escenario, los campos y los límites deben ajustarse al protocolo. El padre comprueba también las aserciones de llamadas y estados frente al escenario, en lugar de confiar en un indicador de éxito. Una salida inválida y cualquier código de salida no nulo del worker son errores de ejecución, aunque el hijo haya impreso un objeto JSON con apariencia de éxito.

El ejemplo stale incluido representa la pérdida de transporte mediante `unavailable`. No deduce la vigencia del origen a partir de `last_changed`, no prueba el análisis de marcas temporales del sensor ni demuestra su caducidad real. La anulación manual es una política sintética explícita; la herramienta no la añade a una automatización existente.
