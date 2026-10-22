# स्थापना और अलगाव

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

Python 3.14.2–3.14.x के साथ तय संस्करण वाला Home Assistant रनटाइम इस्तेमाल करें। मूल README के अनुसार पहले `--require-hashes` से `requirements.lock` स्थापित करें, फिर `--no-deps .` से यह पैकेज स्थापित करें। लॉक फ़ाइल में अनुप्रयोग और परीक्षण की निर्भरताएँ शामिल हैं। साफ़ वातावरण ज़रूरी है; इसे अपने उत्पादन Home Assistant वातावरण में स्थापित न करें। स्रोत संपादित करते समय इसके बजाय `pip install --no-deps -e .` इस्तेमाल करें।

पहले `ha-scenario validate examples/stale_sensor.json` चलाएँ। सत्यापन HA रनटाइम आयात नहीं करता। फिर `ha-scenario run examples/stale_sensor.json --report result.json` चलाएँ। कोई लक्ष्य सर्वर कॉन्फ़िगर नहीं किया जाता। एकमात्र आउटपुट पथ आपके स्पष्ट `--report` तर्क से आता है, परिदृश्य से नहीं।

अधिक मज़बूत नेटवर्क सीमा के लिए:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

बिल्ड को निर्भरताओं के लिए इंटरनेट चाहिए। रन के दौरान नेटवर्क नहीं होता और लिखने योग्य `/tmp` अस्थायी होता है; घर की कॉन्फ़िगरेशन, Docker सॉकेट या क्रेडेंशियल माउंट नहीं किए जाते। यह वैकल्पिक परिनियोजन विधि है; यही कंटेनर वास्तव में चलाया गया था या नहीं, सत्यापन रिकॉर्ड में देखें। होस्ट नेटवर्किंग या उत्पादन माउंट न जोड़ें।

उपप्रक्रिया इंटरफ़ेस विरासत में मिले क्रेडेंशियल और `PYTHONPATH` हटाता है। वर्कर का `-I` स्थापित पैकेज इस्तेमाल करता है। केवल PATH, SYSTEMROOT और LANG विरासत में आते हैं; हैश बीज स्थिर है। Linux पर वर्कर का लाइब्रेरी पथ चल रहे Python की स्थापना के `LIBDIR` से निकाला जाता है, ताकि स्थानांतरित किए जा सकने वाले Python बिल्ड libpython खोज सकें। विरासत में मिला `LD_LIBRARY_PATH` कभी कॉपी नहीं होता। चाइल्ड पर पैरेंट की 30 सेकंड की समयसीमा और अंदरूनी 20 सेकंड की समयसीमा है; टाइमलाइन में माँगा गया कुल इंतज़ार अधिकतम 5 सेकंड और रिकॉर्ड की गई क्रियाएँ अधिकतम 256 हैं। नेटिव निर्भरता अटकने पर पैरेंट की समयसीमा उसे समाप्त करती है।

pytest प्लगइन अपने आप स्थापित होता है। परीक्षण `ha_scenario_tests.schema.load` से परिदृश्य लोड कर सकता है और `scenario_runner` fixture बुला सकता है। JUnit स्वयं pytest बनाता है। सामान्य Python में भी `run_scenario` आयात किया जा सकता है।
