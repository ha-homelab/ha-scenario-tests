# Протокол проверки

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

## 2026-10-15: проверка выполнения в Linux

[Запуск GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) успешно завершился на коммите `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` с CPython 3.14.8 в Ubuntu и закреплённым Home Assistant 2026.10.0. Полная команда `python3 -m pytest -q` завершилась с результатом **54 теста пройдено за 21.42 с**, без пропусков. Включены все семь тестов с настоящим HA: четыре примера сценариев, случай с намеренно неверным ожиданием и запрещённым действием, JSON-отчёт локализованного CLI и контракт передачи роли для зависимого проекта. Каждый тест запускает новый контролируемый worker; проверки ожидаемого провала тестируются как провалы, а не выдаются за успешные сценарии.

В том же запуске прошли Ruff, проверки ссылок и SVG документации, сборки исходного пакета и wheel, политика публикации исходников и сканирование всей истории на секреты. Это подтверждает синтетическую диспетчеризацию сервисов и поведение состояний под описанной защитой ввода-вывода Python. Это не подтверждает песочницу уровня ОС, выполнение Docker-контейнера или физическое поведение устройств.

## 2026-10-15: локальные проверки разработки в macOS

Исходники, строгая проверка входных данных, audit-защита Python, переводы CLI и повторная генерация SVG проверялись локально с Python 3.14.7 в macOS arm64. Команда `python -m pytest -q -m 'not runtime'` прошла **47 тестов**; семь случаев с настоящим HA явно исключены этой командой. Команда `python -m ruff check src tests scripts` прошла. Это не замена полному набору тестов выполнения.

Настоящий движок Home Assistant 2026.10.0 загрузил `automation`, `blueprint` и `trace` и выполнил сценарии таймаута присутствия и ручного переопределения с ожидаемыми синтетическими вызовами сервисов, конечными состояниями и без заблокированного ввода-вывода. Затем локальный процесс Python завершился нативной ошибкой сегментации при завершении интерпретатора. Родительский runner корректно считает этот ненулевой код ошибкой выполнения, даже если перед ним был успешный JSON. **Полное успешное прохождение теста выполнения в macOS не заявляется.**

Для принятия выпуска необходим полный набор Linux CI. Выполните `python -m pytest -q --junitxml=junit.xml`; отсутствие HA, неверная версия HA, таймауты и ненулевые коды дочерних процессов приводят к провалу, а не к скрытому пропуску. Запуск по ссылке выше — доказательство для этой реализации в Linux; последующим изменениям нужен собственный успешный запуск. Этот протокол не заявляет выполнения Docker или проверки физических устройств.

## Контролируемые метаданные начальной загрузки

Worker задаёт синтетическое значение `synthetic` для кэшированных метаданных процессора Python и отключает `socket.has_ipv6` перед импортом HA. Это не даёт инициализации платформы HA запускать `uname -p` и предотвращает пробное открытие локального IPv6-сокета при импорте urllib3. В Linux ifaddr импортируется под защитой с использованием `ctypes.CDLL(None)`, разрешающего символы libc, уже загруженной в процесс; это позволяет избежать подпроцесса `ldconfig`, вызываемого поиском библиотеки. Обычный механизм поиска библиотек сразу восстанавливается. В защите ввода-вывода нет исключений для этих операций. Изменения затрагивают только метаданные и пробы хоста; триггеры, условия, таймеры, reload, скрипты и диспетчеризация сервисов HA настоящие. Эти изменения зависят от версий и покрываются закреплённым набором тестов выполнения.

## Воспроизведение

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Ни один отчёт не доказывает реальное состояние реле, доставку по радио, точность определения присутствия дома или работу на производственных длительностях. Шкала времени SVG показывает синтетические ожидания, а не замеры производительности.

В набор тестов выполнения также входит `tests/fixtures/role_transfer.json` — синтетический контракт зависимого проекта: текущая роль выключается, а выведенная из роли розетка остаётся включённой. Это не тест физического переноса нагрузки.
