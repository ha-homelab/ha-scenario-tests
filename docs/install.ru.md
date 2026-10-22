# Установка и ограничение среды

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

Используйте закреплённую версию среды Home Assistant с Python 3.14.2–3.14.x. Установите `requirements.lock` с параметром `--require-hashes`, затем установите пакет с `--no-deps .`, как показано в корневом README. Lock-файл охватывает зависимости приложения и тестов. Требуется чистая среда; не устанавливайте пакет в рабочую среду Home Assistant. При редактировании исходников вместо этого используйте `pip install --no-deps -e .`.

Сначала выполните `ha-scenario validate examples/stale_sensor.json`. Валидация не импортирует среду HA. Затем запустите `ha-scenario run examples/stale_sensor.json --report result.json`. Целевой сервер не настраивается. Единственный путь вывода берётся из явно переданного аргумента `--report`, а не из сценария.

Для более строгого сетевого ограничения:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Сборке нужен интернет для получения зависимостей. При запуске сети нет, а записываемый `/tmp` одноразовый; домашняя конфигурация, сокет Docker и учётные данные не монтируются. Это необязательный рецепт развёртывания; сведения о том, запускался ли именно этот контейнер, смотрите в протоколе проверки. Не добавляйте сеть хоста или монтирование рабочих данных.

Интерфейс подпроцесса удаляет унаследованные учётные данные и `PYTHONPATH`. Worker с `-I` использует установленный пакет. Наследуются только PATH, SYSTEMROOT и LANG; seed хеширования фиксирован. В Linux путь к библиотеке worker определяется по `LIBDIR` используемой установки Python, чтобы переносимые сборки Python могли найти libpython. Унаследованный `LD_LIBRARY_PATH` никогда не копируется. Родитель ограничивает дочерний процесс 30 секундами, внутренний таймаут составляет 20 секунд, суммарные запрошенные ожидания шкалы времени — не более 5 секунд, число записанных действий — 256. Зависания нативных зависимостей прерываются родительским таймаутом.

Плагин pytest устанавливается автоматически. Тест может загрузить сценарий через `ha_scenario_tests.schema.load` и вызвать фикстуру `scenario_runner`. JUnit формирует сам pytest. `run_scenario` также можно импортировать в обычный Python-код.
