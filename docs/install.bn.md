# ইনস্টলেশন ও বিচ্ছিন্নতা

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

Python 3.14.2–3.14.x-এর সঙ্গে নির্দিষ্ট সংস্করণের Home Assistant রানটাইম ব্যবহার করুন। মূল README অনুযায়ী প্রথমে `--require-hashes` দিয়ে `requirements.lock` ইনস্টল করুন, তারপর `--no-deps .` দিয়ে এই প্যাকেজটি ইনস্টল করুন। লক ফাইলে অ্যাপ্লিকেশন ও পরীক্ষার নির্ভরতাগুলি অন্তর্ভুক্ত। পরিষ্কার পরিবেশ প্রয়োজন; চলমান উৎপাদন Home Assistant পরিবেশে ইনস্টল করবেন না। সোর্স সম্পাদনার সময় পরিবর্তে `pip install --no-deps -e .` ব্যবহার করুন।

প্রথমে `ha-scenario validate examples/stale_sensor.json` চালান। যাচাই HA রানটাইম ইমপোর্ট করে না। এরপর `ha-scenario run examples/stale_sensor.json --report result.json` চালান। কোনো লক্ষ্য সার্ভার কনফিগার করা হয় না। একমাত্র আউটপুট পাথ আসে আপনার স্পষ্ট `--report` আর্গুমেন্ট থেকে, দৃশ্যপট থেকে নয়।

আরও শক্তিশালী নেটওয়ার্ক সীমানার জন্য:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

বিল্ডের সময় নির্ভরতা পেতে ইন্টারনেট লাগে। চালানোর সময় নেটওয়ার্ক থাকে না এবং লেখার উপযোগী `/tmp` সাময়িক ও একবারের ব্যবহারযোগ্য; বাড়ির কনফিগারেশন, Docker সকেট বা পরিচয়পত্র মাউন্ট করা হয় না। এটি ঐচ্ছিক স্থাপনার পদ্ধতি; ঠিক এই কনটেইনারটি চালানো হয়েছিল কি না যাচাইয়ের নথিতে দেখুন। হোস্ট নেটওয়ার্কিং বা উৎপাদন পরিবেশের মাউন্ট যোগ করবেন না।

সাবপ্রসেস ইন্টারফেস উত্তরাধিকারসূত্রে পাওয়া পরিচয়পত্র ও `PYTHONPATH` সরিয়ে দেয়। ওয়ার্কারের `-I` ইনস্টল করা প্যাকেজ ব্যবহার করে। শুধু PATH, SYSTEMROOT ও LANG উত্তরাধিকারসূত্রে আসে; হ্যাশ সিড নির্দিষ্ট থাকে। Linux-এ ওয়ার্কারের লাইব্রেরি পাথ চলমান Python ইনস্টলেশনের `LIBDIR` থেকে নির্ধারিত হয়, ফলে স্থানান্তরযোগ্য Python বিল্ডও libpython খুঁজে পায়। উত্তরাধিকারসূত্রে পাওয়া `LD_LIBRARY_PATH` কখনো কপি করা হয় না। চাইল্ডের জন্য প্যারেন্টের ৩০ সেকেন্ড এবং ভেতরে ২০ সেকেন্ডের সময়সীমা থাকে; টাইমলাইনে মোট চাওয়া অপেক্ষা সর্বোচ্চ ৫ সেকেন্ড এবং রেকর্ড করা কাজ সর্বোচ্চ ২৫৬টি। নেটিভ নির্ভরতা আটকে গেলে প্যারেন্টের সময়সীমা সেটি বন্ধ করে।

pytest প্লাগইন স্বয়ংক্রিয়ভাবে ইনস্টল হয়। পরীক্ষা `ha_scenario_tests.schema.load` দিয়ে দৃশ্যপট লোড করে `scenario_runner` fixture ডাকতে পারে। JUnit নিজে pytest তৈরি করে। সাধারণ Python কোডেও `run_scenario` ইমপোর্ট করা যায়।
