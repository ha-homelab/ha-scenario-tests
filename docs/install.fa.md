# نصب و جداسازی

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


<div dir="rtl" lang="fa">

محیط اجرای Home Assistant با نسخهٔ ثابت را همراه Python 3.14.2–3.14.x به کار ببرید. مطابق README ریشه، ابتدا `requirements.lock` را با `--require-hashes` و سپس این بسته را با `--no-deps .` نصب کنید. فایل قفل، وابستگی‌های برنامه و آزمون را پوشش می‌دهد. محیط تمیز الزامی است؛ در محیط Home Assistant عملیاتی نصب نکنید. هنگام ویرایش منبع، به‌جای آن از `pip install --no-deps -e .` استفاده کنید.

ابتدا `ha-scenario validate examples/stale_sensor.json` را اجرا کنید. اعتبارسنجی، محیط اجرای HA را وارد نمی‌کند. سپس `ha-scenario run examples/stale_sensor.json --report result.json` را اجرا کنید. هیچ سرور مقصدی پیکربندی نمی‌شود. تنها مسیر خروجی از آرگومان صریح `--report` شما می‌آید، نه از سناریو.

برای مرز شبکه‌ای قوی‌تر:

</div>

<div dir="ltr">

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

</div>

<div dir="rtl" lang="fa">

ساخت برای دریافت وابستگی‌ها به اینترنت نیاز دارد. هنگام اجرا شبکه‌ای وجود ندارد و `/tmp` قابل نوشتن و یک‌بارمصرف است؛ تنظیمات خانه، سوکت Docker یا اطلاعات احراز هویت متصل نمی‌شوند. این روش استقرار اختیاری است؛ برای اطلاع از اینکه دقیقاً همین کانتینر اجرا شده یا نه، سابقهٔ اعتبارسنجی را ببینید. شبکهٔ میزبان یا اتصال مسیرهای عملیاتی را اضافه نکنید.

رابط زیرفرایند، اطلاعات احراز هویت ارث‌رسیده و `PYTHONPATH` را حذف می‌کند. گزینهٔ `-I` در کارگر از بستهٔ نصب‌شده استفاده می‌کند. فقط PATH، SYSTEMROOT و LANG به ارث می‌رسند؛ بذر هش ثابت است. در Linux مسیر کتابخانهٔ کارگر از `LIBDIR` نصب Python در حال اجرا گرفته می‌شود تا ساخت‌های جابه‌جاشدنی Python بتوانند libpython را پیدا کنند. `LD_LIBRARY_PATH` ارث‌رسیده هرگز کپی نمی‌شود. فرزند مهلت ۳۰ثانیه‌ای از سوی والد و مهلت داخلی ۲۰ثانیه‌ای دارد؛ مجموع انتظار درخواستی خط زمانی حداکثر ۵ ثانیه و تعداد عملیات ثبت‌شده حداکثر ۲۵۶ است. توقف وابستگی‌های بومی با پایان مهلت والد خاتمه می‌یابد.

افزونهٔ pytest خودکار نصب می‌شود. آزمون می‌تواند سناریو را با `ha_scenario_tests.schema.load` بار کند و fixture به نام `scenario_runner` را فراخواند. JUnit را خود pytest تولید می‌کند. واردکردن `run_scenario` در Python عادی نیز ممکن است.

</div>
