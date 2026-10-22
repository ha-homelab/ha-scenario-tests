# استكشاف الأخطاء وإصلاحها

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


<div dir="rtl" lang="ar">

- الخروج بالرمز 2 أثناء التثبيت أو التشغيل: تحقّق من Python 3.14.2–3.14.x وإصدار HA المثبّت بدقة وبيئة افتراضية نظيفة. يرفض المشغّل إصدارات HA الأخرى. أعد التثبيت من ملف القفل قبل الإبلاغ عن فشل.
- فشل العامل أو انتهاء مهلته: فشل استيراد اعتمادية أو إعداد HA. شغّل العامل المعزول مباشرةً مع ملف **اصطناعي** للحصول على تتبّع خطأ محلي: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. لا تنشر تشخيصات البيئة قبل مراجعتها.
- `calls_mismatch`: قارن الترتيب والاستدعاءات المكررة، لا الحالة النهائية وحدها. تُضبط الحالات الأولية قبل البدء؛ ولا تُحسب تلقائياً كمشغّل حالة جديد بعد البدء.
- `forbidden_call`: طابق أمر مشغّل اصطناعي مسجّل العقدَ السلبي. هذا إرسال أتمتة حقيقي وليس تشغيلاً مادياً.
- `states_mismatch`: ترك إسناد في الخط الزمني أو مشغّل اصطناعي حالة مختلفة.
- `blocked_io` أو `background_exception`: لا تعطّل الحارس أبداً للحصول على نتيجة خضراء. لا يسمح هذا الإصدار بتكاملات شبكية. أبلغ عن إعادة الإنتاج الاصطناعية والإصدار.
- تقلب نتائج المؤقّت: زد الفاصل بين انتقال الحالة والموعد الذي يؤكده الاختبار. تُقاس جدولة حلقة الأحداث الفعلية؛ لا نضمن ساعة افتراضية أو جدولة دقيقة إلى الميكروثانية.
- إعادة التحميل: قد تلغي إعادة التحميل الحقيقية مؤقّتات `for`. إذا تطلبت السياسة استعادة الحالة، تلزم أتمتة تسوية صريحة؛ قارن `reload_reconcile.json`.
- وجود تقرير سابق: يرفض `--report` عمداً الكتابة فوقه. اختر مساراً جديداً.

عند استخدام شجرة المصدر بعد تثبيت غير قابل للتحرير، أعد تثبيت الحزمة قبل اختبار التغييرات. للتطوير ثبّت باستخدام `--no-deps -e .`.

</div>
