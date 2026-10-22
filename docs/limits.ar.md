# النطاق والأدلة

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


<div dir="rtl" lang="ar">

يتحقق هذا الإصدار من مجموعة فرعية محدودة باستخدام مشغّلات Home Assistant الحقيقية وشروطه ومؤقّتاته وإعادة التحميل وإرسال إجراءات البرامج النصية. مستقبلات أوامر المشغّلات المادية وحالات الإدخال اصطناعية. لا يثبت ذلك بروتوكولات الاتصال أو استهلاك التيار أو دقة المستشعر أو الحالة المادية للمرحّل أو السلامة أو سلوك كل إعداد ممكن لـ HA.

تُقاس المدة الفعلية بساعة رتيبة. تستخدم الاختبارات عمداً فترات قصيرة وهامشاً للجدولة. لا نعدّل طرق التأخير الداخلية في HA، ولا نغيّر مدد مؤقّتات الإنتاج، ولا ندّعي التكافؤ مع الزمن الافتراضي. التوقيت الصيفي والجدولة وفق وقت الساعة وإعادة تشغيل عملية HA بالكامل واستمرارية Recorder خارج نطاق v1. تُختبر إعادة التحميل؛ وهي ليست إعادة تشغيل للعملية.

لا يتضمن الإدخال قوالب قابلة للتنفيذ أو إعدادات تكامل. يستخدم كل عامل دليلاً مؤقتاً نظيفاً وبيئةً منقّاة وحارس تدقيق عاماً. يمنع ذلك عمليات إدخال/إخراج Python العرضية للشبكة أو العمليات الفرعية عبر المسار المسموح. وليس صندوق عزل للشيفرة العدائية: تُعد اعتماديات Python والاعتماديات الأصلية والمفسّر والمضيف موثوقة. لا تشغّل مصادر أو اعتماديات غير موثوقة إلا في بيئة مؤمّنة على نحو مستقل. تقوّي وصفة Docker الاختيارية network-none العزل الشبكي، لكنها لا تثبت سلوك العتاد.

ينبغي أن تحتوي التقارير العامة على تجهيزات اختبار اصطناعية فقط. تكشف الخطوط الزمنية للحالات الحقيقية عن الوجود في المنزل والعادات حتى دون رمز وصول. لا توجد هنا قوائم أجهزة منزلية أو تسجيلات أو إعدادات إنتاج. جميع المخططات موسومة بأنها اصطناعية وقابلة لإعادة التوليد باستخدام `python scripts/render_diagrams.py`.

راجع [التحقق](validation.ar.md) للاطلاع على الفحوص المقاسة التي أُجريت على هذا الإصدار. يقتصر دعم التثبيت على البيئات المذكورة في ذلك السجل؛ وصفة الحاوية لا تعني اختبار كل منصة.

</div>
