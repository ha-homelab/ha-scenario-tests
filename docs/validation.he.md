# רשומת אימות

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


<div dir="rtl" lang="he">

## אימות זמן ריצה ב־Linux בתאריך 2026-10-15

[הרצת GitHub Actions מספר 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) עברה ב־commit ‏`0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, עם CPython 3.14.8 ב־Ubuntu ועם Home Assistant 2026.10.0 המקובע. הפקודה המלאה `python3 -m pytest -q` הסתיימה עם **54 בדיקות שעברו בתוך 21.42 שניות**, ללא דילוגים. נכללו כל שבע בדיקות זמן הריצה עם HA אמיתי: ארבעה תרחישי דוגמה, מקרה ציפייה/פעולה אסורה שנכשל במכוון, דוח CLI JSON מתורגם וחוזה העברת תפקיד של הצרכן בהמשך. כל בדיקת זמן ריצה פותחת עובד מבוקר חדש; טענות כשל צפוי נבדקות ככשלים ולא מדווחות כתרחישים מוצלחים.

באותה הרצה עברו גם Ruff, בדיקות קישורי תיעוד/SVG, בניית מקור ו־wheel, מדיניות פרסום המקור וסריקת סודות בהיסטוריה המלאה. זה מאמת שיגור שירותים סינתטי והתנהגות מצבים תחת הגנת הקלט/פלט המתועדת של Python. זה אינו מבסס ארגז חול אבטחתי של מערכת ההפעלה, אינו מאמת הרצת Docker ואינו מוכיח התנהגות של מכשיר פיזי.

## בדיקות פיתוח macOS בתאריך 2026-10-15

המקור, קבלת הקלט המחמירה, הגנת הביקורת של Python, תרגומי CLI ויצירה מחדש של SVG נבדקו מקומית עם Python 3.14.7 ב־macOS arm64. הפקודה `python -m pytest -q -m 'not runtime'` עברה **47 בדיקות**; שבעת מקרי HA האמיתי מוחרגים במפורש בפקודה זו. `python -m ruff check src tests scripts` עברה. זה אינו תחליף למערך זמן הריצה המלא.

מנוע Home Assistant 2026.10.0 האמיתי טען `automation`, ‏`blueprint` ו־`trace`, והריץ את תרחישי פקיעת זמן הנוכחות והעקיפה הידנית עם קריאות שירות סינתטיות ומצבים סופיים כצפוי, וללא קלט/פלט חסום. לאחר מכן תהליך Python המקומי יצא בשל segmentation fault מקורי בעת פירוק המפרש. המריץ האב מתייחס כראוי ליציאה שאינה אפס ככשל זמן ריצה, גם כשקדמה לה חבילת JSON מוצלחת. **אין טענה שכל בדיקת זמן הריצה ב־macOS עברה.**

מערך Linux CI המלא נדרש לפני קבלת גרסה. הריצו `python -m pytest -q --junitxml=junit.xml`; HA חסר, גרסאות HA שגויות, חריגות זמן של ילד ויציאות ילד שאינן אפס מכשילות ואינן מדולגות בשקט. ההרצה המקושרת למעלה היא ראיית Linux למימוש זה; שינויים מאוחרים יותר דורשים הרצה מוצלחת משלהם. רשומה זו אינה טוענת להרצת Docker או לאימות מכשיר פיזי.

## מטא־נתוני אתחול מבוקרים

העובד מספק את הערך הסינתטי `synthetic` למטא־נתוני המעבד השמורים במטמון של Python, ומשבית `socket.has_ipv6` לפני ייבוא HA. כך נמנעת הפעלת `uname -p` באתחול הפלטפורמה של HA, ונמנעת בדיקת bind ל־IPv6 ב־localhost בעת ייבוא urllib3. ב־Linux מייבאים את ifaddr תחת ההגנה באמצעות `ctypes.CDLL(None)`, שמאתר סמלי libc שכבר נטענו בתהליך; כך נמנע תהליך המשנה `ldconfig` של מאתר הספריות. מאתר הספריות הרגיל משוחזר מיד. להגנת הקלט/פלט אין חריג ברשימת ההיתרים לפעולות האלה. השינויים משפיעים רק על מטא־נתונים/גישוש של המארח; הטריגרים, התנאים, הטיימרים, הטעינה מחדש, הסקריפטים ושיגור השירותים של HA אמיתיים. הם תלויי גרסה ומכוסים במערך זמן הריצה המקובע.

## שחזור

</div>

<div dir="ltr">

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

</div>

<div dir="rtl" lang="he">

אף דוח אינו מוכיח מצב ממסר אמיתי, מסירה אלחוטית, דיוק נוכחות בבית או תזמון במשכי זמן של סביבת ייצור. ציר הזמן ב־SVG מציג ציפיות סינתטיות, ולא מדידות ביצועים.

מערך זמן הריצה כולל גם את `tests/fixtures/role_transfer.json`, החוזה הסינתטי של הצרכן בהמשך: התפקיד הנוכחי נכבה והשקע שיצא משימוש נשאר דלוק. זו אינה בדיקת העברת עומס פיזי.

</div>
