# عیب‌یابی

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


<div dir="rtl" lang="fa">

- خروج ۲ هنگام نصب/اجرا: Python 3.14.2–3.14.x، نسخهٔ دقیق و ثابت HA و محیط مجازی تمیز را بررسی کنید. اجراکننده دیگر نسخه‌های HA را رد می‌کند. پیش از گزارش شکست، دوباره از فایل قفل نصب کنید.
- شکست/پایان مهلت کارگر: واردکردن وابستگی یا راه‌اندازی HA ناموفق بوده است. برای دریافت ردگیری محلی، کارگر ایزوله را مستقیماً با فایل **مصنوعی** اجرا کنید: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. اطلاعات تشخیصی بازبینی‌نشدهٔ محیط را منتشر نکنید.
- `calls_mismatch`: ترتیب و فراخوانی‌های تکراری را مقایسه کنید، نه فقط وضعیت نهایی را. وضعیت‌های اولیه پیش از شروع تنظیم می‌شوند؛ پس از شروع خودکار محرک وضعیت تازه محسوب نمی‌شوند.
- `forbidden_call`: فرمان ثبت‌شدهٔ عملگر مصنوعی با قرارداد منع مطابقت داشته است. این ارسال واقعی اتوماسیون است، نه عمل فیزیکی.
- `states_mismatch`: انتساب خط زمانی یا عملگر مصنوعی وضعیت دیگری باقی گذاشته است.
- `blocked_io` یا `background_exception`: هرگز برای سبزکردن نتیجه محافظ را خاموش نکنید. این نسخه یکپارچه‌سازی شبکه‌ای نمی‌پذیرد. بازتولید مصنوعی و نسخه را گزارش کنید.
- ناپایداری آزمون زمان‌سنج: فاصلهٔ تغییر وضعیت تا مهلت مورد ادعا را افزایش دهید. زمان‌بندی واقعی حلقهٔ رویداد سنجیده می‌شود؛ ساعت مجازی یا زمان‌بندی دقیق میکروثانیه‌ای تضمین نشده است.
- بارگذاری مجدد: بارگذاری واقعی ممکن است زمان‌سنج‌های `for` را لغو کند. اگر سیاست به بازیابی نیاز دارد، اتوماسیون تطبیق صریح لازم است؛ `reload_reconcile.json` را مقایسه کنید.
- گزارش موجود: `--report` عمداً بازنویسی آن را رد می‌کند. مسیر تازه‌ای انتخاب کنید.

اگر پس از نصب غیرقابل‌ویرایش از درخت منبع استفاده می‌کنید، پیش از آزمون تغییرات بسته را دوباره نصب کنید. برای توسعه با `--no-deps -e .` نصب کنید.

</div>
