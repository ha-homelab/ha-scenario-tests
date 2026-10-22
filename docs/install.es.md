# Instalación y contención

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

Usa el entorno de ejecución de Home Assistant fijado con Python 3.14.2–3.14.x. Instala `requirements.lock` con `--require-hashes` y después este paquete con `--no-deps .`, como indica el README raíz. El archivo de bloqueo cubre las dependencias de la aplicación y las pruebas. Se requiere un entorno limpio; no instales en tu entorno de Home Assistant de producción. Si vas a editar el código, usa `pip install --no-deps -e .` en su lugar.

Ejecuta primero `ha-scenario validate examples/stale_sensor.json`. La validación no importa el entorno de HA. Después ejecuta `ha-scenario run examples/stale_sensor.json --report result.json`. No se configura un servidor de destino. La única ruta de salida procede de tu argumento explícito `--report`, no del escenario.

Para reforzar el aislamiento de red:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

La compilación necesita Internet para obtener las dependencias. La ejecución no tiene red y dispone de un `/tmp` desechable con escritura; no monta la configuración del hogar, el socket de Docker ni credenciales. Esta receta de despliegue es opcional; consulta el registro de validación para saber si se ejecutó exactamente este contenedor. No añadas red del host ni montajes de producción.

La interfaz de subprocesos elimina las credenciales heredadas y `PYTHONPATH`. El worker con `-I` usa el paquete instalado. Solo se heredan PATH, SYSTEMROOT y LANG; la semilla del hash está fijada. En Linux, la ruta de bibliotecas del worker deriva del `LIBDIR` de la instalación de Python en ejecución, lo que permite a las compilaciones reubicables encontrar libpython. Nunca se copia un `LD_LIBRARY_PATH` heredado. El proceso hijo tiene un tiempo límite del padre de 30 segundos, un límite interno de 20 segundos, un máximo de 5 segundos de esperas solicitadas en la cronología y 256 acciones capturadas. El límite del padre termina los bloqueos de dependencias nativas.

El complemento de pytest se instala automáticamente. Una prueba puede cargar un escenario con `ha_scenario_tests.schema.load` y llamar a la fixture `scenario_runner`. El propio pytest genera JUnit. También se puede importar `run_scenario` desde código Python normal.
