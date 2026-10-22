# পরিধি ও প্রমাণ

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

এই সংস্করণ বাস্তব Home Assistant ট্রিগার, শর্ত, টাইমার, রিলোড ও স্ক্রিপ্টের কাজ প্রেরণ দিয়ে একটি সীমিত উপসেট যাচাই করে। অ্যাকচুয়েটর গ্রাহক ও ইনপুট অবস্থা কৃত্রিম। এতে যোগাযোগ প্রোটোকল, বিদ্যুৎপ্রবাহের ব্যবহার, সেন্সরের নির্ভুলতা, রিলের ভৌত অবস্থা, নিরাপত্তা বা সম্ভাব্য সব HA কনফিগারেশনের আচরণ প্রমাণিত হয় না।

ঘড়ি বাস্তবে অতিবাহিত একমুখী সময় মাপে। পরীক্ষাগুলি ইচ্ছাকৃতভাবে ছোট বিরতি ও সময়সূচির বাড়তি সুযোগ রাখে। আমরা HA-এর অভ্যন্তরীণ বিলম্ব পদ্ধতি প্যাচ করি না, উৎপাদনের টাইমারের সময়কাল বদলাই না এবং ভার্চুয়াল সময়ের সমতুল্য বলে দাবি করি না। দিবালোক সংরক্ষণ সময়, ঘড়ির সময় অনুযায়ী সূচি, পুরো HA প্রসেস পুনরায় চালু করা ও Recorder-এর স্থায়ী সংরক্ষণ v1-এর বাইরে। রিলোড পরীক্ষা করা হয়; সেটি প্রসেস পুনরায় চালু করা নয়।

ইনপুটে চালানো যায় এমন টেমপ্লেট বা ইন্টিগ্রেশন কনফিগারেশন থাকে না। প্রতিটি ওয়ার্কার পরিষ্কার অস্থায়ী ডিরেক্টরি, ছাঁটা পরিবেশ এবং সর্বব্যাপী অডিট গার্ড ব্যবহার করে। এটি অনুমোদিত পথে অনিচ্ছাকৃত Python নেটওয়ার্ক/সাবপ্রসেস I/O রোধ করে। এটি ক্ষতিকর কোডের স্যান্ডবক্স নয়: Python/নেটিভ নির্ভরতা, ইন্টারপ্রেটার ও হোস্টকে বিশ্বস্ত ধরা হয়। অবিশ্বস্ত সোর্স বা নির্ভরতা শুধু আলাদাভাবে সুরক্ষিত পরিবেশে চালান। ঐচ্ছিক Docker network-none পদ্ধতি নেটওয়ার্ক বিচ্ছিন্নতা বাড়ায়, কিন্তু হার্ডওয়্যারের আচরণ প্রমাণ করে না।

প্রকাশ্য রিপোর্টে শুধু কৃত্রিম fixture থাকা উচিত। বাস্তব অবস্থার টাইমলাইন টোকেন ছাড়াও বাড়িতে থাকা ও অভ্যাস প্রকাশ করে। এখানে গৃহস্থালি সরঞ্জামের তালিকা, রেকর্ডিং বা উৎপাদনের কনফিগারেশন নেই। সব চিত্র কৃত্রিম হিসেবে চিহ্নিত এবং `python scripts/render_diagrams.py` দিয়ে পুনরায় তৈরি করা যায়।

এই সংস্করণে করা পরিমাপভিত্তিক পরীক্ষার জন্য [যাচাই](validation.bn.md) দেখুন। ইনস্টলেশন সমর্থন ওই নথির পরিবেশগুলিতে সীমিত; কনটেইনারের পদ্ধতি দেওয়া মানে সব প্ল্যাটফর্ম পরীক্ষা করা হয়েছে নয়।
