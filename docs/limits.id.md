# Cakupan dan bukti

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

Rilis ini memvalidasi bagian terbatas menggunakan pemicu, kondisi, timer, pemuatan ulang, dan pengiriman tindakan skrip Home Assistant yang sebenarnya. Penerima perintah aktuator dan status masukan bersifat sintetis. Ini tidak membuktikan protokol komunikasi, konsumsi arus, akurasi sensor, status fisik relai, keselamatan, atau perilaku setiap kemungkinan konfigurasi HA.

Jam mengukur waktu monoton nyata yang berlalu. Pengujian sengaja memakai interval pendek dan kelonggaran penjadwalan. Kami tidak menambal metode penundaan internal HA, menulis ulang durasi timer produksi, atau mengklaim kesetaraan dengan waktu virtual. Perubahan waktu musim panas, penjadwalan menurut jam dinding, mulai ulang penuh proses HA, dan persistensi Recorder berada di luar v1. Pemuatan ulang diuji; itu bukan mulai ulang proses.

Masukan tidak berisi templat yang dapat dieksekusi atau konfigurasi integrasi. Setiap worker memakai direktori sementara bersih, lingkungan yang dibersihkan, dan penjaga audit global. Ini mencegah I/O jaringan atau subproses Python yang tidak disengaja melalui jalur yang diizinkan. Ini bukan sandbox bagi kode berbahaya: dependensi Python dan native, interpreter, serta host dipercaya. Jalankan sumber atau dependensi yang tidak dipercaya hanya di lingkungan aman yang terpisah. Resep Docker tanpa jaringan yang opsional memperkuat isolasi jaringan tetapi tidak membuktikan perilaku perangkat keras.

Laporan publik hanya boleh memuat fixture sintetis. Linimasa status nyata mengungkap keberadaan penghuni dan kebiasaan meskipun tanpa token. Tidak ada inventaris rumah tangga, rekaman, atau konfigurasi produksi yang disertakan di sini. Semua diagram diberi label sintetis dan dapat direproduksi dengan `python scripts/render_diagrams.py`.

Lihat [validasi](validation.id.md) untuk pemeriksaan terukur yang dijalankan pada rilis ini. Dukungan instalasi terbatas pada lingkungan dalam catatan tersebut; resep kontainer tidak mengklaim bahwa setiap platform sudah diuji.
