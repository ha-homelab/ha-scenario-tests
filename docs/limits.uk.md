# Обсяг і докази

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

Цей випуск перевіряє обмежену підмножину можливостей зі справжніми тригерами, умовами, таймерами, перезавантаженням автоматизацій і диспетчеризацією дій скриптів Home Assistant. Одержувачі команд виконавчих пристроїв і вхідні стани синтетичні. Це не доводить роботу протоколів зв’язку, споживання струму, точність датчиків, фізичний стан реле, безпеку чи поведінку кожної можливої конфігурації HA.

Годинник вимірює реальний минулий монотонний час. Тести навмисно використовують короткі інтервали й запас на планування. Ми не змінюємо внутрішні методи затримки HA, не переписуємо тривалості робочих таймерів і не заявляємо еквівалентності віртуальному часу. Перехід на літній час, розклади за цивільним годинником, повний перезапуск процесу HA та збереження даних Recorder не входять до v1. Перевіряється reload; це не перезапуск процесу.

Вхідні дані не містять виконуваних шаблонів або конфігурації інтеграцій. Кожен worker використовує чистий тимчасовий каталог, очищене середовище й глобальний захист аудиту. Це запобігає випадковому мережевому вводу-виводу та запуску підпроцесів Python через дозволений шлях. Це не пісочниця для ворожого коду: залежностям Python і нативним залежностям, інтерпретатору та хосту довіряють. Недовірені вихідні коди або залежності запускайте лише в окремо захищеному середовищі. Необов’язковий спосіб Docker без мережі посилює мережеву ізоляцію, але не доводить поведінку обладнання.

Публічні звіти мають містити лише синтетичні фікстури. Реальні часові послідовності станів розкривають присутність людей і звички навіть без токена. Тут немає інвентарю домогосподарства, записів чи робочої конфігурації. Усі діаграми позначено як синтетичні; їх можна відтворити командою `python scripts/render_diagrams.py`.

Виміряні перевірки цього випуску наведено у [протоколі перевірки](validation.md). Підтримка встановлення обмежена зазначеними там середовищами; спосіб запуску контейнера не є заявою, що перевірено кожну платформу.
