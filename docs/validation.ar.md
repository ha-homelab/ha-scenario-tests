# سجل التحقق

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


<div dir="rtl" lang="ar">

## التحقق من تشغيل Linux في 2026-10-15

نجح [تشغيل GitHub Actions رقم 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) عند الالتزام `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`، باستخدام CPython 3.14.8 على Ubuntu وإصدار Home Assistant 2026.10.0 المثبّت. اكتمل الأمر الكامل `python3 -m pytest -q` بنتيجة **نجاح 54 اختباراً خلال 21.42 ثانية**، دون تخطّي أي اختبار. يشمل ذلك اختبارات التشغيل السبعة كلها مع HA الحقيقي: أربعة سيناريوهات نموذجية، وحالة توقع/إجراء محظور تفشل عمداً، وتقرير CLI JSON المترجم، وعقد نقل الأدوار للمستهلك اللاحق. يبدأ كل اختبار تشغيل عاملاً مضبوطاً جديداً؛ وتُختبر تأكيدات الفشل المتوقع بوصفها حالات فشل، ولا تُبلّغ كسيناريوهات ناجحة.

نجحت أيضاً في التشغيل نفسه فحوص Ruff وروابط الوثائق وSVG، وبناء المصدر وwheel، وسياسة نشر المصدر، ومسح الأسرار في التاريخ الكامل. يتحقق ذلك من إرسال الخدمات الاصطناعية وسلوك الحالات تحت حارس إدخال/إخراج Python الموثّق. لا يثبت وجود صندوق أمان على مستوى نظام التشغيل، ولا يتحقق من تنفيذ Docker أو يثبت سلوك جهاز مادي.

## فحوص تطوير macOS في 2026-10-15

فُحص المصدر وقبول الإدخال الصارم وحارس تدقيق Python وترجمات CLI وإعادة توليد SVG محلياً باستخدام Python 3.14.7 على macOS arm64. نجح `python -m pytest -q -m 'not runtime'` في **47 اختباراً**؛ ويستبعد هذا الأمر صراحةً حالات HA الحقيقية السبع. نجح `python -m ruff check src tests scripts`. هذا ليس بديلاً لمجموعة اختبارات التشغيل الكاملة.

حمّل محرك Home Assistant 2026.10.0 الحقيقي مكوّنات `automation` و`blueprint` و`trace` ونفّذ سيناريوهَي انتهاء مهلة الوجود والتجاوز اليدوي، مع استدعاءات خدمات اصطناعية وحالات نهائية متوقعة ودون إدخال/إخراج محظور. ثم خرجت عملية Python المحلية بسبب خطأ تجزئة أصلي أثناء إنهاء المفسّر. يعامل المشغّل الأب هذا الخروج غير الصفري على نحو صحيح كفشل تشغيل، حتى عندما يسبقه محتوى JSON ناجح. **لا ندّعي نجاح اختبار تشغيل macOS كاملاً.**

تُشترط مجموعة Linux CI الكاملة قبل قبول الإصدار. شغّل `python -m pytest -q --junitxml=junit.xml`؛ يؤدي غياب HA أو إصداره الخاطئ أو انتهاء مهلة الابن أو خروجه غير الصفري إلى الفشل، ولا تُتخطّى هذه الحالات بصمت. التشغيل المرتبط أعلاه هو دليل Linux لهذا التنفيذ؛ تتطلب التغييرات اللاحقة تشغيلها الناجح الخاص. لا يدّعي هذا السجل تشغيل Docker أو التحقق من أجهزة مادية.

## بيانات بدء وصفية مضبوطة

يوفر العامل القيمة الاصطناعية `synthetic` لبيانات المعالج الوصفية التي يخزّنها Python مؤقتاً، ويعطّل `socket.has_ipv6` قبل استيراد HA. يمنع ذلك تهيئة منصة HA من إطلاق `uname -p`، ويمنع اختبار ربط IPv6 على localhost الذي يجريه urllib3 أثناء الاستيراد. على Linux يُستورد ifaddr تحت الحارس باستخدام `ctypes.CDLL(None)` لحل رموز libc المحمّلة بالفعل في العملية؛ وبذلك تُتجنب عملية `ldconfig` الفرعية التي يطلقها باحث المكتبات. يُستعاد باحث المكتبات العادي فوراً. لا يحتوي حارس الإدخال/الإخراج على استثناء في قائمة السماح لهذه العمليات. تؤثر هذه التغييرات فقط على بيانات المضيف الوصفية واستكشافه؛ أما مشغّلات HA وشروطه ومؤقّتاته وإعادة تحميله وبرامجه النصية وإرسال خدماته فحقيقية. وهي حساسة للإصدار وتغطيها مجموعة اختبارات التشغيل المثبّتة.

## إعادة الإنتاج

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

<div dir="rtl" lang="ar">

لا يثبت أي تقرير حالة مرحّل حقيقية أو تسليم اتصال لاسلكي أو دقة الوجود في المنزل أو التوقيت بمدد الإنتاج. يعرض الخط الزمني SVG توقعات اصطناعية لا قياسات أداء معيارية.

تتضمن مجموعة التشغيل أيضاً `tests/fixtures/role_transfer.json`، وهو العقد الاصطناعي للمستهلك اللاحق: يُطفأ الدور الحالي ويظل المقبس المتقاعد قيد التشغيل. هذا ليس اختبار نقل حمل مادي.

</div>
