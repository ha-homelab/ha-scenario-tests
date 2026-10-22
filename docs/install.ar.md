# التثبيت والعزل

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


<div dir="rtl" lang="ar">

استخدم إصدار Home Assistant المثبّت مع Python 3.14.2–3.14.x. ثبّت `requirements.lock` باستخدام `--require-hashes`، ثم ثبّت هذه الحزمة باستخدام `--no-deps .`، كما يوضح README في الجذر. يشمل ملف القفل اعتماديات التطبيق والاختبارات. يلزم استخدام بيئة نظيفة؛ لا تثبّت الحزمة في بيئة Home Assistant الإنتاجية. عند تعديل المصدر استخدم `pip install --no-deps -e .` بدلاً من ذلك.

شغّل `ha-scenario validate examples/stale_sensor.json` أولاً. لا يستورد التحقق بيئة تشغيل HA. ثم شغّل `ha-scenario run examples/stale_sensor.json --report result.json`. لا يُضبط أي خادم مستهدف. يأتي مسار الإخراج الوحيد من وسيطة `--report` التي تحددها صراحةً، وليس من السيناريو.

لحدود عزل شبكي أقوى:

</div>

<div dir="ltr">

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

</div>

<div dir="rtl" lang="ar">

يحتاج البناء إلى الإنترنت لتنزيل الاعتماديات. لا تتوفر شبكة أثناء التشغيل، ويكون `/tmp` قابلاً للكتابة ومؤقتاً يُتخلّص منه؛ لا تُركّب إعدادات المنزل أو مقبس Docker أو بيانات الاعتماد. هذه وصفة نشر اختيارية؛ راجع سجل التحقق لمعرفة إن كانت هذه الحاوية بعينها قد نُفّذت. لا تضف شبكة المضيف أو نقاط تركيب من بيئة الإنتاج.

تزيل واجهة العملية الفرعية بيانات الاعتماد الموروثة و`PYTHONPATH`. يستخدم العامل مع `-I` الحزمة المثبّتة. لا تُورّث إلا PATH وSYSTEMROOT وLANG؛ وتكون بذرة التجزئة ثابتة. على Linux يُشتق مسار مكتبات العامل من `LIBDIR` لتثبيت Python الجاري، مما يتيح لبناءات Python القابلة للنقل العثور على libpython. لا تُنسخ قيمة `LD_LIBRARY_PATH` الموروثة أبداً. للعملية التابعة مهلة 30 ثانية يفرضها الأب ومهلة داخلية 20 ثانية، وبحد أقصى 5 ثوانٍ من الانتظار المطلوب في الخط الزمني و256 إجراءً مسجلاً. ينهي الأب تعليق الاعتماديات الأصلية عند انتهاء مهلته.

تُثبّت إضافة pytest تلقائياً. يمكن للاختبار تحميل سيناريو باستخدام `ha_scenario_tests.schema.load` واستدعاء fixture المسمّى `scenario_runner`. يولّد pytest نفسه ملف JUnit. ويمكن أيضاً استيراد `run_scenario` في شيفرة Python العادية.

</div>
