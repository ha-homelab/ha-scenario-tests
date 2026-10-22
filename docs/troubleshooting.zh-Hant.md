# 故障排查

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

- 安裝/執行時退出碼為 2：檢查 Python 3.14.2–3.14.x、精確的 HA 固定版本和乾淨的虛擬環境。執行器會拒絕其他 HA 版本。報告失敗前先從鎖定檔重新安裝。
- 工作程序失敗/逾時：相依套件匯入或 HA 初始化失敗。用**合成**檔案直接執行隔離的工作程序以獲得本地堆疊：`python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`。不要發布未經審查的環境診斷資訊。
- `calls_mismatch`：比較順序及重複呼叫，而不只是最終狀態。初始狀態在啟動前設定；它們不會自動算作啟動後的新狀態觸發器。
- `forbidden_call`：捕獲的合成執行器命令匹配了禁止契約。這是真實的自動化分發，而不是物理動作。
- `states_mismatch`：時間軸賦值或合成執行器留下了不同的狀態。
- `blocked_io` 或 `background_exception`：絕不要為了通過檢查而關閉防護。本版本不允許網路整合。請報告合成重現案例和版本。
- 定時器測試偶發失敗：增大狀態轉換與斷言截止時間之間的間隔。測量的是真實事件迴圈排程；不承諾虛擬時鐘或精確到微秒的排程。
- 重新載入：真正的重新載入可能取消 `for` 定時器。如果策略要求恢復，需要明確的協調自動化；請比較 `reload_reconcile.json`。
- 報告已存在：`--report` 有意拒絕覆蓋。請選擇新路徑。

在非可編輯安裝後使用原始碼樹時，應先重新安裝套件再測試改動。開發時使用 `--no-deps -e .` 安裝。
