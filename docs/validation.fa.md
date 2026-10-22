# سابقهٔ اعتبارسنجی

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


<div dir="rtl" lang="fa">

## اعتبارسنجی زمان اجرای Linux در 2026-10-15

[اجرای GitHub Actions شمارهٔ 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) روی کامیت `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` با CPython 3.14.8 در Ubuntu و Home Assistant 2026.10.0 ثابت‌شده موفق بود. فرمان کامل `python3 -m pytest -q` با **۵۴ آزمون موفق در ۲۱٫۴۲ ثانیه** و بدون آزمون ردشده به پایان رسید. هر هفت آزمون زمان اجرا با HA واقعی در این نتیجه هستند: چهار سناریوی نمونه، مورد انتظار/عمل ممنوع که عمداً شکست می‌خورد، گزارش JSON بومی‌شدهٔ CLI و قرارداد انتقال نقش مصرف‌کنندهٔ پایین‌دست. هر آزمون زمان اجرا کارگر کنترل‌شدهٔ تازه‌ای آغاز می‌کند؛ ادعاهای شکست مورد انتظار به‌عنوان شکست آزموده می‌شوند، نه به‌عنوان سناریوهای موفق.

در همان اجرا، Ruff، بررسی پیوندهای مستندات/SVG، ساخت منبع و wheel، سیاست انتشار منبع و اسکن اسرار در تمام تاریخچه نیز موفق بودند. این نتایج ارسال سرویس مصنوعی و رفتار وضعیت را تحت محافظ ورودی/خروجی Python مستندشده اعتبارسنجی می‌کنند. این کار محیط ایزولهٔ امنیتی سیستم‌عامل ایجاد نمی‌کند، اجرای Docker را تأیید نمی‌کند و رفتار دستگاه فیزیکی را اثبات نمی‌کند.

## بررسی‌های توسعهٔ macOS در 2026-10-15

منبع، پذیرش سخت‌گیرانهٔ ورودی، محافظ ممیزی Python، ترجمه‌های CLI و بازتولید SVG به‌صورت محلی با Python 3.14.7 در macOS arm64 بررسی شدند. فرمان `python -m pytest -q -m 'not runtime'` **۴۷ آزمون** را با موفقیت گذراند؛ این فرمان هفت مورد HA واقعی را صریحاً کنار می‌گذارد. `python -m ruff check src tests scripts` موفق بود. این جایگزین مجموعهٔ کامل آزمون زمان اجرا نیست.

موتور واقعی Home Assistant 2026.10.0 مؤلفه‌های `automation`، `blueprint` و `trace` را بار کرد و سناریوهای پایان مهلت حضور و اعمال دستی را با فراخوانی‌های سرویس مصنوعی و وضعیت‌های نهایی مورد انتظار و بدون ورودی/خروجی مسدودشده اجرا کرد. سپس فرایند محلی Python هنگام پاک‌سازی مفسر با خطای قطعه‌بندی بومی خارج شد. اجراکنندهٔ والد این خروج غیرصفر را درست به‌عنوان شکست زمان اجرا تلقی می‌کند، حتی اگر پیش از آن محتوای JSON موفق آمده باشد. **ادعای موفقیت کامل آزمون زمان اجرای macOS نداریم.**

پیش از پذیرش انتشار، مجموعهٔ کامل Linux CI الزامی است. `python -m pytest -q --junitxml=junit.xml` را اجرا کنید؛ نبود HA، نسخهٔ نادرست HA، پایان مهلت فرزند و خروج غیرصفر فرزند شکست‌اند و هرگز بی‌صدا نادیده گرفته نمی‌شوند. اجرای پیوندشدهٔ بالا شاهد Linux برای این پیاده‌سازی است؛ تغییرات بعدی اجرای موفق خود را لازم دارند. در این سابقه ادعای اجرای Docker یا اعتبارسنجی دستگاه فیزیکی وجود ندارد.

## فرادادهٔ راه‌اندازی کنترل‌شده

کارگر مقدار مصنوعی `synthetic` را برای فرادادهٔ پردازندهٔ ذخیره‌شده در حافظهٔ نهان Python فراهم می‌کند و پیش از واردکردن HA، `socket.has_ipv6` را غیرفعال می‌کند. این کار از ایجاد `uname -p` هنگام راه‌اندازی سکوی HA و آزمایش اتصال IPv6 محلی هنگام واردکردن urllib3 جلوگیری می‌کند. در Linux، ifaddr زیر محافظ با `ctypes.CDLL(None)` وارد می‌شود و نمادهای libc از پیش بارشده در فرایند را حل می‌کند؛ در نتیجه زیرفرایند `ldconfig` جست‌وجوگر کتابخانه اجرا نمی‌شود. جست‌وجوگر عادی کتابخانه بلافاصله بازگردانده می‌شود. محافظ ورودی/خروجی برای این عملیات استثنای فهرست مجاز ندارد. این تغییرات فقط فراداده/کاوش میزبان را تحت تأثیر قرار می‌دهند؛ محرک‌ها، شرط‌ها، زمان‌سنج‌ها، بارگذاری مجدد، اسکریپت‌ها و ارسال سرویس HA واقعی‌اند. آن‌ها به نسخه حساس‌اند و مجموعهٔ آزمون زمان اجرای ثابت‌شده آن‌ها را پوشش می‌دهد.

## بازتولید

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

<div dir="rtl" lang="fa">

هیچ گزارشی وضعیت واقعی رله، تحویل رادیویی، دقت حضور در خانه یا زمان‌بندی با مدت عملیاتی را ثابت نمی‌کند. خط زمانی SVG انتظارهای مصنوعی را نشان می‌دهد، نه اندازه‌گیری معیار کارایی.

مجموعهٔ زمان اجرا شامل `tests/fixtures/role_transfer.json` نیز هست؛ قرارداد مصنوعی پایین‌دست که نقش فعلی خاموش می‌شود و پریز کنارگذاشته‌شده روشن می‌ماند. این آزمون انتقال بار فیزیکی نیست.

</div>
