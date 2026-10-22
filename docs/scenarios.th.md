# สัญญาสถานการณ์ทดสอบ v1

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

ตัวตรวจสอบหลักคือ `src/ha_scenario_tests/schema.py` รับเฉพาะ JSON ขนาดไม่เกิน 64 KiB ปฏิเสธคีย์ที่ไม่รู้จัก คีย์ JSON ซ้ำ อินพุตลิงก์สัญลักษณ์ ตัวเลขที่ไม่เป็นจำนวนจำกัด และชนิดข้อมูลไม่ถูกต้อง อย่าคัดลอกการตั้งค่าบ้านลงในตัวอย่างสาธารณะ

ฟิลด์รากที่จำเป็นคือ `schema: "ha-scenario/v1"`, `name` สั้นที่ใช้ตัวพิมพ์เล็ก, `seed`, `automations`, `timeline`, `expect` ฟิลด์ทางเลือก `settle_seconds` มีค่าเริ่มต้น 0.1 ID เอนทิตีทั้งหมดใช้คำนำหน้า `scenario_` และต้องประกาศในข้อมูลตั้งต้น โดเมนที่รองรับ: `light`, `switch`, `input_boolean`, `binary_sensor` สถานะที่รองรับ: `on`, `off`, `unknown`, `unavailable`

ระบบอัตโนมัติมี `id`, `triggers`, `actions` และฟิลด์ทางเลือก `conditions` กับ `mode` (`single` หรือ `restart`) ทริกเกอร์สถานะต้องมี `trigger`, `entity_id`, `to` และอาจมี `from`, `for_seconds` ทริกเกอร์เหตุการณ์ใช้ `trigger: "event"` และ `event_type: "scenario_name"` รวมทั้งรองรับ `automation_reloaded` เงื่อนไขเป็นการเปรียบเทียบสถานะเท่านั้น การกระทำมี `action` กับ `entity_id` หนึ่งค่า: `turn_on`, `turn_off`, `toggle` บนเอนทิตี light/switch/input_boolean ที่กำหนดตั้งต้น ไม่รับเทมเพลต ตัวเลือก การกระทำของอุปกรณ์ บลูพรินต์ สคริปต์จากดิสก์ หรือข้อมูลบริการ

ขั้นตอนไทม์ไลน์มี `after` (วินาทีสัมพัทธ์นับจากขั้นตอนก่อนหน้าเสร็จ) และมีการดำเนินการหนึ่งอย่างเท่านั้น:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

การดำเนินการอื่นคือ `"event": "scenario_manual_off"` หรือ `"reload": true` การโหลดใหม่เรียกบริการอัตโนมัติจริงของ HA ซึ่งอ่าน `configuration.yaml` ชั่วคราวที่สร้างขึ้น การทดสอบไม่ได้เลียนแบบการโหลดใหม่ด้วยการส่งเหตุการณ์เสร็จสิ้น

`expect.calls` คือรายการระเบียน `{action, entity_id}` ตามลำดับอย่างเคร่งครัดรวมรายการซ้ำ รายการว่างห้ามการเรียกอุปกรณ์ทั้งหมด `expect.forbidden` ใช้ระบุการเรียกที่ห้ามเกิดขึ้นโดยเป็นฟิลด์ทางเลือก `expect.states` จับคู่ ID ตั้งต้นกับสถานะสุดท้าย การเรียกที่ไม่คาดหมายทำให้ล้มเหลวแม้สถานะสุดท้ายบังเอิญตรงกัน

ขีดจำกัด: เอนทิตีตั้งต้น 64 รายการ ระบบอัตโนมัติ 16 รายการ ทริกเกอร์ 8 รายการและเงื่อนไข 8 รายการต่อระบบอัตโนมัติ การกระทำ 16 รายการต่อระบบอัตโนมัติ ขั้นตอนไทม์ไลน์ 32 ขั้น เวลารอที่ขอรวม 5 วินาที และการเรียกที่บันทึก 256 ครั้ง ข้อผิดพลาดของงานเบื้องหลังและ I/O ที่ถูกบล็อกทำให้รันล้มเหลว รายงานมีเวลาที่ผ่านไปของการเรียก/ขั้นตอนตามนาฬิกาทางเดียว คอมโพเนนต์ที่โหลด สถานะสุดท้าย และรหัสความล้มเหลว

โปรเซสแม่ตรวจรายงานเวิร์กเกอร์ทั้งหมดก่อนส่งกลับ `passed` ต้องเป็นชนิด Boolean จริง ๆ, `physical_validation` ต้องเป็น false และสคีมา เวอร์ชัน HA ชื่อสถานการณ์ ฟิลด์ และขอบเขตต้องตรงกับโปรโตคอล โปรเซสแม่ยังตรวจข้อยืนยันการเรียก/สถานะกับสถานการณ์ แทนที่จะเชื่อธงความสำเร็จ เอาต์พุตไม่ถูกต้องและการออกของเวิร์กเกอร์ด้วยรหัสไม่เป็นศูนย์เป็นข้อผิดพลาดขณะรัน แม้ลูกจะพิมพ์ออบเจ็กต์ JSON ที่ดูเหมือนสำเร็จ

ตัวอย่างข้อมูลเก่าที่ให้มาแทนการขาดการส่งข้อมูลด้วย `unavailable` ไม่ได้อนุมานความใหม่ของต้นทางจาก `last_changed` ไม่ทดสอบการแยกวิเคราะห์เวลาประทับเซนเซอร์ และไม่พิสูจน์พฤติกรรมหมดอายุของเซนเซอร์จริง การแทนที่ด้วยมือเป็นนโยบายสังเคราะห์ที่ระบุชัด เครื่องมือไม่เพิ่มนโยบายนั้นลงในระบบอัตโนมัติที่มีอยู่
