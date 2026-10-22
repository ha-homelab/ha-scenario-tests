# 驗證記錄

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

## 2026-10-15 Linux 執行時驗證

[GitHub Actions 執行 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) 在提交 `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` 上通過，環境為 Ubuntu、CPython 3.14.8 和固定的 Home Assistant 2026.10.0。完整命令 `python3 -m pytest -q` 在 **21.42 秒內通過 54 項測試**，沒有跳過項。其中包含全部七項真實 HA 執行時測試：四個範例場景、一個故意失敗的期望/禁止操作案例、本地化 CLI JSON 報告，以及下游角色轉移契約。每項執行時測試都啟動新的受控工作程序；預期失敗斷言按失敗進行測試，不會被報告為成功場景。

同一次執行中，Ruff、文件連結/SVG 檢查、原始碼和 wheel 建置、原始碼發布策略及完整歷史秘密掃描也全部通過。這驗證了在所述 Python I/O 防護下的合成服務分發和狀態行為，但不能確立作業系統安全沙箱，也不驗證 Docker 執行或證明物理裝置行為。

## 2026-10-15 macOS 開發檢查

在 macOS arm64 上用 Python 3.14.7 本地檢查了原始碼、嚴格輸入准入、Python 審計防護、CLI 翻譯和 SVG 重新生成。`python -m pytest -q -m 'not runtime'` 通過 **47 項測試**；該命令明確排除了七項真實 HA 案例。`python -m ruff check src tests scripts` 通過。這不能替代完整執行時測試集。

真實 Home Assistant 2026.10.0 引擎載入了 `automation`、`blueprint` 和 `trace`，執行了在場逾時與手動覆蓋場景，得到預期的合成服務呼叫、最終狀態，且沒有被阻止的 I/O。隨後本地 Python 程序在直譯器清理期間因原生記憶體區段錯誤退出。父執行器正確地將該非零退出視為執行時失敗，即使此前已輸出成功的 JSON 內容。**不宣稱 macOS 執行時測試完整通過。**

接受發布前必須通過完整 Linux CI 測試集。執行 `python -m pytest -q --junitxml=junit.xml`；HA 缺失、HA 版本錯誤、子程序逾時或非零退出都會失敗，絕不靜默跳過。上述連結執行是此實作的 Linux 證據；後續改動需要各自通過一次執行。本記錄不宣稱執行過 Docker 或驗證過物理裝置。

## 受控啟動後設資料

工作程序向 Python 快取的處理器後設資料提供合成值 `synthetic`，並在匯入 HA 前關閉 `socket.has_ipv6`。這阻止 HA 平臺初始化啟動 `uname -p`，也阻止 urllib3 在匯入時進行 localhost IPv6 繫結探測。在 Linux 上，ifaddr 在防護下使用 `ctypes.CDLL(None)` 匯入，解析程序內已經載入的 libc 符號，從而避免程式庫尋找器啟動 `ldconfig` 子程序。普通程式庫尋找器隨後立即恢復。I/O 防護沒有為這些操作設定允許列表例外。這些改動僅影響主機後設資料/探測；HA 觸發器、條件、定時器、重新載入、指令碼和服務分發均為真實執行。它們對版本敏感，並由固定版本執行時測試集覆蓋。

## 重現

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

沒有任何報告能證明真實繼電器狀態、無線送達、家庭在場檢測精度或正式環境時長下的定時行為。SVG 時間軸展示的是合成期望，而非基準測量結果。

執行時測試集還包括 `tests/fixtures/role_transfer.json`，即合成的下游契約：當前角色關閉，退出使用的插座保持開啟。這不是物理負載轉移測試。
