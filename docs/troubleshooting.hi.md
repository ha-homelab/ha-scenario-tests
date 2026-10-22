# समस्या निवारण

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

- स्थापना/रन में निकास 2: Python 3.14.2–3.14.x, HA का ठीक वही तय संस्करण और साफ़ वर्चुअल वातावरण जाँचें। रनर अन्य HA संस्करण अस्वीकार करता है। विफलता बताने से पहले लॉक से पुनः स्थापित करें।
- वर्कर विफल/समय समाप्त: निर्भरता आयात या HA सेटअप विफल हुआ। स्थानीय traceback पाने के लिए पृथक वर्कर को **कृत्रिम** फ़ाइल के साथ सीधे चलाएँ: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`। बिना समीक्षा के वातावरण निदान सार्वजनिक न करें।
- `calls_mismatch`: केवल अंतिम स्थिति नहीं, क्रम और दोहराए गए कॉल की तुलना करें। आरंभिक स्थितियाँ शुरुआत से पहले लगाई जाती हैं; वे शुरुआत के बाद नया स्थिति ट्रिगर अपने आप नहीं मानी जातीं।
- `forbidden_call`: रिकॉर्ड किया कृत्रिम ऐक्चुएटर आदेश निषेध अनुबंध से मेल खाया। यह वास्तविक ऑटोमेशन प्रेषण है, भौतिक संचालन नहीं।
- `states_mismatch`: टाइमलाइन असाइनमेंट या कृत्रिम ऐक्चुएटर ने अलग स्थिति छोड़ी।
- `blocked_io` या `background_exception`: हरा परिणाम पाने के लिए गार्ड कभी बंद न करें। यह संस्करण नेटवर्क इंटीग्रेशन स्वीकार नहीं करता। कृत्रिम पुनरुत्पादन और संस्करण बताएँ।
- अस्थिर टाइमर परीक्षण: स्थिति बदलाव और जाँची गई समयसीमा के बीच अंतर बढ़ाएँ। वास्तविक इवेंट-लूप शेड्यूलिंग मापी जाती है; आभासी घड़ी या माइक्रोसेकंड-सटीक शेड्यूलिंग का वादा नहीं है।
- रीलोड: वास्तविक रीलोड `for` टाइमर रद्द कर सकता है। नीति में रिकवरी ज़रूरी हो तो स्पष्ट सामंजस्य ऑटोमेशन चाहिए; `reload_reconcile.json` से तुलना करें।
- मौजूदा रिपोर्ट: `--report` जानबूझकर उस पर लिखना अस्वीकार करता है। नया पथ चुनें।

गैर-संपादन योग्य स्थापना के बाद स्रोत ट्री इस्तेमाल कर रहे हों तो बदलाव जाँचने से पहले पैकेज पुनः स्थापित करें। विकास के लिए `--no-deps -e .` से स्थापित करें।
