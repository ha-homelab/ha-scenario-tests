# การติดตั้งและการแยกสภาพแวดล้อม

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

ใช้รันไทม์ Home Assistant เวอร์ชันที่ตรึงไว้กับ Python 3.14.2–3.14.x ติดตั้ง `requirements.lock` ด้วย `--require-hashes` แล้วติดตั้งแพ็กเกจนี้ด้วย `--no-deps .` ตาม README ที่รากโครงการ ไฟล์ล็อกครอบคลุมการพึ่งพาของแอปพลิเคชันและการทดสอบ ต้องใช้สภาพแวดล้อมสะอาด อย่าติดตั้งในสภาพแวดล้อม Home Assistant ที่ใช้งานจริง หากแก้ไขซอร์ส ให้ใช้ `pip install --no-deps -e .` แทน

เรียก `ha-scenario validate examples/stale_sensor.json` ก่อน การตรวจสอบจะไม่ import รันไทม์ HA จากนั้นเรียก `ha-scenario run examples/stale_sensor.json --report result.json` ไม่มีการกำหนดเซิร์ฟเวอร์เป้าหมาย พาธเอาต์พุตเพียงแห่งเดียวมาจากอาร์กิวเมนต์ `--report` ที่คุณระบุชัดเจน ไม่ใช่จากสถานการณ์ทดสอบ

หากต้องการขอบเขตเครือข่ายที่เข้มงวดยิ่งขึ้น:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

การบิลด์ต้องใช้อินเทอร์เน็ตเพื่อดาวน์โหลดการพึ่งพา ขณะรันไม่มีเครือข่าย และ `/tmp` ที่เขียนได้จะใช้ชั่วคราวแล้วทิ้ง ไม่มีการเมานต์การตั้งค่าบ้าน ซ็อกเก็ต Docker หรือข้อมูลรับรอง นี่เป็นวิธีติดตั้งที่เลือกใช้ได้ โปรดดูบันทึกการตรวจสอบว่ามีการรันคอนเทนเนอร์นี้จริงหรือไม่ อย่าเพิ่มเครือข่ายโฮสต์หรือเมานต์จากระบบใช้งานจริง

อินเทอร์เฟซโปรเซสย่อยจะลบข้อมูลรับรองที่สืบทอดมาและ `PYTHONPATH` ตัวเลือก `-I` ของเวิร์กเกอร์ใช้แพ็กเกจที่ติดตั้งแล้ว สืบทอดเฉพาะ PATH, SYSTEMROOT และ LANG โดยตรึงค่าเริ่มต้นของแฮชไว้ บน Linux พาธไลบรารีของเวิร์กเกอร์มาจาก `LIBDIR` ของ Python ที่กำลังรัน ทำให้ Python ที่ย้ายตำแหน่งได้ค้นพบ libpython จะไม่คัดลอก `LD_LIBRARY_PATH` ที่สืบทอดมาเด็ดขาด โปรเซสแม่กำหนดเวลาสูงสุดของลูก 30 วินาที และภายในกำหนด 20 วินาที ขอเวลารอในไทม์ไลน์รวมได้สูงสุด 5 วินาที และบันทึกการกระทำได้ 256 ครั้ง หากการพึ่งพาแบบเนทีฟค้าง โปรเซสแม่จะยุติเมื่อหมดเวลา

ปลั๊กอิน pytest จะติดตั้งอัตโนมัติ การทดสอบโหลดสถานการณ์ด้วย `ha_scenario_tests.schema.load` และเรียก fixture `scenario_runner` ได้ pytest สร้าง JUnit เอง และ import `run_scenario` ใน Python ปกติได้ด้วย
