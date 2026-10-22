# חוזה תרחיש v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="scenarios.md" lang="en" dir="ltr">English</a> ·
<a href="scenarios.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="scenarios.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="scenarios.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="scenarios.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="scenarios.es.md" lang="es" dir="ltr">Español</a> ·
<a href="scenarios.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="scenarios.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="scenarios.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="scenarios.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="scenarios.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="scenarios.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="scenarios.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="scenarios.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="scenarios.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="scenarios.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="scenarios.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="scenarios.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="scenarios.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="scenarios.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="scenarios.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="scenarios.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="scenarios.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="scenarios.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->


<div dir="rtl" lang="he">

המאמת הקובע הוא `src/ha_scenario_tests/schema.py`. מתקבל JSON בלבד, עד 64 KiB. מפתחות לא מוכרים, מפתחות JSON כפולים, קלט מקישור סמלי, מספרים לא סופיים וטיפוסים שגויים נדחים. אל תעתיקו תצורת בית לדוגמאות ציבוריות.

שדות השורש הנדרשים: `schema: "ha-scenario/v1"`, שדה `name` קצר באותיות קטנות, `seed`, `automations`, `timeline`, `expect`. ברירת המחדל של `settle_seconds` האופציונלי היא 0.1. כל מזהי הישויות משתמשים בקידומת `scenario_` וחייבים להיות מוגדרים בנתוני האתחול. התחומים הנתמכים: `light`, `switch`, `input_boolean`, `binary_sensor`. המצבים הנתמכים: `on`, `off`, `unknown`, `unavailable`.

לאוטומציה יש `id`, `triggers`, `actions`, ולפי הצורך `conditions` ו־`mode` (`single` או `restart`). טריגרים של מצב דורשים `trigger`, `entity_id`, `to`; אפשר להוסיף `from` ו־`for_seconds`. טריגרים של אירוע משתמשים ב־`trigger: "event"` וב־`event_type: "scenario_name"`; גם `automation_reloaded` נתמך. תנאים הם השוואות מצב בלבד. פעולות מכילות `action` ו־`entity_id` אחד: `turn_on`, `turn_off`, `toggle` על ישויות light/switch/input_boolean שהוגדרו באתחול. אין תמיכה בתבניות, בבוררים, בפעולות מכשיר, ב־blueprints, בסקריפטים מהדיסק או בנתוני שירות.

שלבי ציר הזמן מכילים `after` (שניות יחסיות מאז השלמת השלב הקודם) ופעולה אחת בדיוק:

</div>

<div dir="ltr">

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

</div>

<div dir="rtl" lang="he">

פעולות אחרות: `"event": "scenario_manual_off"` או `"reload": true`. טעינה מחדש קוראת לשירות האוטומציה האמיתי של HA, שקורא את `configuration.yaml` הזמני שנוצר; הבדיקה אינה מחקה טעינה מחדש באמצעות שליחת אירוע ההשלמה שלה.

`expect.calls` היא הרשימה המדויקת והמסודרת של רשומות `{action, entity_id}`, כולל חזרות; רשימה ריקה אוסרת כל קריאה למפעיל. `expect.forbidden` מפרטת באופן אופציונלי קריאות שאסור שיקרו אי פעם. `expect.states` ממפה מזהים מאותחלים למצבים הסופיים. קריאות בלתי צפויות מכשילות את הריצה גם אם המצב הסופי תואם במקרה.

מגבלות: 64 ישויות אתחול, 16 אוטומציות, 8 טריגרים ו־8 תנאים לכל אוטומציה, 16 פעולות לכל אוטומציה, 32 שלבי ציר זמן, 5 שניות המתנה מבוקשת בסך הכול ו־256 קריאות מתועדות. שגיאות במשימות רקע וקלט/פלט חסום מכשילים את הריצה. הדוח כולל זמני קריאה/שלב שחלפו לפי שעון מונוטוני, רכיבים שנטענו, מצבים סופיים וקודי כשל.

האב מאמת את כל דוח העובד לפני החזרתו. `passed` חייב להיות ממש מטיפוס Boolean, `physical_validation` חייב להיות false, והסכמה, גרסת HA, שם התרחיש, השדות והגבולות חייבים להתאים לפרוטוקול. האב גם בודק את טענות הקריאות והמצבים מול התרחיש, במקום לסמוך על דגל הצלחה. פלט לא תקין וכל יציאת עובד שאינה אפס הם שגיאות זמן ריצה, גם אם הילד הדפיס אובייקט JSON שנראה מוצלח.

דוגמת המידע הישן המצורפת מייצגת אובדן תקשורת באמצעות `unavailable`. היא אינה מסיקה את עדכניות המקור מתוך `last_changed`, אינה בודקת פענוח חותמות זמן של חיישן ואינה מוכיחה את התנהגות פקיעת התוקף של חיישן אמיתי. עקיפה ידנית היא מדיניות סינתטית מפורשת; הכלי אינו מוסיף אותה לאוטומציה קיימת.

</div>
