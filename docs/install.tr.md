# Kurulum ve yalıtım

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

Sabitlenmiş Home Assistant çalışma ortamını Python 3.14.2–3.14.x ile kullanın. Kök README'de gösterildiği gibi `requirements.lock` dosyasını `--require-hashes` ile yükleyin, ardından bu paketi `--no-deps .` ile kurun. Kilit dosyası uygulama ve test bağımlılıklarını kapsar. Temiz bir ortam gerekir; üretimdeki Home Assistant ortamınıza kurmayın. Kaynak kodu düzenlerken bunun yerine `pip install --no-deps -e .` kullanın.

Önce `ha-scenario validate examples/stale_sensor.json` çalıştırın. Doğrulama HA çalışma ortamını içe aktarmaz. Ardından `ha-scenario run examples/stale_sensor.json --report result.json` çalıştırın. Hedef sunucu yapılandırılmaz. Tek çıktı yolu senaryodan değil, açıkça verdiğiniz `--report` argümanından gelir.

Daha güçlü bir ağ sınırı için:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

Derleme, bağımlılıklar için İnternet erişimi gerektirir. Çalıştırma sırasında ağ yoktur; yazılabilir `/tmp` geçicidir. Ev yapılandırması, Docker soketi veya kimlik bilgileri bağlanmaz. Bu isteğe bağlı bir dağıtım tarifidir; tam olarak bu konteynerin çalıştırılıp çalıştırılmadığını doğrulama kaydından kontrol edin. Ana makine ağını veya üretim bağlamalarını eklemeyin.

Alt süreç arayüzü devralınan kimlik bilgilerini ve `PYTHONPATH` değerini temizler. İşçinin `-I` seçeneği kurulu paketi kullanır. Yalnızca PATH, SYSTEMROOT ve LANG devralınır; karma tohumu sabittir. Linux'ta işçinin kitaplık yolu çalışan Python kurulumunun `LIBDIR` değerinden türetilir; böylece taşınabilir Python derlemeleri libpython'ı bulabilir. Devralınan `LD_LIBRARY_PATH` asla kopyalanmaz. Alt süreç için üst süreçte 30 saniyelik, içeride 20 saniyelik zaman aşımı vardır; zaman çizelgesinde en fazla 5 saniye bekleme istenebilir ve 256 eylem yakalanabilir. Yerel bağımlılıkların takılması, üst sürecin zaman aşımıyla sonlandırılır.

pytest eklentisi otomatik kurulur. Bir test `ha_scenario_tests.schema.load` ile senaryo yükleyebilir ve `scenario_runner` fixture'ını çağırabilir. JUnit çıktısını pytest üretir. `run_scenario` normal Python kodunda da içe aktarılabilir.
