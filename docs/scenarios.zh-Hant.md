# 場景契約 v1

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

權威驗證器是 `src/ha_scenario_tests/schema.py`。僅支援 JSON，上限 64 KiB。未知鍵、重複 JSON 鍵、符號連結輸入、非有限數值和無效型別都會被拒絕。不要將家庭設定複製到公開範例中。

必填根欄位：`schema: "ha-scenario/v1"`、簡短小寫的 `name`、`seed`、`automations`、`timeline`、`expect`。可選的 `settle_seconds` 預設為 0.1。所有實體 ID 都使用 `scenario_` 字首，且必須在初始資料中宣告。支援的域：`light`、`switch`、`input_boolean`、`binary_sensor`。支援的狀態：`on`、`off`、`unknown`、`unavailable`。

自動化包含 `id`、`triggers`、`actions`，以及可選的 `conditions` 和 `mode`（`single` 或 `restart`）。狀態觸發器必須包含 `trigger`、`entity_id`、`to`，可選 `from` 和 `for_seconds`。事件觸發器使用 `trigger: "event"` 和 `event_type: "scenario_name"`；也支援 `automation_reloaded`。條件僅支援狀態比較。操作包含 `action` 和一個 `entity_id`：對已初始化的 light/switch/input_boolean 實體執行 `turn_on`、`turn_off`、`toggle`。不接受模板、選擇器、裝置操作、藍圖、磁碟指令碼或服務資料。

時間軸步驟包含 `after`（從前一步完成起算的相對秒數），且必須恰好有一個操作：

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

其他操作：`"event": "scenario_manual_off"` 或 `"reload": true`。重新載入會呼叫 HA 真正的自動化服務，讀取生成的臨時 `configuration.yaml`；測試不會透過傳送重新載入完成事件來模仿重新載入。

`expect.calls` 是 `{action, entity_id}` 記錄嚴格按順序排列的完整列表，包括重複項；空列表禁止所有執行器呼叫。可選的 `expect.forbidden` 列出絕不能發生的呼叫。`expect.states` 將已初始化 ID 對應到最終狀態。即使最終狀態碰巧匹配，意外呼叫也會導致失敗。

限制：64 個初始實體、16 個自動化，每個自動化 8 個觸發器、8 個條件和 16 個操作，32 個時間軸步驟，請求等待總計 5 秒，256 次捕獲呼叫。背景任務錯誤和被阻止的 I/O 會使執行失敗。報告包含單調時鐘測得的呼叫/步驟耗時、已載入元件、最終狀態和失敗代碼。

父程序在返回報告前驗證工作程序的完整報告。`passed` 必須確實為布林型別，`physical_validation` 必須為 false，且模式、HA 版本、場景名、欄位和邊界必須符合協議。父程序還會按照場景檢查呼叫/狀態斷言，而不只相信成功標誌。無效輸出和工作程序的任何非零退出都是執行時錯誤，即使子程序列印了看似成功的 JSON 物件。

提供的陳舊資料範例用 `unavailable` 表示傳輸丟失。它不會透過 `last_changed` 推斷源資料新鮮度，不測試感測器時間戳解析，也不證明真實感測器的過期行為。手動覆蓋是一項明確合成策略；工具不會將該策略新增到現有自動化中。
