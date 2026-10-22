# Kontrak skenario v1

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

Validator yang menjadi acuan adalah `src/ha_scenario_tests/schema.py`. Hanya JSON, paling besar 64 KiB. Kunci tak dikenal, kunci JSON duplikat, masukan symlink, angka nonhingga, dan tipe tidak valid ditolak. Jangan menyalin konfigurasi rumah tangga ke contoh publik.

Field akar wajib: `schema: "ha-scenario/v1"`, `name` pendek dengan huruf kecil, `seed`, `automations`, `timeline`, `expect`. Field opsional `settle_seconds` bernilai 0.1 secara default. Semua ID entitas memakai awalan `scenario_` dan harus dideklarasikan dalam seed. Domain yang didukung: `light`, `switch`, `input_boolean`, `binary_sensor`. Status yang didukung: `on`, `off`, `unknown`, `unavailable`.

Otomasi memiliki `id`, `triggers`, `actions`, serta `conditions` dan `mode` opsional (`single` atau `restart`). Pemicu status mewajibkan `trigger`, `entity_id`, `to`; `from` dan `for_seconds` bersifat opsional. Pemicu peristiwa memakai `trigger: "event"` dan `event_type: "scenario_name"`; `automation_reloaded` juga didukung. Kondisi hanya berupa perbandingan status. Tindakan memuat `action` dan satu `entity_id`: `turn_on`, `turn_off`, `toggle` pada entitas light/switch/input_boolean yang ada dalam seed. Templat, selector, tindakan perangkat, blueprint, skrip dari disk, atau data layanan tidak diperbolehkan.

Langkah linimasa memuat `after` (detik relatif sejak langkah sebelumnya selesai), dan tepat satu operasi:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Operasi lain: `"event": "scenario_manual_off"` atau `"reload": true`. Pemuatan ulang memanggil layanan otomasi HA yang sebenarnya, yang membaca `configuration.yaml` sementara hasil pembuatan; pengujian tidak menirukan pemuatan ulang dengan memicu peristiwa selesainya.

`expect.calls` adalah daftar berurutan yang persis dari catatan `{action, entity_id}`, termasuk pengulangan; daftar kosong melarang semua panggilan aktuator. `expect.forbidden` secara opsional mencantumkan panggilan yang tidak boleh terjadi. `expect.states` memetakan ID dalam seed ke status akhir. Panggilan tak terduga menyebabkan kegagalan meskipun status akhir kebetulan cocok.

Batas: 64 entitas seed, 16 otomasi, 8 pemicu dan 8 kondisi per otomasi, 16 tindakan per otomasi, 32 langkah linimasa, total 5 detik jeda yang diminta, 256 panggilan tertangkap. Kesalahan tugas latar belakang dan I/O yang diblokir menggagalkan eksekusi. Laporan memuat waktu monoton yang berlalu untuk panggilan dan langkah, komponen yang dimuat, status akhir, dan kode kegagalan.

Induk memvalidasi seluruh laporan worker sebelum mengembalikannya. `passed` harus benar-benar bertipe Boolean, `physical_validation` harus false, dan skema, versi HA, nama skenario, field, serta batas harus sesuai dengan protokol. Induk juga memeriksa asersi panggilan dan status terhadap skenario, bukan mempercayai penanda keberhasilan. Keluaran tidak valid dan setiap kode keluar worker bukan nol adalah kesalahan runtime, meskipun anak mencetak objek JSON yang terlihat berhasil.

Contoh stale yang disediakan menyatakan kehilangan transport melalui `unavailable`. Contoh itu tidak menyimpulkan kesegaran sumber dari `last_changed`, tidak menguji penguraian stempel waktu sensor, atau membuktikan perilaku kedaluwarsa sensor yang sesungguhnya. Pengambilalihan manual adalah kebijakan sintetis eksplisit; alat ini tidak menambahkan kebijakan tersebut pada otomasi yang sudah ada.
