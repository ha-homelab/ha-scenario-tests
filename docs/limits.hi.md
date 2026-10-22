# दायरा और प्रमाण

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

यह संस्करण वास्तविक Home Assistant ट्रिगर, शर्तें, टाइमर, रीलोड और स्क्रिप्ट क्रिया प्रेषण के साथ एक सीमित उपसमुच्चय सत्यापित करता है। ऐक्चुएटर के प्राप्तकर्ता और इनपुट स्थितियाँ कृत्रिम हैं। इससे संचार प्रोटोकॉल, विद्युत धारा खपत, सेंसर की सटीकता, रिले की भौतिक स्थिति, सुरक्षा या हर संभव HA कॉन्फ़िगरेशन का व्यवहार सिद्ध नहीं होता।

घड़ी वास्तविक बीते हुए एकदिश समय को मापती है। परीक्षण जानबूझकर छोटे अंतराल और शेड्यूलिंग की गुंजाइश रखते हैं। हम HA की अंदरूनी विलंब विधियों को पैच नहीं करते, उत्पादन टाइमर की अवधि नहीं बदलते और आभासी समय से समतुल्यता का दावा नहीं करते। डे-लाइट सेविंग, वास्तविक घड़ी के समय पर शेड्यूलिंग, पूरी HA प्रक्रिया को पुनः शुरू करना और Recorder की स्थायी संग्रहण क्षमता v1 के बाहर हैं। रीलोड का परीक्षण होता है; वह प्रक्रिया पुनः शुरू करना नहीं है।

इनपुट में चलाए जा सकने वाले टेम्पलेट या इंटीग्रेशन कॉन्फ़िगरेशन नहीं है। हर वर्कर साफ़ अस्थायी निर्देशिका, छँटा हुआ वातावरण और वैश्विक ऑडिट गार्ड इस्तेमाल करता है। इससे स्वीकृत पथ से अनजाने में होने वाला Python नेटवर्क/उपप्रक्रिया I/O रुकता है। यह दुर्भावनापूर्ण कोड का सैंडबॉक्स नहीं है: Python/नेटिव निर्भरताएँ, इंटरप्रेटर और होस्ट विश्वसनीय माने जाते हैं। अविश्वसनीय स्रोत या निर्भरताएँ केवल अलग सुरक्षित वातावरण में चलाएँ। वैकल्पिक Docker network-none विधि नेटवर्क अलगाव मज़बूत करती है, पर हार्डवेयर व्यवहार सिद्ध नहीं करती।

सार्वजनिक रिपोर्ट में केवल कृत्रिम fixture होने चाहिए। वास्तविक स्थिति की टाइमलाइन बिना टोकन भी घर में मौजूदगी और आदतें उजागर करती है। यहाँ घरेलू उपकरणों की सूची, रिकॉर्डिंग या उत्पादन कॉन्फ़िगरेशन नहीं है। सभी आरेख कृत्रिम चिह्नित हैं और `python scripts/render_diagrams.py` से फिर बनाए जा सकते हैं।

इस संस्करण पर किए गए मापित परीक्षणों के लिए [सत्यापन](validation.hi.md) देखें। स्थापना समर्थन उसी रिकॉर्ड के वातावरणों तक सीमित है; कंटेनर विधि का अर्थ यह नहीं कि हर प्लेटफ़ॉर्म जाँचा गया है।
