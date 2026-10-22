# সমস্যা সমাধান

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

- ইনস্টলেশন/রানের সময় exit ২: Python 3.14.2–3.14.x, HA-এর ঠিক নির্দিষ্ট সংস্করণ এবং পরিষ্কার ভার্চুয়াল পরিবেশ যাচাই করুন। রানার অন্য HA সংস্করণ বাতিল করে। ব্যর্থতা জানানোর আগে লক ফাইল থেকে পুনরায় ইনস্টল করুন।
- ওয়ার্কারের ব্যর্থতা/সময় শেষ: নির্ভরতা ইমপোর্ট বা HA সেটআপ ব্যর্থ হয়েছে। স্থানীয় traceback পেতে বিচ্ছিন্ন ওয়ার্কার সরাসরি **কৃত্রিম** ফাইল দিয়ে চালান: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`। পর্যালোচনা না করা পরিবেশের রোগনির্ণয় তথ্য প্রকাশ করবেন না।
- `calls_mismatch`: শুধু শেষ অবস্থা নয়, ক্রম ও পুনরাবৃত্ত কল তুলনা করুন। প্রাথমিক অবস্থা চালুর আগে নির্ধারিত হয়; চালুর পরে তা স্বয়ংক্রিয়ভাবে নতুন অবস্থা-ট্রিগার গণ্য হয় না।
- `forbidden_call`: রেকর্ড করা কৃত্রিম অ্যাকচুয়েটর কমান্ড নিষেধ চুক্তির সঙ্গে মিলেছে। এটি বাস্তব অটোমেশন প্রেরণ, ভৌত সক্রিয়করণ নয়।
- `states_mismatch`: টাইমলাইনের assignment বা কৃত্রিম অ্যাকচুয়েটর আলাদা অবস্থা রেখে গেছে।
- `blocked_io` অথবা `background_exception`: সবুজ ফল পেতে কখনো গার্ড বন্ধ করবেন না। এই সংস্করণ নেটওয়ার্ক ইন্টিগ্রেশন গ্রহণ করে না। কৃত্রিম পুনরুৎপাদন ও সংস্করণ জানান।
- অনিয়মিত টাইমার পরীক্ষা: অবস্থার পরিবর্তন ও যাচাই করা সময়সীমার দূরত্ব বাড়ান। বাস্তব ইভেন্ট-লুপের সময়সূচি মাপা হয়; ভার্চুয়াল ঘড়ি বা মাইক্রোসেকেন্ড-নির্ভুল সময়সূচির প্রতিশ্রুতি নেই।
- রিলোড: বাস্তব রিলোড `for` টাইমার বাতিল করতে পারে। নীতিতে পুনরুদ্ধার লাগলে স্পষ্ট সমন্বয় অটোমেশন প্রয়োজন; `reload_reconcile.json` তুলনা করুন।
- বিদ্যমান রিপোর্ট: `--report` ইচ্ছাকৃতভাবে সেটি ওভাররাইট করতে অস্বীকার করে। নতুন পাথ বেছে নিন।

সম্পাদনাযোগ্য নয় এমন ইনস্টলের পরে সোর্স ট্রি ব্যবহার করলে পরিবর্তন পরীক্ষার আগে প্যাকেজ পুনরায় ইনস্টল করুন। উন্নয়নের জন্য `--no-deps -e .` দিয়ে ইনস্টল করুন।
