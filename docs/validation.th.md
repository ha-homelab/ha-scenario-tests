# บันทึกการตรวจสอบ

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

## การตรวจสอบรันไทม์ Linux วันที่ 2026-10-15

[การรัน GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) ผ่านที่คอมมิต `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` โดยใช้ CPython 3.14.8 บน Ubuntu กับ Home Assistant 2026.10.0 ที่ตรึงไว้ คำสั่งเต็ม `python3 -m pytest -q` จบด้วย **ผ่าน 54 การทดสอบใน 21.42 วินาที** โดยไม่ข้ามการทดสอบ รวมการทดสอบรันไทม์ที่ใช้ HA จริงทั้งเจ็ดรายการ ได้แก่ สถานการณ์ตัวอย่างสี่รายการ กรณีความคาดหวัง/การกระทำต้องห้ามที่ตั้งใจให้ล้มเหลว รายงาน CLI JSON ที่แปลภาษา และสัญญาการโอนบทบาทของผู้ใช้ปลายทาง การทดสอบรันไทม์แต่ละรายการเริ่มเวิร์กเกอร์ที่ควบคุมใหม่ ข้อยืนยันที่คาดว่าจะล้มเหลวถูกทดสอบในฐานะความล้มเหลว ไม่รายงานเป็นสถานการณ์สำเร็จ

ในการรันเดียวกัน Ruff การตรวจลิงก์เอกสาร/SVG การบิลด์ซอร์สและ wheel นโยบายเผยแพร่ซอร์ส และการสแกนความลับตลอดประวัติก็ผ่านด้วย สิ่งนี้ตรวจสอบการส่งบริการสังเคราะห์และพฤติกรรมสถานะภายใต้ตัวป้องกัน Python I/O ที่อธิบายไว้ ไม่ได้ยืนยันแซนด์บ็อกซ์ความปลอดภัยระดับ OS ตรวจสอบการรัน Docker หรือพิสูจน์พฤติกรรมอุปกรณ์จริง

## การตรวจสอบระหว่างพัฒนา macOS วันที่ 2026-10-15

มีการตรวจซอร์ส การรับอินพุตอย่างเข้มงวด ตัวป้องกันการตรวจสอบ Python คำแปล CLI และการสร้าง SVG ใหม่ในเครื่องด้วย Python 3.14.7 บน macOS arm64 คำสั่ง `python -m pytest -q -m 'not runtime'` ผ่าน **47 การทดสอบ** โดยแยกเจ็ดกรณี HA จริงออกอย่างชัดเจน คำสั่ง `python -m ruff check src tests scripts` ผ่าน สิ่งนี้ไม่แทนชุดทดสอบรันไทม์เต็ม

เอนจิน Home Assistant 2026.10.0 จริงโหลด `automation`, `blueprint` และ `trace` และรันสถานการณ์หมดเวลาการตรวจพบคนกับการแทนที่ด้วยมือ โดยมีการเรียกบริการสังเคราะห์และสถานะสุดท้ายตามคาด ไม่มี I/O ที่ถูกบล็อก จากนั้นโปรเซส Python ในเครื่องออกด้วย segmentation fault แบบเนทีฟระหว่างเก็บกวาดอินเทอร์พรีเตอร์ ตัวรันแม่ถือว่ารหัสออกไม่เป็นศูนย์นั้นเป็นความล้มเหลวขณะรันอย่างถูกต้อง แม้ก่อนหน้านั้นจะมีข้อมูล JSON สำเร็จ **ไม่ได้อ้างว่าการทดสอบรันไทม์ macOS เต็มชุดผ่าน**

ต้องผ่านชุด Linux CI เต็มก่อนยอมรับรุ่นเผยแพร่ เรียก `python -m pytest -q --junitxml=junit.xml` การไม่มี HA เวอร์ชัน HA ผิด ลูกหมดเวลา หรือลูกออกด้วยรหัสไม่เป็นศูนย์จะทำให้ล้มเหลว ไม่ข้ามเงียบ ๆ การรันที่เชื่อมไว้ด้านบนเป็นหลักฐาน Linux ของการใช้งานนี้ การเปลี่ยนแปลงภายหลังต้องมีการรันผ่านของตนเอง บันทึกนี้ไม่อ้างว่ารัน Docker หรือตรวจสอบอุปกรณ์จริงแล้ว

## เมทาดาทาตอนเริ่มต้นที่ควบคุม

เวิร์กเกอร์ให้ค่าสังเคราะห์ `synthetic` แก่เมทาดาทาหน่วยประมวลผลที่ Python แคชไว้ และปิด `socket.has_ipv6` ก่อน import HA จึงป้องกันการเริ่มต้นแพลตฟอร์ม HA จากการสร้าง `uname -p` และป้องกันการทดสอบ bind IPv6 บน localhost ระหว่าง import urllib3 บน Linux จะ import ifaddr ภายใต้ตัวป้องกันโดยใช้ `ctypes.CDLL(None)` เพื่อค้นหาสัญลักษณ์ libc ที่โหลดในโปรเซสแล้ว จึงเลี่ยงโปรเซสย่อย `ldconfig` ของตัวค้นหาไลบรารี แล้วคืนตัวค้นหาไลบรารีปกติทันที ตัวป้องกัน I/O ไม่มีข้อยกเว้นในรายการอนุญาตสำหรับการดำเนินการเหล่านี้ การเปลี่ยนแปลงมีผลเฉพาะเมทาดาทา/การตรวจหาโฮสต์ ทริกเกอร์ เงื่อนไข ตัวจับเวลา การโหลดใหม่ สคริปต์ และการส่งบริการ HA เป็นของจริง ทั้งหมดไวต่อเวอร์ชันและอยู่ในชุดทดสอบรันไทม์ที่ตรึงไว้

## ทำซ้ำ

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

ไม่มีรายงานใดพิสูจน์สถานะรีเลย์จริง การส่งถึงทางวิทยุ ความแม่นยำการตรวจคนในบ้าน หรือจังหวะเวลาที่มีระยะเท่าระบบจริง ไทม์ไลน์ SVG แสดงความคาดหวังสังเคราะห์ ไม่ใช่ผลวัดเบนช์มาร์ก

ชุดรันไทม์ยังมี `tests/fixtures/role_transfer.json` ซึ่งเป็นสัญญาสังเคราะห์ของผู้ใช้ปลายทาง บทบาทปัจจุบันปิดและปลั๊กที่เลิกใช้งานในบทบาทนั้นยังเปิดอยู่ นี่ไม่ใช่การทดสอบโอนโหลดทางกายภาพ
