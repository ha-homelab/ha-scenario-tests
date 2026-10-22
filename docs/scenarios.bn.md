# দৃশ্যপট চুক্তি v1

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

প্রামাণ্য যাচাইকারী হলো `src/ha_scenario_tests/schema.py`। শুধু JSON, সর্বোচ্চ 64 KiB। অজানা কী, একই JSON কী একাধিকবার, সিমলিংক ইনপুট, অসীম বা অ-সসীম সংখ্যা এবং অবৈধ টাইপ বাতিল হয়। বাড়ির কনফিগারেশন প্রকাশ্য উদাহরণে কপি করবেন না।

বাধ্যতামূলক মূল ফিল্ড: `schema: "ha-scenario/v1"`, ছোট হাতের অক্ষরে সংক্ষিপ্ত `name`, `seed`, `automations`, `timeline`, `expect`। ঐচ্ছিক `settle_seconds`-এর ডিফল্ট 0.1। সব সত্তার ID-তে `scenario_` উপসর্গ থাকতে হবে এবং প্রাথমিক ডেটায় ঘোষণা করতে হবে। সমর্থিত ডোমেন: `light`, `switch`, `input_boolean`, `binary_sensor`। সমর্থিত অবস্থা: `on`, `off`, `unknown`, `unavailable`।

অটোমেশনে `id`, `triggers`, `actions` এবং ঐচ্ছিক `conditions` ও `mode` (`single` অথবা `restart`) থাকে। অবস্থা-ট্রিগারে `trigger`, `entity_id`, `to` লাগে; `from` ও `for_seconds` ঐচ্ছিক। ইভেন্ট ট্রিগার `trigger: "event"` ও `event_type: "scenario_name"` ব্যবহার করে; `automation_reloaded`-ও সমর্থিত। শর্ত শুধুই অবস্থার তুলনা। কাজে `action` ও একটি `entity_id` থাকে: প্রাথমিকভাবে ঘোষিত light/switch/input_boolean সত্তায় `turn_on`, `turn_off`, `toggle`। টেমপ্লেট, সিলেক্টর, ডিভাইসের কাজ, ব্লুপ্রিন্ট, ডিস্কের স্ক্রিপ্ট বা সার্ভিস ডেটা অনুমোদিত নয়।

টাইমলাইনের ধাপে `after` (আগের ধাপ শেষ হওয়ার পর আপেক্ষিক সেকেন্ড) এবং ঠিক একটি কাজ থাকে:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

অন্যান্য কাজ: `"event": "scenario_manual_off"` অথবা `"reload": true`। রিলোড HA-এর বাস্তব অটোমেশন সার্ভিস ডাকে, যা তৈরি করা অস্থায়ী `configuration.yaml` পড়ে; পরীক্ষা সমাপ্তির ইভেন্ট পাঠিয়ে রিলোড অনুকরণ করে না।

`expect.calls` হলো পুনরাবৃত্তিসহ `{action, entity_id}` রেকর্ডের হুবহু ক্রমযুক্ত তালিকা; ফাঁকা তালিকা অ্যাকচুয়েটরের সব কল নিষিদ্ধ করে। ঐচ্ছিক `expect.forbidden` কখনো ঘটতে দেওয়া যাবে না এমন কল তালিকাভুক্ত করে। `expect.states` প্রাথমিক ID-কে শেষ অবস্থার সঙ্গে মেলায়। শেষ অবস্থা কাকতালীয়ভাবে মিললেও অপ্রত্যাশিত কল ব্যর্থতা ঘটায়।

সীমা: ৬৪টি প্রাথমিক সত্তা, ১৬টি অটোমেশন, প্রতিটি অটোমেশনে ৮টি ট্রিগার ও ৮টি শর্ত, প্রতিটিতে ১৬টি কাজ, ৩২টি টাইমলাইন ধাপ, মোট ৫ সেকেন্ড চাওয়া অপেক্ষা, ২৫৬টি রেকর্ড করা কল। ব্যাকগ্রাউন্ড কাজের ত্রুটি ও অবরুদ্ধ I/O রান ব্যর্থ করে। রিপোর্টে একমুখী ঘড়িতে কল/ধাপের অতিবাহিত সময়, লোড করা উপাদান, শেষ অবস্থা ও ব্যর্থতার কোড থাকে।

প্যারেন্ট ফেরত দেওয়ার আগে ওয়ার্কারের পুরো রিপোর্ট যাচাই করে। `passed` সত্যিই Boolean টাইপ হতে হবে, `physical_validation` false হতে হবে এবং স্কিমা, HA সংস্করণ, দৃশ্যপটের নাম, ফিল্ড ও সীমানা প্রোটোকলের সঙ্গে মিলতে হবে। প্যারেন্ট শুধু সফলতার ফ্ল্যাগ বিশ্বাস না করে দৃশ্যপট অনুযায়ী কল/অবস্থার assertion-ও যাচাই করে। অবৈধ আউটপুট ও ওয়ার্কারের যেকোনো অশূন্য exit রানটাইম ত্রুটি, এমনকি চাইল্ড সফল দেখায় এমন JSON অবজেক্ট ছাপালেও।

সরবরাহ করা পুরোনো ডেটার উদাহরণ `unavailable` দিয়ে পরিবহন সংযোগ হারানো বোঝায়। এটি `last_changed` থেকে উৎসের সতেজতা অনুমান করে না, সেন্সরের টাইমস্ট্যাম্প পার্সিং পরীক্ষা করে না বা বাস্তব সেন্সরের মেয়াদোত্তীর্ণ আচরণ প্রমাণ করে না। ম্যানুয়াল ওভাররাইড একটি স্পষ্ট কৃত্রিম নীতি; টুল বিদ্যমান অটোমেশনে ওই নীতি যোগ করে না।
