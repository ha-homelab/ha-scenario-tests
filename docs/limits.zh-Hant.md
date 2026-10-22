# 範圍與證據

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

本版本透過真正的 Home Assistant 觸發器、條件、定時器、重新載入和指令碼操作分發，驗證一個有界子集。執行器接收端和輸入狀態均為合成資料。它不能證明通訊協議、電流消耗、感測器精度、繼電器物理狀態、安全性或所有可能的 HA 設定行為。

時鐘使用真實流逝的單調時間。測試有意採用短間隔和排程餘量。我們不修改 HA 內部延遲方法，不改寫正式環境定時器時長，也不宣稱與虛擬時間等價。夏令時、實際時鐘排程、完整 HA 程序重啟和 Recorder 持久化不在 v1 範圍內。重新載入經過測試；它並不是程序重啟。

輸入不含可執行模板或整合設定。每個工作程序使用乾淨臨時目錄、精簡環境和全域審計防護。這能防止在准入路徑中意外發生 Python 網路/子程序 I/O，但不是惡意程式碼沙箱：Python/原生相依套件、直譯器和主機均視為可信。只應在另行加固的環境中執行不可信原始碼或相依套件。可選 Docker network-none 方案增強網路隔離，但不能證明硬體行為。

公開報告應只包含合成 fixture。即使沒有權杖，真實狀態時間軸也會洩露居家情況和生活習慣。這裡不包含家庭裝置清單、錄製內容或正式環境設定。所有圖表均標明為合成資料，可用 `python scripts/render_diagrams.py` 重現。

本版本實際執行並測量的檢查見[驗證](validation.zh-Hant.md)。安裝支援僅限該記錄所列環境；提供容器方案不代表每個平臺都測試過。
