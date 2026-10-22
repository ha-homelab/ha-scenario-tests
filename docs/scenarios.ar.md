# عقد السيناريو v1

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


<div dir="rtl" lang="ar">

أداة التحقق المرجعية هي `src/ha_scenario_tests/schema.py`. يُقبل JSON فقط، بحد أقصى 64 KiB. تُرفض المفاتيح غير المعروفة ومفاتيح JSON المكررة ومدخلات الروابط الرمزية والأعداد غير المنتهية والأنواع غير الصالحة. لا تنسخ إعدادات المنزل إلى الأمثلة العامة.

حقول الجذر المطلوبة: `schema: "ha-scenario/v1"`، و`name` قصير بأحرف صغيرة، و`seed`، و`automations`، و`timeline`، و`expect`. القيمة الافتراضية للحقل الاختياري `settle_seconds` هي 0.1. تستخدم جميع معرّفات الكيانات البادئة `scenario_` ويجب التصريح بها في البيانات الأولية. المجالات المدعومة: `light`، و`switch`، و`input_boolean`، و`binary_sensor`. الحالات المدعومة: `on`، و`off`، و`unknown`، و`unavailable`.

تحتوي الأتمتة على `id` و`triggers` و`actions`، واختيارياً `conditions` و`mode` (`single` أو `restart`). تتطلب مشغّلات الحالة `trigger` و`entity_id` و`to`، واختيارياً `from` و`for_seconds`. تستخدم مشغّلات الأحداث `trigger: "event"` و`event_type: "scenario_name"`؛ ويُدعم أيضاً `automation_reloaded`. تقتصر الشروط على مقارنات الحالات. تحتوي الإجراءات على `action` و`entity_id` واحد: `turn_on` أو `turn_off` أو `toggle` لكيانات light/switch/input_boolean المعرّفة أولياً. لا يُسمح بالقوالب أو المحدّدات أو إجراءات الأجهزة أو المخططات الجاهزة أو البرامج النصية من القرص أو بيانات الخدمات.

تحتوي خطوات الخط الزمني على `after` (ثوانٍ نسبية منذ اكتمال الخطوة السابقة) وعلى عملية واحدة بالضبط:

</div>

<div dir="ltr">

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

</div>

<div dir="rtl" lang="ar">

العمليات الأخرى: `"event": "scenario_manual_off"` أو `"reload": true`. تستدعي إعادة التحميل خدمة الأتمتة الحقيقية في HA، التي تقرأ ملف `configuration.yaml` المؤقت المُولّد؛ لا يقلّد الاختبار إعادة التحميل بإطلاق حدث اكتمالها.

يمثّل `expect.calls` القائمة المرتبة الدقيقة لسجلات `{action, entity_id}`، بما فيها التكرارات؛ تمنع القائمة الفارغة جميع استدعاءات المشغّلات. يسرد `expect.forbidden` اختيارياً الاستدعاءات التي يجب ألا تحدث أبداً. يربط `expect.states` المعرّفات الأولية بالحالات النهائية. تسبب الاستدعاءات غير المتوقعة الفشل حتى لو وافقت الحالة النهائية المطلوب بالمصادفة.

الحدود: 64 كياناً أولياً، و16 أتمتة، و8 مشغّلات و8 شروط لكل أتمتة، و16 إجراءً لكل أتمتة، و32 خطوة زمنية، و5 ثوانٍ إجمالية للانتظار المطلوب، و256 استدعاءً مسجلاً. تؤدي أخطاء مهام الخلفية وعمليات الإدخال/الإخراج المحظورة إلى فشل التشغيل. يتضمن التقرير أزمنة الاستدعاءات والخطوات المنقضية بالساعة الرتيبة، والمكوّنات المحمّلة، والحالات النهائية، ورموز الفشل.

يتحقق الأب من تقرير العامل كاملاً قبل إرجاعه. يجب أن يكون `passed` من النوع المنطقي فعلاً، وأن تكون `physical_validation` بقيمة false، وأن يطابق المخطط وإصدار HA واسم السيناريو والحقول والحدود البروتوكول. يتحقق الأب أيضاً من تأكيدات الاستدعاءات والحالات مقابل السيناريو بدلاً من الثقة بعلم النجاح. يُعد الإخراج غير الصالح وأي خروج للعامل برمز غير صفري خطأً أثناء التشغيل، حتى لو طبع الابن كائن JSON يبدو ناجحاً.

يمثّل مثال البيانات القديمة المرفق فقدان النقل بواسطة `unavailable`. لا يستنتج حداثة المصدر من `last_changed`، ولا يختبر تحليل الطوابع الزمنية للمستشعر أو يثبت سلوك انتهاء صلاحية المستشعر الحقيقي. التجاوز اليدوي سياسة اصطناعية صريحة؛ ولا تضيف الأداة تلك السياسة إلى أتمتة موجودة.

</div>
