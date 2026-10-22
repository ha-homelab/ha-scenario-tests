# Alcance y evidencias

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

Esta versión valida un subconjunto acotado con disparadores, condiciones, temporizadores, recarga y despacho de acciones de scripts reales de Home Assistant. Los receptores de órdenes de actuadores y los estados de entrada son sintéticos. No demuestra los protocolos físicos de comunicación, el consumo eléctrico, la precisión de los sensores, el estado físico de un relé, la seguridad ni el comportamiento de cualquier configuración posible de HA.

El reloj mide tiempo monótono real transcurrido. Las pruebas usan deliberadamente intervalos cortos y margen de planificación. No modificamos los métodos internos de demora de HA, no reescribimos los tiempos de los temporizadores de producción ni afirmamos equivalencia con tiempo virtual. Los cambios de horario estacional, la planificación por reloj civil, el reinicio completo del proceso HA y la persistencia de Recorder quedan fuera de v1. Se prueba la recarga; no es un reinicio del proceso.

La entrada no contiene plantillas ejecutables ni configuración de integraciones. Cada worker usa un directorio temporal limpio, un entorno depurado y una protección global de auditoría. Esto impide E/S accidental de red o subprocesos de Python a través de la ruta admitida. No es un entorno aislado para código hostil: se confía en las dependencias Python y nativas, el intérprete y el host. Ejecuta código o dependencias no fiables solo en un entorno protegido aparte. La receta opcional de Docker sin red refuerza el aislamiento de red, pero no demuestra el comportamiento del hardware.

Los informes públicos deben contener solo fixtures sintéticas. Las cronologías reales de estados revelan ocupación y hábitos incluso sin un token. Aquí no se incluyen inventarios domésticos, grabaciones ni configuración de producción. Todos los diagramas están etiquetados como sintéticos y se reproducen con `python scripts/render_diagrams.py`.

Consulta la [validación](validation.es.md) para conocer las comprobaciones medidas realizadas sobre esta versión. La compatibilidad de instalación se limita a los entornos de ese registro; la receta del contenedor no afirma que se haya probado cada plataforma.
