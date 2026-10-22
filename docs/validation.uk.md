# Протокол перевірки

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

## 2026-10-15: перевірка виконання в Linux

[Запуск GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) успішно завершився на коміті `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` із CPython 3.14.8 в Ubuntu та Home Assistant, закріпленим на 2026.10.0. Повна команда `python3 -m pytest -q` завершилася результатом **54 тести пройдено за 21.42 с**, без пропущених тестів. Це охоплює всі сім тестів зі справжнім HA: чотири приклади сценаріїв, випадок із навмисно хибним очікуванням і забороненою дією, JSON-звіт локалізованого CLI та контракт передавання ролі для залежного проєкту. Кожен тест виконання запускає новий контрольований worker; твердження з очікуваною помилкою перевіряються як помилки, а не подаються як успішні сценарії.

У тому самому запуску також пройшли Ruff, перевірки посилань документації та SVG, збирання вихідного пакета й wheel, політика публікації джерел та сканування всієї історії на секрети. Це перевіряє синтетичну диспетчеризацію сервісів і поведінку станів під задокументованим захистом вводу-виводу Python. Це не підтверджує пісочницю рівня ОС, виконання Docker чи фізичну поведінку пристроїв.

## 2026-10-15: локальні перевірки розробки в macOS

Джерела, суворий допуск входу, захист аудиту Python, переклади CLI та повторну генерацію SVG перевірено локально з Python 3.14.7 у macOS arm64. `python -m pytest -q -m 'not runtime'` пройшла **47 тестів**; сім випадків зі справжнім HA ця команда явно виключає. `python -m ruff check src tests scripts` пройшла. Це не заміна повному набору тестів виконання.

Справжній рушій Home Assistant 2026.10.0 завантажив `automation`, `blueprint` і `trace` та виконав сценарії тайм-ауту присутності й ручного перевизначення з очікуваними синтетичними викликами сервісів, кінцевими станами й без заблокованого вводу-виводу. Потім локальний процес Python завершився нативною помилкою сегментації під час завершення інтерпретатора. Батьківський runner правильно вважає цей ненульовий код помилкою виконання, навіть якщо перед ним був успішний JSON. **Повного успішного тесту виконання в macOS не заявлено.**

Перед прийняттям випуску потрібен повний набір Linux CI. Виконайте `python -m pytest -q --junitxml=junit.xml`; відсутність HA, неправильні версії HA, тайм-аути й ненульові коди дочірніх процесів спричиняють помилки, а не приховані пропуски. Наведений вище запуск — доказ для цієї реалізації в Linux; подальші зміни вимагають власного успішного запуску. Цей протокол не заявляє виконання Docker чи перевірки фізичного пристрою.

## Контрольовані метадані початкового завантаження

Worker задає синтетичне значення `synthetic` для кешованих метаданих процесора Python і вимикає `socket.has_ipv6` перед імпортом HA. Це не дозволяє ініціалізації платформи HA запускати `uname -p` і запобігає пробному відкриттю локального IPv6-сокета під час імпорту urllib3. У Linux ifaddr імпортується під захистом із використанням `ctypes.CDLL(None)`, яка знаходить символи вже завантаженої в процес libc; це дозволяє уникнути підпроцесу `ldconfig` пошуку бібліотек. Звичайний пошук бібліотек негайно відновлюється. Захист вводу-виводу не має винятків у списку дозволених для цих операцій. Зміни стосуються лише метаданих і проб хоста; тригери, умови, таймери, reload, скрипти й диспетчеризація сервісів HA справжні. Вони залежать від версій і покриваються закріпленим набором тестів виконання.

## Відтворення

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Жоден звіт не доводить справжній стан реле, доставлення радіоканалом, точність визначення присутності вдома або роботу на виробничих тривалостях. Часова шкала SVG показує синтетичні очікування, а не вимірювання продуктивності.

Набір тестів виконання також містить `tests/fixtures/role_transfer.json` — синтетичний контракт залежного проєкту: поточна роль вимикається, а розетка, виведена з ролі, залишається увімкненою. Це не тест фізичного передавання навантаження.
