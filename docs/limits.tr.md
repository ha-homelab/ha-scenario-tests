# Kapsam ve kanıtlar

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

Bu sürüm, gerçek Home Assistant tetikleyicileri, koşulları, zamanlayıcıları, yeniden yüklemesi ve betik eylemi dağıtımıyla sınırlı bir alt kümeyi doğrular. Eyleyici alıcıları ve giriş durumları sentetiktir. İletişim protokollerini, çekilen akımı, sensör doğruluğunu, rölenin fiziksel durumunu, güvenliği veya her olası HA yapılandırmasının davranışını kanıtlamaz.

Saat, gerçek geçen monoton zamandır. Testler kasıtlı olarak kısa aralıklar ve zamanlama payı kullanır. HA'nın dahili gecikme yöntemlerini yamalamaz, üretim zamanlayıcılarının sürelerini yeniden yazmaz ve sanal zaman eşdeğerliği iddia etmeyiz. Yaz/kış saati, duvar saatine göre zamanlama, tam HA süreç yeniden başlatması ve Recorder kalıcılığı v1 kapsamı dışındadır. Yeniden yükleme test edilir; süreç yeniden başlatması değildir.

Girdi çalıştırılabilir şablon veya entegrasyon yapılandırması içermez. Her işçi temiz bir geçici dizin, sadeleştirilmiş ortam ve genel denetim koruması kullanır. Bu, izin verilen yol üzerinden yanlışlıkla yapılan Python ağ/alt süreç G/Ç'sini önler. Zararlı kod için bir kum havuzu değildir: Python/yerel bağımlılıklara, yorumlayıcıya ve ana makineye güvenilir. Güvenilmeyen kaynak veya bağımlılıkları yalnızca ayrı güvenceye alınmış bir ortamda çalıştırın. İsteğe bağlı Docker network-none tarifi ağ yalıtımını güçlendirir ama donanım davranışını kanıtlamaz.

Açık raporlar yalnızca sentetik fixture'lar içermelidir. Gerçek durum zaman çizelgeleri, token olmadan da evde bulunma durumunu ve alışkanlıkları açığa çıkarır. Burada ev envanteri, kayıt veya üretim yapılandırması bulunmaz. Tüm diyagramlar sentetik olarak işaretlenmiştir ve `python scripts/render_diagrams.py` ile yeniden üretilebilir.

Bu sürümde gerçekleştirilen ölçülmüş kontroller için [doğrulamaya](validation.md) bakın. Kurulum desteği bu kayıttaki ortamlarla sınırlıdır; konteyner tarifi her platformun test edildiği anlamına gelmez.
