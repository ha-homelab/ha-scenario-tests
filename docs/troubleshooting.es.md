# Resolución de problemas

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

- Salida 2 durante la instalación o ejecución: comprueba Python 3.14.2–3.14.x, la versión exacta fijada de HA y un entorno virtual limpio. El runner rechaza otras versiones de HA. Reinstala el archivo de bloqueo antes de comunicar el fallo.
- Fallo o tiempo agotado del worker: falló una importación de dependencias o la inicialización de HA. Ejecuta directamente el worker aislado con un archivo **sintético** para obtener una traza local: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. No publiques diagnósticos del entorno sin revisar.
- `calls_mismatch`: compara el orden y las llamadas duplicadas, no solo el estado final. Los estados del seed se establecen antes del arranque; no cuentan automáticamente como un nuevo disparador de estado después del arranque.
- `forbidden_call`: una orden capturada de un actuador sintético coincidió con el contrato negativo. Es un despacho real de automatización, no una actuación física.
- `states_mismatch`: una asignación en la cronología o un actuador sintético dejó un estado diferente.
- `blocked_io` o `background_exception`: nunca desactives la protección para obtener un resultado verde. Esta versión no admite integraciones de red. Comunica la reproducción sintética y la versión.
- Pruebas de temporización inestables: aumenta la separación entre la transición de estado y el plazo comprobado. Se mide la planificación real del bucle de eventos; no se promete un reloj virtual ni planificación exacta al microsegundo.
- Recarga: los temporizadores `for` pueden cancelarse por la recarga real. Hace falta una automatización de reconciliación explícita si la política exige recuperación; compara `reload_reconcile.json`.
- Informe existente: `--report` se niega deliberadamente a sobrescribirlo. Elige una ruta nueva.

Si usas el árbol fuente tras una instalación no editable, reinstala el paquete antes de probar cambios. Para desarrollo, instala con `--no-deps -e .`.
