# Sorun giderme

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

- Kurulum/çalıştırmada çıkış 2: Python 3.14.2–3.14.x sürümünü, tam HA sabitlemesini ve temiz sanal ortamı kontrol edin. Çalıştırıcı diğer HA sürümlerini reddeder. Hata bildirmeden önce kilit dosyasından yeniden kurun.
- İşçi hatası/zaman aşımı: bağımlılık içe aktarımı veya HA kurulumu başarısız olmuştur. Yerel hata izini almak için yalıtılmış işçiyi **sentetik** dosyayla doğrudan çalıştırın: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. İncelenmemiş ortam tanılarını yayımlamayın.
- `calls_mismatch`: yalnızca son durumu değil, sıra ve yinelenen çağrıları karşılaştırın. Başlangıç durumları başlatmadan önce ayarlanır; başlatma sonrasında otomatik olarak yeni durum tetikleyicisi sayılmaz.
- `forbidden_call`: yakalanan sentetik eyleyici komutu olumsuz sözleşmeyle eşleşmiştir. Bu gerçek bir otomasyon dağıtımıdır, fiziksel eylem değildir.
- `states_mismatch`: zaman çizelgesi ataması veya sentetik eyleyici farklı bir durum bırakmıştır.
- `blocked_io` veya `background_exception`: yeşil sonuç almak için korumayı asla kapatmayın. Bu sürüm ağ entegrasyonlarına izin vermez. Sentetik yeniden üretimi ve sürümü bildirin.
- Kararsız zamanlayıcı testleri: durum geçişi ile doğrulanan son zaman arasındaki aralığı artırın. Gerçek olay döngüsü zamanlaması ölçülür; sanal saat veya mikrosaniye düzeyinde kesin zamanlama vaat edilmez.
- Yeniden yükleme: gerçek yeniden yükleme `for` zamanlayıcılarını iptal edebilir. Politika toparlanma gerektiriyorsa açık bir uzlaştırma otomasyonu gerekir; `reload_reconcile.json` ile karşılaştırın.
- Mevcut rapor: `--report` bilerek üzerine yazmayı reddeder. Yeni bir yol seçin.

Düzenlenebilir olmayan kurulumdan sonra kaynak ağacı kullanıyorsanız, değişiklikleri test etmeden önce paketi yeniden kurun. Geliştirme için `--no-deps -e .` ile kurun.
