# परिदृश्य अनुबंध v1

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

प्रामाणिक सत्यापक `src/ha_scenario_tests/schema.py` है। केवल JSON, अधिकतम 64 KiB स्वीकार है। अनजान कुंजियाँ, दोहराई गई JSON कुंजियाँ, प्रतीकात्मक लिंक वाला इनपुट, गैर-परिमित संख्याएँ और अमान्य प्रकार अस्वीकार होते हैं। घरेलू कॉन्फ़िगरेशन सार्वजनिक उदाहरणों में कॉपी न करें।

अनिवार्य मूल फ़ील्ड: `schema: "ha-scenario/v1"`, छोटा लोअरकेस `name`, `seed`, `automations`, `timeline`, `expect`। वैकल्पिक `settle_seconds` का डिफ़ॉल्ट 0.1 है। सभी इकाई ID `scenario_` उपसर्ग इस्तेमाल करते हैं और आरंभिक डेटा में घोषित होने चाहिए। समर्थित डोमेन: `light`, `switch`, `input_boolean`, `binary_sensor`। समर्थित स्थितियाँ: `on`, `off`, `unknown`, `unavailable`।

ऑटोमेशन में `id`, `triggers`, `actions` और वैकल्पिक `conditions` तथा `mode` (`single` या `restart`) होते हैं। स्थिति ट्रिगर के लिए `trigger`, `entity_id`, `to` आवश्यक हैं; `from` और `for_seconds` वैकल्पिक हैं। इवेंट ट्रिगर `trigger: "event"` और `event_type: "scenario_name"` इस्तेमाल करते हैं; `automation_reloaded` भी समर्थित है। शर्तें केवल स्थिति तुलना हैं। क्रियाओं में `action` और एक `entity_id` होता है: आरंभिक light/switch/input_boolean इकाइयों पर `turn_on`, `turn_off`, `toggle`। टेम्पलेट, चयनकर्ता, डिवाइस क्रियाएँ, ब्लूप्रिंट, डिस्क की स्क्रिप्ट या सेवा डेटा स्वीकार नहीं हैं।

टाइमलाइन चरणों में `after` (पिछला चरण पूरा होने से सापेक्ष सेकंड) और ठीक एक क्रिया होती है:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

अन्य क्रियाएँ: `"event": "scenario_manual_off"` या `"reload": true`। रीलोड HA की वास्तविक ऑटोमेशन सेवा बुलाता है, जो बनाई गई अस्थायी `configuration.yaml` पढ़ती है; परीक्षण पूर्णता इवेंट भेजकर रीलोड की नकल नहीं करता।

`expect.calls`, दोहराव सहित `{action, entity_id}` रिकॉर्ड की सटीक क्रमबद्ध सूची है; खाली सूची सभी ऐक्चुएटर कॉल मना करती है। वैकल्पिक `expect.forbidden` उन कॉल को सूचीबद्ध करता है जो कभी नहीं होने चाहिए। `expect.states` आरंभिक ID को अंतिम स्थिति से जोड़ता है। अनपेक्षित कॉल विफलता लाते हैं, भले अंतिम स्थिति संयोग से मिल जाए।

सीमाएँ: 64 आरंभिक इकाइयाँ, 16 ऑटोमेशन, हर ऑटोमेशन में 8 ट्रिगर और 8 शर्तें, हर ऑटोमेशन में 16 क्रियाएँ, 32 टाइमलाइन चरण, कुल 5 सेकंड अनुरोधित इंतज़ार, 256 रिकॉर्ड किए गए कॉल। बैकग्राउंड कार्य की त्रुटियाँ और रोका गया I/O रन विफल करते हैं। रिपोर्ट में एकदिश घड़ी से कॉल/चरण का बीता समय, लोड किए गए घटक, अंतिम स्थितियाँ और विफलता कोड होते हैं।

पैरेंट लौटाने से पहले वर्कर की पूरी रिपोर्ट सत्यापित करता है। `passed` वास्तव में Boolean प्रकार होना चाहिए, `physical_validation` false होना चाहिए, और स्कीमा, HA संस्करण, परिदृश्य नाम, फ़ील्ड तथा सीमाएँ प्रोटोकॉल से मेल खाने चाहिए। पैरेंट सफलता फ़्लैग पर भरोसा करने के बजाय परिदृश्य के अनुसार कॉल/स्थिति अभिकथन भी जाँचता है। अमान्य आउटपुट और वर्कर का कोई भी गैर-शून्य निकास रनटाइम त्रुटि है, भले चाइल्ड ने सफल दिखता JSON ऑब्जेक्ट छापा हो।

दिया गया पुरानी जानकारी का उदाहरण `unavailable` से संचार टूटना दर्शाता है। यह `last_changed` से स्रोत की ताज़गी नहीं निकालता, सेंसर टाइमस्टैम्प पार्सिंग नहीं जाँचता और वास्तविक सेंसर के एक्सपायर होने का व्यवहार सिद्ध नहीं करता। मैनुअल ओवरराइड स्पष्ट कृत्रिम नीति है; उपकरण यह नीति मौजूदा ऑटोमेशन में नहीं जोड़ता।
