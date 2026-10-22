# 场景契约 v1

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

权威验证器是 `src/ha_scenario_tests/schema.py`。仅支持 JSON，上限 64 KiB。未知键、重复 JSON 键、符号链接输入、非有限数值和无效类型都会被拒绝。不要将家庭配置复制到公开示例中。

必填根字段：`schema: "ha-scenario/v1"`、简短小写的 `name`、`seed`、`automations`、`timeline`、`expect`。可选的 `settle_seconds` 默认为 0.1。所有实体 ID 都使用 `scenario_` 前缀，且必须在初始数据中声明。支持的域：`light`、`switch`、`input_boolean`、`binary_sensor`。支持的状态：`on`、`off`、`unknown`、`unavailable`。

自动化包含 `id`、`triggers`、`actions`，以及可选的 `conditions` 和 `mode`（`single` 或 `restart`）。状态触发器必须包含 `trigger`、`entity_id`、`to`，可选 `from` 和 `for_seconds`。事件触发器使用 `trigger: "event"` 和 `event_type: "scenario_name"`；也支持 `automation_reloaded`。条件仅支持状态比较。操作包含 `action` 和一个 `entity_id`：对已初始化的 light/switch/input_boolean 实体执行 `turn_on`、`turn_off`、`toggle`。不接受模板、选择器、设备操作、蓝图、磁盘脚本或服务数据。

时间线步骤包含 `after`（从前一步完成起算的相对秒数），且必须恰好有一个操作：

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

其他操作：`"event": "scenario_manual_off"` 或 `"reload": true`。重载会调用 HA 真正的自动化服务，读取生成的临时 `configuration.yaml`；测试不会通过发送重载完成事件来模仿重载。

`expect.calls` 是 `{action, entity_id}` 记录严格按顺序排列的完整列表，包括重复项；空列表禁止所有执行器调用。可选的 `expect.forbidden` 列出绝不能发生的调用。`expect.states` 将已初始化 ID 映射到最终状态。即使最终状态碰巧匹配，意外调用也会导致失败。

限制：64 个初始实体、16 个自动化，每个自动化 8 个触发器、8 个条件和 16 个操作，32 个时间线步骤，请求等待总计 5 秒，256 次捕获调用。后台任务错误和被阻止的 I/O 会使运行失败。报告包含单调时钟测得的调用/步骤耗时、已加载组件、最终状态和失败代码。

父进程在返回报告前验证工作进程的完整报告。`passed` 必须确实为布尔类型，`physical_validation` 必须为 false，且模式、HA 版本、场景名、字段和边界必须符合协议。父进程还会按照场景检查调用/状态断言，而不只相信成功标志。无效输出和工作进程的任何非零退出都是运行时错误，即使子进程打印了看似成功的 JSON 对象。

提供的陈旧数据示例用 `unavailable` 表示传输丢失。它不会通过 `last_changed` 推断源数据新鲜度，不测试传感器时间戳解析，也不证明真实传感器的过期行为。手动覆盖是一项显式合成策略；工具不会将该策略添加到现有自动化中。
