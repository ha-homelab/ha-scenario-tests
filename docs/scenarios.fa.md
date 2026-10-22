# قرارداد سناریو v1

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


<div dir="rtl" lang="fa">

اعتبارسنج مرجع `src/ha_scenario_tests/schema.py` است. فقط JSON تا حداکثر 64 KiB پذیرفته می‌شود. کلید ناشناخته، کلید JSON تکراری، ورودی پیوند نمادین، عدد نامتناهی و نوع نامعتبر رد می‌شوند. تنظیمات خانه را در نمونه‌های عمومی کپی نکنید.

فیلدهای ریشهٔ الزامی: `schema: "ha-scenario/v1"`، یک `name` کوتاه با حروف کوچک، `seed`، `automations`، `timeline` و `expect`. مقدار پیش‌فرض `settle_seconds` اختیاری 0.1 است. همهٔ شناسه‌های موجودیت از پیشوند `scenario_` استفاده می‌کنند و باید در داده‌های اولیه تعریف شوند. دامنه‌های پشتیبانی‌شده: `light`، `switch`، `input_boolean`، `binary_sensor`. وضعیت‌های پشتیبانی‌شده: `on`، `off`، `unknown`، `unavailable`.

اتوماسیون شامل `id`، `triggers`، `actions` و به‌طور اختیاری `conditions` و `mode` (`single` یا `restart`) است. محرک‌های وضعیت به `trigger`، `entity_id` و `to` نیاز دارند؛ `from` و `for_seconds` اختیاری‌اند. محرک‌های رویداد از `trigger: "event"` و `event_type: "scenario_name"` استفاده می‌کنند؛ `automation_reloaded` نیز پشتیبانی می‌شود. شرط‌ها فقط مقایسهٔ وضعیت هستند. عملیات شامل `action` و یک `entity_id` است: `turn_on`، `turn_off` و `toggle` روی موجودیت‌های light/switch/input_boolean تعریف‌شده در ابتدا. قالب، انتخابگر، عملیات دستگاه، blueprint، اسکریپت از دیسک یا دادهٔ سرویس پذیرفته نمی‌شود.

گام‌های خط زمانی شامل `after` (ثانیهٔ نسبی از پایان گام قبلی) و دقیقاً یک عمل هستند:

</div>

<div dir="ltr">

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

</div>

<div dir="rtl" lang="fa">

عملیات دیگر: `"event": "scenario_manual_off"` یا `"reload": true`. بارگذاری مجدد، سرویس واقعی اتوماسیون HA را فراخوانی می‌کند که `configuration.yaml` موقت تولیدشده را می‌خواند؛ آزمون با انتشار رویداد تکمیل، بارگذاری مجدد را تقلید نمی‌کند.

`expect.calls` فهرست دقیق و مرتب رکوردهای `{action, entity_id}` با احتساب تکرارهاست؛ فهرست خالی همهٔ فراخوانی‌های عملگر را ممنوع می‌کند. `expect.forbidden` به‌صورت اختیاری فراخوانی‌هایی را فهرست می‌کند که هرگز نباید رخ دهند. `expect.states` شناسه‌های اولیه را به وضعیت نهایی نگاشت می‌کند. فراخوانی غیرمنتظره حتی اگر وضعیت نهایی تصادفاً منطبق باشد، آزمون را ناموفق می‌کند.

حدود: ۶۴ موجودیت اولیه، ۱۶ اتوماسیون، ۸ محرک و ۸ شرط برای هر اتوماسیون، ۱۶ عملیات برای هر اتوماسیون، ۳۲ گام خط زمانی، مجموع ۵ ثانیه انتظار درخواستی و ۲۵۶ فراخوانی ثبت‌شده. خطاهای کار پس‌زمینه و ورودی/خروجی مسدودشده اجرا را ناموفق می‌کنند. گزارش شامل زمان‌های سپری‌شدهٔ فراخوانی/گام با ساعت یکنواخت، مؤلفه‌های بارشده، وضعیت‌های نهایی و کدهای شکست است.

والد پیش از بازگرداندن، کل گزارش کارگر را اعتبارسنجی می‌کند. `passed` باید واقعاً از نوع Boolean و `physical_validation` برابر false باشد؛ طرح، نسخهٔ HA، نام سناریو، فیلدها و حدود باید با پروتکل منطبق باشند. والد همچنین ادعاهای فراخوانی/وضعیت را با سناریو می‌سنجد و صرفاً به پرچم موفقیت اعتماد نمی‌کند. خروجی نامعتبر و هر خروج غیرصفر کارگر خطای زمان اجرا محسوب می‌شود، حتی اگر فرزند شیء JSON ظاهراً موفقی چاپ کرده باشد.

نمونهٔ دادهٔ کهنهٔ ارائه‌شده، قطع انتقال را با `unavailable` نشان می‌دهد. تازگی منبع را از `last_changed` استنباط نمی‌کند، تجزیهٔ زمان‌مهر حسگر را نمی‌آزماید و رفتار انقضای حسگر واقعی را اثبات نمی‌کند. اعمال دستی، سیاست مصنوعی صریحی است؛ ابزار این سیاست را به اتوماسیون موجود اضافه نمی‌کند.

</div>
