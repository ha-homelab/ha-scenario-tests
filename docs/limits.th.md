# ขอบเขตและหลักฐาน

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

รุ่นนี้ตรวจสอบชุดย่อยที่มีขอบเขตจำกัด โดยใช้ทริกเกอร์ เงื่อนไข ตัวจับเวลา การโหลดใหม่ และการส่งการกระทำของสคริปต์จาก Home Assistant จริง ตัวรับคำสั่งอุปกรณ์และสถานะอินพุตเป็นข้อมูลสังเคราะห์ ไม่ได้พิสูจน์โปรโตคอลการสื่อสาร การใช้กระแสไฟ ความแม่นยำเซนเซอร์ สถานะทางกายภาพของรีเลย์ ความปลอดภัย หรือพฤติกรรมของการตั้งค่า HA ทุกแบบที่เป็นไปได้

นาฬิกาวัดเวลาจริงที่ผ่านไปแบบเพิ่มขึ้นทางเดียว การทดสอบตั้งใจใช้ช่วงเวลาสั้นและมีระยะเผื่อการจัดตาราง เราไม่แพตช์เมธอดหน่วงเวลาภายใน HA ไม่เปลี่ยนระยะเวลาของตัวจับเวลาในระบบจริง และไม่อ้างว่าเทียบเท่าเวลาเสมือน เวลาออมแสง การจัดตารางตามเวลานาฬิกา การเริ่มโปรเซส HA ทั้งหมดใหม่ และการเก็บข้อมูลถาวรของ Recorder อยู่นอกขอบเขต v1 มีการทดสอบการโหลดใหม่ แต่ไม่ใช่การเริ่มโปรเซสใหม่

อินพุตไม่มีเทมเพลตที่รันได้หรือการตั้งค่าอินทิเกรชัน แต่ละเวิร์กเกอร์ใช้ไดเรกทอรีชั่วคราวสะอาด สภาพแวดล้อมที่ตัดค่าที่ไม่จำเป็น และตัวป้องกันการตรวจสอบแบบทั่วทั้งโปรเซส ซึ่งป้องกัน I/O เครือข่าย/โปรเซสย่อยของ Python ที่เกิดโดยไม่ตั้งใจผ่านเส้นทางที่อนุญาต นี่ไม่ใช่แซนด์บ็อกซ์สำหรับโค้ดประสงค์ร้าย การพึ่งพา Python/เนทีฟ อินเทอร์พรีเตอร์ และโฮสต์ถือว่าเชื่อถือได้ ให้รันซอร์สหรือการพึ่งพาที่ไม่น่าเชื่อถือเฉพาะในสภาพแวดล้อมที่รักษาความปลอดภัยแยกต่างหาก วิธี Docker network-none ที่เลือกใช้ได้เพิ่มการแยกเครือข่าย แต่ไม่พิสูจน์พฤติกรรมฮาร์ดแวร์

รายงานสาธารณะควรมีเฉพาะ fixture สังเคราะห์ ไทม์ไลน์สถานะจริงเผยการอยู่บ้านและพฤติกรรมได้แม้ไม่มีโทเคน ที่นี่ไม่มีรายการอุปกรณ์ในบ้าน สิ่งบันทึก หรือการตั้งค่าระบบจริง แผนภาพทุกภาพระบุว่าเป็นข้อมูลสังเคราะห์ และสร้างซ้ำได้ด้วย `python scripts/render_diagrams.py`

ดู[การตรวจสอบ](validation.th.md)สำหรับรายการตรวจที่วัดผลกับรุ่นนี้ การรองรับการติดตั้งจำกัดเฉพาะสภาพแวดล้อมในบันทึกนั้น วิธีคอนเทนเนอร์ไม่ได้หมายความว่าทดสอบแล้วทุกแพลตฟอร์ม
