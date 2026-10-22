# Doğrulama kaydı

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

## 2026-10-15 Linux çalışma zamanı doğrulaması

[GitHub Actions çalıştırması 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199), Ubuntu üzerinde CPython 3.14.8 ve sabitlenmiş Home Assistant 2026.10.0 kullanarak `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` commit'inde geçti. Tam `python3 -m pytest -q` komutu, atlanan test olmadan **21.42 saniyede 54 başarılı testle** tamamlandı. Buna yedi gerçek HA çalışma zamanı testi dahildir: dört örnek senaryo, kasıtlı başarısız beklenti/yasak eylem vakası, yerelleştirilmiş CLI JSON raporu ve alt tüketicinin rol aktarımı sözleşmesi. Her çalışma zamanı testi yeni kontrollü bir işçi başlatır; beklenen başarısızlık doğrulamaları başarısızlık olarak test edilir, başarılı senaryo olarak raporlanmaz.

Aynı çalıştırmada Ruff, belge bağlantısı/SVG kontrolleri, kaynak ve wheel derlemeleri, kaynak yayımlama politikası ve tam geçmiş sır taraması da geçti. Bu, belgelenen Python G/Ç koruması altında sentetik servis dağıtımını ve durum davranışını doğrular. İşletim sistemi güvenlik kum havuzu kurulduğunu göstermez, Docker çalıştırmasını doğrulamaz veya fiziksel cihaz davranışını kanıtlamaz.

## 2026-10-15 macOS geliştirme kontrolleri

Kaynak, sıkı girdi kabulü, Python denetim koruması, CLI çevirileri ve SVG yeniden üretimi macOS arm64 üzerinde Python 3.14.7 ile yerel olarak kontrol edildi. `python -m pytest -q -m 'not runtime'` **47 testi** geçti; bu komut yedi gerçek HA vakasını açıkça dışlar. `python -m ruff check src tests scripts` geçti. Bu tam çalışma zamanı paketinin yerine geçmez.

Gerçek Home Assistant 2026.10.0 motoru `automation`, `blueprint` ve `trace` bileşenlerini yükledi; varlık zaman aşımı ve elle geçersiz kılma senaryolarını beklenen sentetik servis çağrıları, son durumlar ve engellenen G/Ç olmadan çalıştırdı. Ardından yerel Python süreci yorumlayıcı kapanırken yerel bir segmentasyon hatasıyla çıktı. Üst çalıştırıcı, önce başarılı JSON yükü gelmiş olsa bile bu sıfırdan farklı çıkışı doğru biçimde çalışma zamanı hatası kabul eder. **macOS çalışma zamanı testinin tamamen geçtiği iddia edilmez.**

Sürüm kabul edilmeden önce tam Linux CI paketi gerekir. `python -m pytest -q --junitxml=junit.xml` çalıştırın; eksik HA, yanlış HA sürümleri, alt süreç zaman aşımları ve sıfırdan farklı çıkışlar başarısız olur, sessizce atlanmaz. Yukarıdaki bağlantılı çalıştırma bu uygulamanın Linux kanıtıdır; sonraki değişiklikler kendi başarılı çalıştırmalarını gerektirir. Bu kayıt Docker çalıştırması veya fiziksel cihaz doğrulaması iddia etmez.

## Kontrollü başlangıç meta verileri

İşçi, Python'ın önbelleğe alınmış işlemci meta verisi için sentetik `synthetic` değerini sağlar ve HA'yı içe aktarmadan önce `socket.has_ipv6` özelliğini kapatır. Böylece HA platform başlatması `uname -p` başlatmaz ve urllib3 içe aktarım sırasındaki localhost IPv6 bağlama denemesini yapmaz. Linux'ta ifaddr, koruma altında `ctypes.CDLL(None)` kullanılarak içe aktarılır ve süreçte zaten yüklenmiş libc sembolleri çözülür; bu, kitaplık bulucunun `ldconfig` alt sürecini önler. Normal kitaplık bulucu hemen geri yüklenir. G/Ç korumasında bu işlemler için izin listesi istisnası yoktur. Değişiklikler yalnızca ana makine meta verilerini/yoklamasını etkiler; HA tetikleyicileri, koşulları, zamanlayıcıları, yeniden yüklemesi, betikleri ve servis dağıtımı gerçektir. Sürüme duyarlıdırlar ve sabitlenmiş çalışma zamanı paketiyle kapsanırlar.

## Yeniden üretme

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Hiçbir rapor gerçek röle durumunu, radyo iletimini, evde bulunma doğruluğunu veya üretim sürelerindeki zamanlamayı kanıtlamaz. SVG zaman çizelgesi performans ölçümlerini değil, sentetik beklentileri gösterir.

Çalışma zamanı paketi, alt tüketicinin sentetik sözleşmesi `tests/fixtures/role_transfer.json` dosyasını da içerir: geçerli rol kapanır, kullanım dışı priz açık kalır. Bu fiziksel yük aktarımı testi değildir.
