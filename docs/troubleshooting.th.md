# การแก้ปัญหา

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

- ออกด้วยรหัส 2 ระหว่างติดตั้ง/รัน: ตรวจ Python 3.14.2–3.14.x เวอร์ชัน HA ที่ตรึงให้ตรง และสภาพแวดล้อมเสมือนสะอาด ตัวรันปฏิเสธ HA เวอร์ชันอื่น ติดตั้งจากไฟล์ล็อกอีกครั้งก่อนรายงานความล้มเหลว
- เวิร์กเกอร์ล้มเหลว/หมดเวลา: การ import การพึ่งพาหรือการตั้งค่า HA ล้มเหลว รันเวิร์กเกอร์ที่แยกโดยตรงด้วยไฟล์ **สังเคราะห์** เพื่อรับ traceback ในเครื่อง: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json` อย่าเผยแพร่ข้อมูลวินิจฉัยสภาพแวดล้อมที่ยังไม่ได้ตรวจทาน
- `calls_mismatch`: เปรียบเทียบลำดับและการเรียกซ้ำ ไม่ใช่เฉพาะสถานะสุดท้าย สถานะตั้งต้นถูกกำหนดก่อนเริ่ม จึงไม่ถือเป็นทริกเกอร์สถานะใหม่หลังเริ่มโดยอัตโนมัติ
- `forbidden_call`: คำสั่งอุปกรณ์สังเคราะห์ที่บันทึกตรงกับสัญญาข้อห้าม นี่คือการส่งงานอัตโนมัติจริง ไม่ใช่การทำงานทางกายภาพ
- `states_mismatch`: การกำหนดค่าในไทม์ไลน์หรืออุปกรณ์สังเคราะห์ทิ้งสถานะที่ต่างออกไป
- `blocked_io` หรือ `background_exception`: อย่าปิดตัวป้องกันเพื่อให้ได้ผลเขียวเด็ดขาด รุ่นนี้ไม่อนุญาตอินทิเกรชันเครือข่าย ให้รายงานตัวอย่างสังเคราะห์สำหรับทำซ้ำและเวอร์ชัน
- การทดสอบตัวจับเวลาไม่คงที่: เพิ่มระยะห่างระหว่างการเปลี่ยนสถานะกับเส้นตายที่ยืนยัน วัดการจัดตารางลูปเหตุการณ์จริง ไม่รับประกันนาฬิกาเสมือนหรือการจัดตารางที่แม่นยำระดับไมโครวินาที
- โหลดใหม่: การโหลดใหม่จริงอาจยกเลิกตัวจับเวลา `for` ต้องมีระบบอัตโนมัติปรับคืนสถานะอย่างชัดเจนหากนโยบายกำหนดให้กู้คืน เปรียบเทียบ `reload_reconcile.json`
- มีรายงานอยู่แล้ว: `--report` ตั้งใจปฏิเสธการเขียนทับ ให้เลือกพาธใหม่

หากใช้ซอร์สทรีหลังติดตั้งแบบแก้ไขไม่ได้ ให้ติดตั้งแพ็กเกจใหม่ก่อนทดสอบการเปลี่ยนแปลง สำหรับการพัฒนาให้ติดตั้งด้วย `--no-deps -e .`
