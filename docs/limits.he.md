# היקף וראיות

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


<div dir="rtl" lang="he">

גרסה זו מאמתת תת־קבוצה מוגבלת באמצעות טריגרים, תנאים, טיימרים, טעינה מחדש ושיגור פעולות סקריפט אמיתיים של Home Assistant. מקבלי פקודות המפעילים ומצבי הקלט הם סינתטיים. אין בכך הוכחה לפרוטוקולי תקשורת, לצריכת זרם, לדיוק חיישנים, למצב פיזי של ממסר, לבטיחות או להתנהגות של כל תצורת HA אפשרית.

השעון מודד זמן מונוטוני אמיתי שחלף. הבדיקות משתמשות במכוון במרווחים קצרים ובמרווח ביטחון לתזמון. איננו משנים את שיטות ההשהיה הפנימיות של HA, משכתבים זמני טיימרים מסביבת הייצור או טוענים לשקילות לזמן וירטואלי. שעון קיץ, תזמון לפי שעה, הפעלה מחדש של כל תהליך HA ושמירה מתמשכת של Recorder אינם נכללים ב־v1. טעינה מחדש נבדקת; היא אינה הפעלה מחדש של תהליך.

הקלט אינו מכיל תבניות ניתנות לביצוע או תצורת אינטגרציה. כל עובד משתמש בספרייה זמנית נקייה, בסביבה מצומצמת ובמנגנון ביקורת כללי. הדבר מונע קלט/פלט מקרי של רשת או תהליכי משנה ב־Python דרך המסלול המותר. אין זה ארגז חול לקוד עוין: תלויות Python ותלויות מקוריות, המפרש והמארח נחשבים מהימנים. הריצו מקור או תלויות לא מהימנים רק בסביבה מאובטחת נפרדת. מתכון Docker האופציונלי network-none מחזק בידוד רשת, אך אינו מוכיח התנהגות חומרה.

דוחות ציבוריים צריכים להכיל רק נתוני בדיקה סינתטיים. צירי זמן של מצבים אמיתיים חושפים נוכחות בבית והרגלים גם בלי אסימון. אין כאן רשימת ציוד ביתי, הקלטות או תצורת ייצור. כל התרשימים מסומנים כסינתטיים וניתנים לשחזור באמצעות `python scripts/render_diagrams.py`.

ראו [אימות](validation.he.md) לבדיקות המדודות שבוצעו בגרסה זו. תמיכת ההתקנה מוגבלת לסביבות שברשומה; הוראות המכולה אינן טענה שכל פלטפורמה נבדקה.

</div>
