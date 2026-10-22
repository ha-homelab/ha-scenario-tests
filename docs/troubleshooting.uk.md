# Діагностика

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

- Код завершення 2 під час встановлення або запуску: перевірте Python 3.14.2–3.14.x, точну закріплену версію HA та чисте віртуальне середовище. Runner відхиляє інші версії HA. Перш ніж повідомляти про помилку, перевстановіть залежності за файлом фіксації.
- Помилка або тайм-аут worker: не вдався імпорт залежності чи налаштування HA. Запустіть ізольований worker безпосередньо із **синтетичним** файлом, щоб отримати локальне трасування: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Не публікуйте неперевірену діагностику середовища.
- `calls_mismatch`: порівняйте порядок і повторювані виклики, а не лише кінцевий стан. Стани seed задаються до запуску; вони не вважаються автоматично новим тригером стану після запуску.
- `forbidden_call`: записана команда синтетичного виконавчого пристрою збіглася з негативним контрактом. Це справжня диспетчеризація автоматизації, а не фізичне спрацювання.
- `states_mismatch`: присвоєння на часовій шкалі чи синтетичний виконавчий пристрій залишив інший стан.
- `blocked_io` або `background_exception`: ніколи не вимикайте захист заради зеленого результату. Цей випуск не допускає мережевих інтеграцій. Повідомте синтетичний приклад відтворення та версію.
- Нестабільні тести таймерів: збільште проміжок між переходом стану й перевірюваним терміном. Вимірюється реальне планування циклу подій; віртуальний годинник або точність до мікросекунди не обіцяються.
- Reload: таймери `for` можуть скасовуватися справжнім перезавантаженням автоматизацій. Якщо політика вимагає відновлення, потрібна явно задана узгоджувальна автоматизація; порівняйте `reload_reconcile.json`.
- Звіт уже існує: `--report` навмисно відмовляється його перезаписувати. Оберіть новий шлях.

Якщо після звичайного, не editable-встановлення ви використовуєте вихідне дерево, перевстановіть пакет перед перевіркою змін. Для розробки встановлюйте з `--no-deps -e .`.
