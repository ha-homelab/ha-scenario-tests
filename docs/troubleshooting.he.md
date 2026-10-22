# פתרון תקלות

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


<div dir="rtl" lang="he">

- יציאה בקוד 2 בהתקנה/הרצה: בדקו Python 3.14.2–3.14.x, קיבוע מדויק של גרסת HA וסביבה וירטואלית נקייה. המריץ דוחה גרסאות HA אחרות. התקינו מחדש מקובץ הנעילה לפני דיווח על כשל.
- כשל/חריגה מזמן העובד: ייבוא תלות או הקמת HA נכשלו. הריצו את העובד המבודד ישירות עם קובץ **סינתטי** כדי לקבל עקבת שגיאה מקומית: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. אל תפרסמו אבחון סביבה שלא נבדק.
- `calls_mismatch`: השוו סדר וקריאות כפולות, לא רק מצב סופי. מצבי האתחול נקבעים לפני ההפעלה; הם אינם נחשבים אוטומטית לטריגר מצב חדש אחריה.
- `forbidden_call`: פקודת מפעיל סינתטי שנלכדה התאימה לחוזה האיסור. זו הפעלה אמיתית של אוטומציה, ולא הפעלה פיזית.
- `states_mismatch`: השמה בציר הזמן או מפעיל סינתטי השאירו מצב שונה.
- `blocked_io` או `background_exception`: לעולם אל תשביתו את ההגנה כדי לקבל תוצאה ירוקה. גרסה זו אינה מאפשרת אינטגרציות רשת. דווחו על השחזור הסינתטי ועל הגרסה.
- בדיקות טיימר לא יציבות: הגדילו את הפער בין שינוי מצב למועד שנבדק. נמדד התזמון האמיתי של לולאת האירועים; אין הבטחה לשעון וירטואלי או לתזמון מדויק ברמת מיקרושנייה.
- טעינה מחדש: הטעינה האמיתית עשויה לבטל טיימרים של `for`. נדרשת אוטומציית יישור מפורשת כשמדיניות דורשת התאוששות; השוו ל־`reload_reconcile.json`.
- דוח קיים: `--report` מסרב במכוון לדרוס אותו. בחרו נתיב חדש.

אם משתמשים בעץ המקור אחרי התקנה שאינה ניתנת לעריכה, התקינו מחדש את החבילה לפני בדיקת שינויים. לפיתוח התקינו עם `--no-deps -e .`.

</div>
