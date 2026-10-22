# যাচাইয়ের নথি

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

## 2026-10-15 Linux রানটাইম যাচাই

[GitHub Actions রান 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) কমিট `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`-এ সফল হয়েছিল, Ubuntu-তে CPython 3.14.8 ও নির্দিষ্ট Home Assistant 2026.10.0 ব্যবহার করে। পুরো `python3 -m pytest -q` কমান্ড **২১.৪২ সেকেন্ডে ৫৪টি পরীক্ষা সফল** করে শেষ হয়, কোনো পরীক্ষা বাদ যায়নি। এতে বাস্তব HA-এর সাতটি রানটাইম পরীক্ষাই আছে: চারটি উদাহরণ দৃশ্যপট, ইচ্ছাকৃতভাবে ব্যর্থ প্রত্যাশা/নিষিদ্ধ কাজের ঘটনা, স্থানীয়কৃত CLI JSON রিপোর্ট এবং পরবর্তী ব্যবহারকারীর ভূমিকা-হস্তান্তর চুক্তি। প্রতিটি রানটাইম পরীক্ষা নতুন নিয়ন্ত্রিত ওয়ার্কার চালায়; প্রত্যাশিত ব্যর্থতার assertion ব্যর্থতা হিসেবেই পরীক্ষা হয়, সফল দৃশ্যপট হিসেবে দেখানো হয় না।

একই রানে Ruff, নথির লিঙ্ক/SVG পরীক্ষা, সোর্স ও wheel বিল্ড, সোর্স প্রকাশ নীতি এবং পুরো ইতিহাসের গোপন তথ্য স্ক্যানও সফল হয়। এটি নথিভুক্ত Python I/O গার্ডের অধীনে কৃত্রিম সার্ভিস প্রেরণ ও অবস্থার আচরণ যাচাই করে। এটি OS নিরাপত্তা স্যান্ডবক্স প্রতিষ্ঠা, Docker চালানো যাচাই বা ভৌত ডিভাইসের আচরণ প্রমাণ করে না।

## 2026-10-15 macOS উন্নয়ন পরীক্ষা

সোর্স, কঠোর ইনপুট গ্রহণ, Python অডিট গার্ড, CLI অনুবাদ এবং SVG পুনর্নির্মাণ স্থানীয়ভাবে macOS arm64-এ Python 3.14.7 দিয়ে পরীক্ষা হয়। `python -m pytest -q -m 'not runtime'` **৪৭টি পরীক্ষা** সফল করে; এই কমান্ড বাস্তব HA-এর সাতটি ঘটনা স্পষ্টভাবে বাদ দেয়। `python -m ruff check src tests scripts` সফল হয়। এটি পুরো রানটাইম পরীক্ষা সমষ্টির বিকল্প নয়।

বাস্তব Home Assistant 2026.10.0 ইঞ্জিন `automation`, `blueprint` ও `trace` লোড করে এবং উপস্থিতির সময়সীমা ও ম্যানুয়াল ওভাররাইড দৃশ্যপট প্রত্যাশিত কৃত্রিম সার্ভিস কল, শেষ অবস্থা এবং কোনো অবরুদ্ধ I/O ছাড়া চালায়। এরপর স্থানীয় Python প্রসেস ইন্টারপ্রেটার বন্ধের সময় নেটিভ segmentation fault নিয়ে বেরিয়ে যায়। আগে সফল JSON ডেটা এলেও প্যারেন্ট রানার এই অশূন্য exit-কে সঠিকভাবে রানটাইম ব্যর্থতা ধরে। **macOS-এর পুরো রানটাইম পরীক্ষা সফল বলে দাবি করা হচ্ছে না।**

রিলিজ গ্রহণের আগে পুরো Linux CI পরীক্ষা সমষ্টি প্রয়োজন। `python -m pytest -q --junitxml=junit.xml` চালান; HA না থাকা, ভুল HA সংস্করণ, চাইল্ডের সময় শেষ হওয়া ও অশূন্য exit ব্যর্থ হয়, নীরবে বাদ যায় না। ওপরে যুক্ত রানটি এই বাস্তবায়নের Linux প্রমাণ; পরের পরিবর্তনের নিজস্ব সফল রান লাগে। এই নথিতে Docker চালানো বা ভৌত ডিভাইস যাচাইয়ের দাবি নেই।

## নিয়ন্ত্রিত বুটস্ট্র্যাপ মেটাডেটা

ওয়ার্কার Python-এর ক্যাশ করা প্রসেসর মেটাডেটায় কৃত্রিম মান `synthetic` দেয় এবং HA ইমপোর্টের আগে `socket.has_ipv6` বন্ধ করে। এতে HA-এর প্ল্যাটফর্ম আরম্ভ `uname -p` চালায় না এবং urllib3 ইমপোর্টের সময় localhost IPv6 bind পরীক্ষা করে না। Linux-এ গার্ডের অধীনে `ctypes.CDLL(None)` দিয়ে ifaddr ইমপোর্ট হয়, যা প্রসেসে ইতিমধ্যে লোড করা libc প্রতীক শনাক্ত করে; ফলে লাইব্রেরি খোঁজার `ldconfig` সাবপ্রসেস এড়ানো যায়। স্বাভাবিক লাইব্রেরি অনুসন্ধানকারী সঙ্গে সঙ্গে ফিরিয়ে আনা হয়। এসব কাজের জন্য I/O গার্ডে অনুমতির তালিকার ব্যতিক্রম নেই। পরিবর্তন শুধু হোস্ট মেটাডেটা/অনুসন্ধানে প্রভাব ফেলে; HA ট্রিগার, শর্ত, টাইমার, রিলোড, স্ক্রিপ্ট ও সার্ভিস প্রেরণ বাস্তব। এগুলি সংস্করণ-সংবেদনশীল এবং নির্দিষ্ট রানটাইম পরীক্ষা সমষ্টিতে অন্তর্ভুক্ত।

## পুনরুৎপাদন

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

কোনো রিপোর্ট বাস্তব রিলের অবস্থা, রেডিও বিতরণ, বাড়িতে উপস্থিতির নির্ভুলতা বা উৎপাদনের সময়কাল অনুযায়ী টাইমিং প্রমাণ করে না। SVG টাইমলাইন কৃত্রিম প্রত্যাশা দেখায়, বেঞ্চমার্ক পরিমাপ নয়।

রানটাইম পরীক্ষা সমষ্টিতে `tests/fixtures/role_transfer.json`-ও আছে, পরবর্তী ব্যবহারকারীর কৃত্রিম চুক্তি: বর্তমান ভূমিকা বন্ধ হয় এবং অবসরপ্রাপ্ত প্লাগ চালু থাকে। এটি ভৌত লোড স্থানান্তরের পরীক্ষা নয়।
