# Registro de validación

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

## 2026-10-15: validación del entorno de ejecución en Linux

La [ejecución de GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) pasó en el commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, con CPython 3.14.8 en Ubuntu y Home Assistant fijado a 2026.10.0. El comando completo `python3 -m pytest -q` terminó con **54 pruebas superadas en 21.42 s**, sin omitir ninguna. Incluye las siete pruebas de ejecución con HA real: cuatro escenarios de ejemplo, un caso de expectativa fallida intencionadamente y acción prohibida, el informe JSON de la CLI localizada y el contrato de transferencia de rol de un proyecto dependiente. Cada prueba de ejecución inicia un worker controlado nuevo; las aserciones de fallo esperado se prueban como fallos y no se presentan como escenarios exitosos.

También pasaron Ruff, las comprobaciones de enlaces documentales y SVG, las compilaciones de fuente y wheel, la política de publicación de fuentes y el escaneo de secretos de todo el historial. Esto valida el despacho sintético de servicios y el comportamiento de estados bajo la protección de E/S Python documentada. No establece un aislamiento de seguridad a nivel de sistema operativo, no valida una ejecución de Docker ni demuestra comportamiento físico de dispositivos.

## 2026-10-15: comprobaciones de desarrollo en macOS

El código fuente, la admisión estricta de entradas, la protección de auditoría de Python, las traducciones de CLI y la regeneración de SVG se comprobaron localmente con Python 3.14.7 en macOS arm64. `python -m pytest -q -m 'not runtime'` superó **47 pruebas**; ese comando excluye explícitamente siete casos con HA real. `python -m ruff check src tests scripts` pasó. Esto no sustituye la suite completa de ejecución.

El motor real Home Assistant 2026.10.0 cargó `automation`, `blueprint` y `trace`, y ejecutó los escenarios de tiempo de presencia y anulación manual con las llamadas sintéticas esperadas, estados finales y sin E/S bloqueada. Después el proceso Python local terminó con un fallo de segmentación nativo durante el cierre del intérprete. El runner padre trata correctamente ese código no nulo como un fallo de ejecución, incluso si antes apareció un JSON exitoso. **No se afirma que haya pasado una prueba completa de ejecución en macOS.**

La suite Linux CI completa es obligatoria antes de aceptar una versión. Ejecuta `python -m pytest -q --junitxml=junit.xml`; la ausencia de HA, versiones erróneas de HA, tiempos agotados del hijo y salidas no nulas provocan fallos, nunca omisiones silenciosas. La ejecución enlazada arriba constituye la evidencia Linux de esta implementación; los cambios posteriores requieren su propia ejecución satisfactoria. Este registro no afirma que se haya ejecutado Docker ni validado un dispositivo físico.

## Metadatos de arranque controlados

El worker proporciona el valor sintético `synthetic` a los metadatos de procesador en caché de Python y desactiva `socket.has_ipv6` antes de importar HA. Esto impide que la inicialización de plataforma de HA lance `uname -p` y evita la prueba de enlace IPv6 local durante la importación de urllib3. En Linux se importa ifaddr bajo la protección mediante `ctypes.CDLL(None)`, resolviendo símbolos de libc ya cargados en el proceso; así se evita el subproceso `ldconfig` del buscador de bibliotecas. El buscador ordinario se restaura inmediatamente. La protección de E/S no tiene excepciones de lista de permitidos para esas operaciones. Los cambios afectan solo a metadatos y sondeos del host; los disparadores, condiciones, temporizadores, recarga, scripts y despacho de servicios de HA son reales. Son sensibles a las versiones y están cubiertos por la suite de ejecución fijada.

## Reproducción

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Ningún informe demuestra el estado real de un relé, entrega por radio, precisión de presencia doméstica ni temporización con duraciones de producción. La cronología SVG muestra expectativas sintéticas, no mediciones de rendimiento.

La suite de ejecución también incluye `tests/fixtures/role_transfer.json`, el contrato sintético del proyecto dependiente: el rol actual se apaga y el enchufe retirado del rol permanece encendido. No es una prueba de transferencia física de carga.
