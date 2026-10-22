# सत्यापन रिकॉर्ड

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

## 2026-10-15 Linux रनटाइम सत्यापन

[GitHub Actions रन 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) कमिट `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` पर सफल हुआ, जिसमें Ubuntu पर CPython 3.14.8 और तय Home Assistant 2026.10.0 इस्तेमाल हुआ। पूरा आदेश `python3 -m pytest -q` **21.42 सेकंड में 54 सफल परीक्षणों** के साथ पूरा हुआ; कोई परीक्षण छोड़ा नहीं गया। इसमें वास्तविक HA के सातों रनटाइम परीक्षण शामिल हैं: चार उदाहरण परिदृश्य, जानबूझकर विफल होने वाला अपेक्षा/निषिद्ध क्रिया मामला, स्थानीयकृत CLI JSON रिपोर्ट और नीचे के उपभोक्ता का भूमिका-हस्तांतरण अनुबंध। हर रनटाइम परीक्षण नया नियंत्रित वर्कर शुरू करता है; अपेक्षित विफलता अभिकथन विफलता के रूप में जाँचे जाते हैं, सफल परिदृश्य नहीं बताए जाते।

उसी रन में Ruff, दस्तावेज़ लिंक/SVG जाँच, स्रोत और wheel बिल्ड, स्रोत प्रकाशन नीति और पूरे इतिहास का सीक्रेट स्कैन भी सफल हुए। यह लिखित Python I/O गार्ड के अंतर्गत कृत्रिम सेवा प्रेषण और स्थिति व्यवहार सत्यापित करता है। इससे OS सुरक्षा सैंडबॉक्स स्थापित होना, Docker निष्पादन या भौतिक डिवाइस व्यवहार सिद्ध नहीं होता।

## 2026-10-15 macOS विकास जाँच

स्रोत, सख़्त इनपुट स्वीकृति, Python ऑडिट गार्ड, CLI अनुवाद और SVG पुनर्निर्माण macOS arm64 पर Python 3.14.7 से स्थानीय रूप से जाँचे गए। `python -m pytest -q -m 'not runtime'` के **47 परीक्षण** सफल हुए; यह आदेश वास्तविक HA के सात मामले स्पष्ट रूप से अलग रखता है। `python -m ruff check src tests scripts` सफल हुआ। यह पूरी रनटाइम परीक्षण शृंखला का विकल्प नहीं है।

वास्तविक Home Assistant 2026.10.0 इंजन ने `automation`, `blueprint` और `trace` लोड किए तथा मौजूदगी समयसीमा और मैनुअल ओवरराइड परिदृश्य अपेक्षित कृत्रिम सेवा कॉल, अंतिम स्थितियों और बिना रोके गए I/O के चलाए। इसके बाद स्थानीय Python प्रक्रिया इंटरप्रेटर समापन के दौरान नेटिव segmentation fault से निकली। पैरेंट रनर इस गैर-शून्य निकास को सही ढंग से रनटाइम विफलता मानता है, भले पहले सफल JSON डेटा आया हो। **पूरा macOS रनटाइम परीक्षण सफल होने का दावा नहीं है।**

रिलीज़ स्वीकारने से पहले पूरी Linux CI शृंखला ज़रूरी है। `python -m pytest -q --junitxml=junit.xml` चलाएँ; HA का न होना, गलत HA संस्करण, चाइल्ड समयसीमा समाप्त होना और गैर-शून्य चाइल्ड निकास विफल होते हैं, चुपचाप छोड़े नहीं जाते। ऊपर लिंक किया रन इस कार्यान्वयन का Linux प्रमाण है; बाद के बदलावों को अपना सफल रन चाहिए। इस रिकॉर्ड में Docker रन या भौतिक डिवाइस सत्यापन का दावा नहीं है।

## नियंत्रित बूटस्ट्रैप मेटाडेटा

वर्कर Python के कैश किए प्रोसेसर मेटाडेटा में कृत्रिम मान `synthetic` देता है और HA आयात से पहले `socket.has_ipv6` बंद करता है। इससे HA का प्लेटफ़ॉर्म आरंभीकरण `uname -p` नहीं चलाता और urllib3 आयात के समय localhost IPv6 bind जाँच नहीं करता। Linux पर ifaddr को गार्ड के अंतर्गत `ctypes.CDLL(None)` से आयात किया जाता है, जो प्रक्रिया में पहले से लोड libc प्रतीक हल करता है; इससे लाइब्रेरी खोजकर्ता की `ldconfig` उपप्रक्रिया नहीं चलती। सामान्य लाइब्रेरी खोजकर्ता तुरंत बहाल होता है। इन क्रियाओं के लिए I/O गार्ड में अनुमति-सूची का कोई अपवाद नहीं है। ये बदलाव केवल होस्ट मेटाडेटा/जाँच प्रभावित करते हैं; HA ट्रिगर, शर्तें, टाइमर, रीलोड, स्क्रिप्ट और सेवा प्रेषण वास्तविक हैं। ये संस्करण-संवेदी हैं और तय रनटाइम परीक्षण शृंखला इन्हें जाँचती है।

## पुनरुत्पादन

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

कोई रिपोर्ट वास्तविक रिले स्थिति, रेडियो वितरण, घरेलू मौजूदगी की सटीकता या उत्पादन अवधि के समय व्यवहार को सिद्ध नहीं करती। SVG टाइमलाइन कृत्रिम अपेक्षाएँ दिखाती है, बेंचमार्क माप नहीं।

रनटाइम शृंखला में `tests/fixtures/role_transfer.json` भी है, जो नीचे के उपभोक्ता का कृत्रिम अनुबंध है: मौजूदा भूमिका बंद होती है और हटाया गया प्लग चालू रहता है। यह भौतिक लोड हस्तांतरण परीक्षण नहीं है।
