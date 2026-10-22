# Диагностика

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

- Код завершения 2 при установке или запуске: проверьте Python 3.14.2–3.14.x, точную закреплённую версию HA и чистую виртуальную среду. Runner отклоняет другие версии HA. Переустановите зависимости по lock-файлу перед сообщением об ошибке.
- Ошибка или таймаут worker: не удался импорт зависимости либо настройка HA. Запустите изолированный worker напрямую с **синтетическим** файлом, чтобы получить локальную трассировку: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Не публикуйте непроверенную диагностику среды.
- `calls_mismatch`: сравните порядок и повторяющиеся вызовы, а не только конечное состояние. Состояния seed задаются до старта; они не считаются автоматически новым триггером состояния после старта.
- `forbidden_call`: записанная команда синтетического исполнительного устройства совпала с запрещённой контрактом. Это настоящая диспетчеризация автоматизации, а не физическое срабатывание.
- `states_mismatch`: присваивание на шкале времени или синтетическое исполнительное устройство оставило иное состояние.
- `blocked_io` или `background_exception`: никогда не отключайте защиту ради зелёного результата. Этот выпуск не допускает сетевых интеграций. Сообщите синтетический пример воспроизведения и версию.
- Нестабильные тесты таймеров: увеличьте интервал между переходом состояния и проверяемым сроком. Измеряется реальное планирование event loop; виртуальные часы или точность планирования до микросекунды не обещаются.
- Reload: таймеры `for` могут отменяться настоящей перезагрузкой автоматизаций. Если политика требует восстановления, нужна явно заданная согласующая автоматизация; сравните `reload_reconcile.json`.
- Отчёт уже существует: `--report` намеренно отказывается его перезаписывать. Выберите новый путь.

Если после обычной, не editable-установки вы работаете с исходниками, перед проверкой изменений переустановите пакет. Для разработки устанавливайте с `--no-deps -e .`.
