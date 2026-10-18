# HA Scenario Tests

[English](README.md) · [Русский](README.ru.md) · [Deutsch](README.de.md)

Ejecuta escenarios sintéticos limitados en el **motor real de automatizaciones y scripts de Home Assistant 2026.10.1**. Comprueba el orden exacto de acciones, las acciones prohibidas y los estados finales. No acepta direcciones, tokens ni configuraciones de una instalación real de HA.

Antes de usarlo, consulte el [registro de validación](docs/validation.md): las pruebas completas son un requisito de publicación; allí se documenta un fallo nativo local al finalizar el proceso.

## Instalación

Se requiere Python 3.14.2–3.14.x. La instalación descarga dependencias; la ejecución no necesita red.

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/ha-scenario --lang es validate examples/presence_timeout.json
.venv/bin/ha-scenario --lang es run examples/manual_override.json --report result.json
.venv/bin/python -m pytest -q --junitxml=junit.xml
```

Códigos de salida: 0 correcto, 1 expectativa incumplida, 2 entrada o entorno incorrecto. Los informes no sobrescriben archivos existentes. Las claves JSON son independientes del idioma; la ayuda y los resultados están traducidos.

## Alcance

Hay cuatro ejemplos completos: presencia, bloqueo manual, pérdida del sensor y recarga real mediante `automation.reload`. Cada ejecución usa un proceso Python nuevo y un directorio HA temporal. Los actuadores sintéticos registran las llamadas y actualizan estados de prueba. Un guardián de auditoría bloquea operaciones de red y subprocesos, pero no es una sandbox del sistema operativo. El contenedor con `--network none` añade una frontera de red.

No hay reloj virtual, importación de YAML arbitrario ni validación física. Un temporizador de prueba de 120 ms no demuestra el funcionamiento de uno real de 20 minutos. La fixture pytest `scenario_runner` devuelve un informe compatible con JSON.

![Cronología sintética](docs/images/timeline.svg)

Documentación ampliada en inglés y ruso: [instalación](docs/install.md), [formato](docs/scenarios.md), [diagnóstico](docs/troubleshooting.md), [limitaciones](docs/limits.md), [wiki](wiki/Home.md). Licencia MIT. Todos los dispositivos y datos de ejemplo son ficticios.
