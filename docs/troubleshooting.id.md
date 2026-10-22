# Pemecahan masalah

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

- Kode keluar 2 selama instalasi atau eksekusi: periksa Python 3.14.2–3.14.x, versi HA yang dipatok secara tepat, dan lingkungan virtual yang bersih. Runner menolak versi HA lain. Instal ulang lock sebelum melaporkan kegagalan.
- Worker gagal atau kehabisan waktu: impor dependensi atau penyiapan HA gagal. Jalankan worker terisolasi secara langsung dengan berkas **sintetis** untuk mendapatkan traceback lokal: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Jangan menerbitkan diagnostik lingkungan yang belum ditinjau.
- `calls_mismatch`: bandingkan urutan dan panggilan duplikat, bukan hanya status akhir. Status seed ditetapkan sebelum startup; status tersebut tidak otomatis dihitung sebagai pemicu status baru setelah startup.
- `forbidden_call`: perintah aktuator sintetis yang ditangkap cocok dengan kontrak negatif. Ini adalah pengiriman otomasi yang sebenarnya, bukan aktivasi fisik.
- `states_mismatch`: penetapan pada linimasa atau aktuator sintetis meninggalkan status yang berbeda.
- `blocked_io` atau `background_exception`: jangan pernah mematikan penjaga hanya untuk mendapat hasil hijau. Rilis ini tidak mengizinkan integrasi jaringan. Laporkan reproduksi sintetis dan versinya.
- Uji timer tidak stabil: perbesar jarak antara transisi status dan tenggat yang diperiksa. Penjadwalan event loop nyata yang diukur; tidak ada janji jam virtual atau penjadwalan tepat hingga mikrodetik.
- Pemuatan ulang: timer `for` dapat dibatalkan oleh pemuatan ulang nyata. Otomasi rekonsiliasi eksplisit diperlukan jika kebijakan menuntut pemulihan; bandingkan `reload_reconcile.json`.
- Laporan sudah ada: `--report` sengaja menolak menimpanya. Pilih jalur baru.

Jika memakai pohon sumber setelah instalasi yang tidak dapat diedit, instal ulang paket sebelum menguji perubahan. Untuk pengembangan, instal dengan `--no-deps -e .`.
