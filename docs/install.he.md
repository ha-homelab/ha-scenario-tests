# התקנה ובידוד

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


<div dir="rtl" lang="he">

השתמשו בסביבת הריצה של Home Assistant בגרסה המקובעת עם Python 3.14.2–3.14.x. התקינו את `requirements.lock` באמצעות `--require-hashes`, ואז התקינו חבילה זו באמצעות `--no-deps .`, כמתואר ב־README שבשורש. קובץ הנעילה מכסה את תלויות היישום והבדיקות. נדרשת סביבה נקייה; אל תתקינו בסביבת Home Assistant שבשימוש בפועל. בעת עריכת המקור השתמשו במקום זאת ב־`pip install --no-deps -e .`.

הריצו תחילה `ha-scenario validate examples/stale_sensor.json`. האימות אינו מייבא את סביבת הריצה של HA. לאחר מכן הריצו `ha-scenario run examples/stale_sensor.json --report result.json`. לא מוגדר שרת יעד. נתיב הפלט היחיד מגיע מהארגומנט המפורש `--report` שסיפקתם, ולא מהתרחיש.

לגבול רשת חזק יותר:

</div>

<div dir="ltr">

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

</div>

<div dir="rtl" lang="he">

הבנייה דורשת גישה לאינטרנט להורדת תלויות. בזמן ההרצה אין רשת, ו־`/tmp` ניתן לכתיבה ונמחק בסיום; לא מעגנים הגדרות בית, שקע Docker או פרטי הזדהות. זו הוראת פריסה אופציונלית; בדקו ברשומת האימות אם המכולה המדויקת הזו אכן הורצה. אל תוסיפו רשת מארח או עיגונים מסביבת הייצור.

ממשק תהליך המשנה מסיר פרטי הזדהות שעברו בירושה ואת `PYTHONPATH`. האפשרות `-I` של העובד משתמשת בחבילה המותקנת. רק PATH, SYSTEMROOT ו־LANG עוברים בירושה; זרע הגיבוב מקובע. ב־Linux נתיב הספריות של העובד נגזר מ־`LIBDIR` בהתקנת Python הפעילה, וכך גם בניות Python הניתנות להעברה יכולות למצוא את libpython. ערך `LD_LIBRARY_PATH` שעבר בירושה לעולם אינו מועתק. לתהליך הילד יש מגבלה של 30 שניות מצד האב, מגבלה פנימית של 20 שניות, לכל היותר 5 שניות המתנה מבוקשת בציר הזמן ו־256 פעולות מתועדות. תקיעות בתלויות מקוריות נעצרות עם פקיעת הזמן אצל האב.

תוסף pytest מותקן אוטומטית. בדיקה יכולה לטעון תרחיש באמצעות `ha_scenario_tests.schema.load` ולקרוא ל־fixture בשם `scenario_runner`. pytest עצמו מייצר JUnit. אפשר גם לייבא `run_scenario` בקוד Python רגיל.

</div>
