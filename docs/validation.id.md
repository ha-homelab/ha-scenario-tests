# Catatan validasi

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

## 2026-10-15: validasi runtime Linux

[Eksekusi GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) lulus pada commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, memakai CPython 3.14.8 di Ubuntu dan Home Assistant yang dipatok ke 2026.10.0. Perintah lengkap `python3 -m pytest -q` selesai dengan **54 pengujian lulus dalam 21.42 detik**, tanpa pengujian yang dilewati. Ini mencakup ketujuh uji runtime dengan HA nyata: empat skenario contoh, kasus harapan gagal dan tindakan terlarang yang disengaja, laporan JSON CLI terlokalisasi, serta kontrak perpindahan peran untuk proyek hilir. Setiap uji runtime memulai worker terkendali baru; asersi yang memang diharapkan gagal diuji sebagai kegagalan, bukan dilaporkan sebagai skenario sukses.

Ruff, pemeriksaan tautan dokumentasi dan SVG, build sumber dan wheel, kebijakan publikasi sumber, serta pemindaian rahasia seluruh riwayat juga lulus dalam eksekusi tersebut. Ini memvalidasi pengiriman layanan sintetis dan perilaku status di bawah penjaga I/O Python yang didokumentasikan. Ini tidak menetapkan sandbox keamanan OS, memvalidasi eksekusi Docker, atau membuktikan perilaku perangkat fisik.

## 2026-10-15: pemeriksaan pengembangan macOS

Sumber, penerimaan masukan ketat, penjaga audit Python, terjemahan CLI, dan regenerasi SVG diperiksa secara lokal menggunakan Python 3.14.7 pada macOS arm64. `python -m pytest -q -m 'not runtime'` lulus **47 pengujian**; tujuh kasus HA nyata secara eksplisit dikecualikan oleh perintah ini. `python -m ruff check src tests scripts` lulus. Ini bukan pengganti suite runtime lengkap.

Mesin Home Assistant 2026.10.0 yang sebenarnya memuat `automation`, `blueprint`, dan `trace`, lalu menjalankan skenario batas waktu kehadiran dan pengambilalihan manual dengan panggilan layanan sintetis yang diharapkan, status akhir, dan tanpa I/O terblokir. Proses Python lokal kemudian keluar dengan segmentation fault native selama penghentian interpreter. Runner induk dengan benar memperlakukan kode keluar bukan nol itu sebagai kegagalan runtime, meskipun sebelumnya ada keluaran JSON sukses. **Tidak diklaim bahwa uji runtime macOS lengkap telah lulus.**

Suite Linux CI lengkap wajib lulus sebelum rilis diterima. Jalankan `python -m pytest -q --junitxml=junit.xml`; HA yang tidak tersedia, versi HA salah, batas waktu anak, dan kode keluar anak bukan nol menyebabkan kegagalan, tidak pernah dilewati diam-diam. Eksekusi tertaut di atas adalah bukti Linux untuk implementasi ini; perubahan berikutnya memerlukan eksekusi suksesnya sendiri. Tidak ada eksekusi Docker atau validasi perangkat fisik yang diklaim dalam catatan ini.

## Metadata bootstrap terkendali

Worker menyediakan nilai sintetis `synthetic` untuk metadata prosesor yang di-cache Python dan menonaktifkan `socket.has_ipv6` sebelum mengimpor HA. Ini mencegah inisialisasi platform HA menjalankan `uname -p` serta mencegah uji bind IPv6 localhost saat impor urllib3. Di Linux, ifaddr diimpor di bawah penjaga memakai `ctypes.CDLL(None)`, yang menyelesaikan simbol libc yang sudah dimuat dalam proses; hal ini menghindari subproses `ldconfig` dari pencari pustaka. Pencari pustaka biasa segera dipulihkan. Penjaga I/O tidak memiliki pengecualian daftar izin untuk operasi ini. Perubahan tersebut hanya memengaruhi metadata dan pemeriksaan host; pemicu, kondisi, timer, pemuatan ulang, skrip, serta pengiriman layanan HA tetap nyata. Perubahan bergantung pada versi dan dicakup oleh suite runtime yang dipatok.

## Reproduksi

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Tidak ada laporan yang membuktikan status relai nyata, pengiriman radio, akurasi kehadiran rumah tangga, atau pengaturan waktu dengan durasi produksi. Linimasa SVG menunjukkan harapan sintetis, bukan pengukuran benchmark.

Suite runtime juga mencakup `tests/fixtures/role_transfer.json`, kontrak sintetis hilir: peran aktif mati dan stopkontak yang dipensiunkan dari peran tetap menyala. Ini bukan pengujian perpindahan beban fisik.
