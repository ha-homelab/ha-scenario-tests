# Встановлення й обмеження середовища

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

Використовуйте закріплену версію середовища Home Assistant із Python 3.14.2–3.14.x. Установіть `requirements.lock` із `--require-hashes`, а потім цей пакет із `--no-deps .`, як показано в кореневому README. Файл фіксації охоплює залежності застосунку й тестів. Потрібне чисте середовище; не встановлюйте пакет у робоче середовище Home Assistant. Для редагування вихідного коду натомість використовуйте `pip install --no-deps -e .`.

Спочатку виконайте `ha-scenario validate examples/stale_sensor.json`. Перевірка не імпортує середовище HA. Потім виконайте `ha-scenario run examples/stale_sensor.json --report result.json`. Цільовий сервер не налаштовується. Єдиний шлях виводу береться з явно переданого аргументу `--report`, а не зі сценарію.

Для сильнішого мережевого обмеження:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Збиранню потрібен доступ до інтернету для залежностей. Під час виконання мережі немає, а записуваний `/tmp` одноразовий; домашня конфігурація, сокет Docker та облікові дані не монтуються. Це необов’язковий спосіб розгортання; чи запускався саме цей контейнер, дивіться у протоколі перевірки. Не додавайте мережу хоста або монтування робочих даних.

Інтерфейс підпроцесу видаляє успадковані облікові дані та `PYTHONPATH`. Worker з `-I` використовує встановлений пакет. Успадковуються лише PATH, SYSTEMROOT і LANG; початкове значення хешування фіксоване. У Linux шлях до бібліотеки worker визначається через `LIBDIR` активної інсталяції Python, що дозволяє переносним збіркам Python знаходити libpython. Успадкований `LD_LIBRARY_PATH` ніколи не копіюється. Дочірній процес має батьківський тайм-аут 30 секунд, внутрішній тайм-аут 20 секунд, не більш як 5 секунд запитаних очікувань часової шкали та 256 записаних дій. Зависання нативних залежностей перериває батьківський тайм-аут.

Плагін pytest встановлюється автоматично. Тест може завантажити сценарій через `ha_scenario_tests.schema.load` і викликати фікстуру `scenario_runner`. JUnit формує сам pytest. `run_scenario` також можна імпортувати у звичайний Python-код.
