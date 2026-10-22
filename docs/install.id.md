# Instalasi dan pembatasan lingkungan

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

Gunakan runtime Home Assistant yang versinya dipatok dengan Python 3.14.2–3.14.x. Instal `requirements.lock` dengan `--require-hashes`, lalu instal paket ini menggunakan `--no-deps .`, seperti ditunjukkan pada README utama. Lock mencakup dependensi aplikasi dan pengujian. Lingkungan bersih wajib digunakan; jangan memasang ke lingkungan Home Assistant produksi Anda. Gunakan `pip install --no-deps -e .` sebagai gantinya ketika mengedit sumber.

Jalankan `ha-scenario validate examples/stale_sensor.json` terlebih dahulu. Validasi tidak mengimpor runtime HA. Kemudian jalankan `ha-scenario run examples/stale_sensor.json --report result.json`. Tidak ada server tujuan yang dikonfigurasi. Satu-satunya jalur keluaran berasal dari argumen `--report` eksplisit Anda, bukan dari skenario.

Untuk batas jaringan yang lebih kuat:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Proses build memerlukan akses Internet untuk dependensi. Proses eksekusi tidak memiliki jaringan dan menggunakan `/tmp` yang dapat ditulis serta dibuang sesudahnya; konfigurasi rumah, soket Docker, atau kredensial tidak dipasang. Ini adalah resep penerapan opsional; lihat catatan validasi untuk mengetahui apakah kontainer persis ini telah dijalankan. Jangan tambahkan jaringan host atau mount produksi.

Antarmuka subproses membuang kredensial warisan dan `PYTHONPATH`. Worker dengan `-I` menggunakan paket yang terinstal. Hanya PATH, SYSTEMROOT, dan LANG yang diwariskan; seed hash dibuat tetap. Di Linux, jalur pustaka worker diturunkan dari `LIBDIR` instalasi Python yang sedang berjalan, sehingga build Python yang dapat dipindahkan bisa menemukan libpython. `LD_LIBRARY_PATH` warisan tidak pernah disalin. Proses anak memiliki batas waktu induk 30 detik, batas internal 20 detik, paling banyak 5 detik jeda yang diminta pada linimasa, serta 256 tindakan yang ditangkap. Kemacetan dependensi native dihentikan oleh batas waktu induk.

Plugin pytest dipasang secara otomatis. Pengujian dapat memuat skenario dengan `ha_scenario_tests.schema.load` dan memanggil fixture `scenario_runner`. JUnit dibuat oleh pytest sendiri. `run_scenario` juga dapat diimpor dari Python biasa.
