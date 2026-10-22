# دامنه و شواهد

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


<div dir="rtl" lang="fa">

این نسخه زیرمجموعه‌ای محدود را با محرک‌ها، شرط‌ها، زمان‌سنج‌ها، بارگذاری مجدد و ارسال عملیات اسکریپت واقعی Home Assistant اعتبارسنجی می‌کند. گیرنده‌های عملگر و وضعیت‌های ورودی مصنوعی‌اند. این کار پروتکل‌های ارتباطی، مصرف جریان، دقت حسگر، وضعیت فیزیکی رله، ایمنی یا رفتار همهٔ پیکربندی‌های ممکن HA را اثبات نمی‌کند.

ساعت، زمان واقعی سپری‌شدهٔ یکنواخت را اندازه می‌گیرد. آزمون‌ها عمداً بازه‌های کوتاه و حاشیهٔ زمان‌بندی دارند. روش‌های تأخیر داخلی HA را وصله نمی‌کنیم، مدت زمان‌سنج‌های عملیاتی را تغییر نمی‌دهیم و ادعای هم‌ارزی با زمان مجازی نداریم. ساعت تابستانی، زمان‌بندی ساعت دیواری، راه‌اندازی مجدد کامل فرایند HA و ماندگاری Recorder خارج از v1 هستند. بارگذاری مجدد آزموده می‌شود؛ این کار راه‌اندازی مجدد فرایند نیست.

ورودی شامل قالب اجرایی یا تنظیمات یکپارچه‌سازی نیست. هر کارگر از پوشهٔ موقت تمیز، محیط پالایش‌شده و محافظ ممیزی سراسری استفاده می‌کند. این کار جلوی ورودی/خروجی تصادفی شبکه یا زیرفرایند Python در مسیر مجاز را می‌گیرد. این محیط ایزولهٔ کد مخرب نیست: وابستگی‌های Python/بومی، مفسر و میزبان مورد اعتمادند. منابع یا وابستگی‌های نامطمئن را فقط در محیطی جداگانه و ایمن اجرا کنید. روش اختیاری Docker network-none جداسازی شبکه را تقویت می‌کند اما رفتار سخت‌افزار را ثابت نمی‌کند.

گزارش‌های عمومی باید فقط شامل داده‌های آزمون مصنوعی باشند. خط زمانی وضعیت‌های واقعی حتی بدون توکن، حضور در خانه و عادت‌ها را آشکار می‌کند. اینجا فهرست وسایل خانه، ضبط‌ها یا تنظیمات عملیاتی وجود ندارد. همهٔ نمودارها برچسب مصنوعی دارند و با `python scripts/render_diagrams.py` بازتولید می‌شوند.

برای بررسی‌های اندازه‌گیری‌شدهٔ این نسخه به [اعتبارسنجی](validation.fa.md) مراجعه کنید. پشتیبانی نصب به محیط‌های همان سابقه محدود است؛ روش کانتینر به معنی آزموده‌شدن همهٔ سکوها نیست.

</div>
