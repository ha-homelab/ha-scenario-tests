# Senaryo sözleşmesi v1

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

Yetkili doğrulayıcı `src/ha_scenario_tests/schema.py` dosyasıdır. Yalnızca JSON kabul edilir, en fazla 64 KiB. Bilinmeyen anahtarlar, yinelenen JSON anahtarları, sembolik bağlantı girdileri, sonlu olmayan sayılar ve geçersiz türler reddedilir. Ev yapılandırmasını açık örneklere kopyalamayın.

Zorunlu kök alanları: `schema: "ha-scenario/v1"`, kısa küçük harfli bir `name`, `seed`, `automations`, `timeline`, `expect`. İsteğe bağlı `settle_seconds` varsayılan olarak 0.1'dir. Tüm varlık kimlikleri `scenario_` önekini kullanır ve başlangıç verilerinde bildirilmelidir. Desteklenen alanlar: `light`, `switch`, `input_boolean`, `binary_sensor`. Desteklenen durumlar: `on`, `off`, `unknown`, `unavailable`.

Bir otomasyon `id`, `triggers`, `actions`, isteğe bağlı `conditions` ve `mode` (`single` veya `restart`) içerir. Durum tetikleyicileri `trigger`, `entity_id`, `to` gerektirir; `from` ve `for_seconds` isteğe bağlıdır. Olay tetikleyicileri `trigger: "event"` ve `event_type: "scenario_name"` kullanır; `automation_reloaded` da desteklenir. Koşullar yalnızca durum karşılaştırmalarıdır. Eylemler `action` ve bir `entity_id` içerir: başlangıçta tanımlanmış light/switch/input_boolean varlıklarında `turn_on`, `turn_off`, `toggle`. Şablonlar, seçiciler, cihaz eylemleri, blueprint'ler, diskten betikler veya servis verileri kabul edilmez.

Zaman çizelgesi adımları `after` (önceki tamamlanan adımdan itibaren göreli saniye) ve tam bir işlem içerir:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Diğer işlemler: `"event": "scenario_manual_off"` veya `"reload": true`. Yeniden yükleme HA'nın gerçek otomasyon servisini çağırır; servis oluşturulan geçici `configuration.yaml` dosyasını okur. Test, tamamlanma olayını tetikleyerek yeniden yüklemeyi taklit etmez.

`expect.calls`, tekrarlar dahil `{action, entity_id}` kayıtlarının tam sıralı listesidir; boş liste bütün eyleyici çağrılarını yasaklar. `expect.forbidden`, hiç gerçekleşmemesi gereken çağrıları isteğe bağlı olarak listeler. `expect.states`, başlangıç kimliklerini son durumlara eşler. Beklenmeyen çağrılar, son durum tesadüfen eşleşse bile başarısızlığa yol açar.

Sınırlar: 64 başlangıç varlığı, 16 otomasyon, otomasyon başına 8 tetikleyici ve 8 koşul, otomasyon başına 16 eylem, 32 zaman çizelgesi adımı, toplam 5 saniye istenen bekleme, 256 yakalanan çağrı. Arka plan görevi hataları ve engellenen G/Ç çalıştırmayı başarısız kılar. Rapor monoton geçen çağrı/adım sürelerini, yüklenen bileşenleri, son durumları ve hata kodlarını içerir.

Üst süreç, işçinin tüm raporunu döndürmeden önce doğrular. `passed` gerçek bir Boolean türünde olmalı, `physical_validation` false olmalı; şema, HA sürümü, senaryo adı, alanlar ve sınırlar protokole uymalıdır. Üst süreç başarı bayrağına güvenmek yerine çağrı/durum doğrulamalarını senaryoyla karşılaştırır. Geçersiz çıktı ve işçinin sıfırdan farklı çıkışı, alt süreç başarılı görünen bir JSON nesnesi yazdırsa bile çalışma zamanı hatasıdır.

Sunulan eski veri örneği, aktarım kaybını `unavailable` ile gösterir. Kaynak güncelliğini `last_changed` üzerinden çıkarmaz, sensör zaman damgası ayrıştırmasını test etmez veya gerçek sensörün süre dolumu davranışını kanıtlamaz. Elle geçersiz kılma açık bir sentetik politikadır; araç bu politikayı mevcut otomasyona eklemez.
