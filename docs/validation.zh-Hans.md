# 验证记录

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

## 2026-10-15 Linux 运行时验证

[GitHub Actions 运行 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) 在提交 `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` 上通过，环境为 Ubuntu、CPython 3.14.8 和固定的 Home Assistant 2026.10.0。完整命令 `python3 -m pytest -q` 在 **21.42 秒内通过 54 项测试**，没有跳过项。其中包含全部七项真实 HA 运行时测试：四个示例场景、一个故意失败的期望/禁止操作案例、本地化 CLI JSON 报告，以及下游角色转移契约。每项运行时测试都启动新的受控工作进程；预期失败断言按失败进行测试，不会被报告为成功场景。

同一次运行中，Ruff、文档链接/SVG 检查、源码和 wheel 构建、源码发布策略及完整历史秘密扫描也全部通过。这验证了在所述 Python I/O 防护下的合成服务分发和状态行为，但不能确立操作系统安全沙箱，也不验证 Docker 执行或证明物理设备行为。

## 2026-10-15 macOS 开发检查

在 macOS arm64 上用 Python 3.14.7 本地检查了源码、严格输入准入、Python 审计防护、CLI 翻译和 SVG 重新生成。`python -m pytest -q -m 'not runtime'` 通过 **47 项测试**；该命令明确排除了七项真实 HA 案例。`python -m ruff check src tests scripts` 通过。这不能替代完整运行时测试集。

真实 Home Assistant 2026.10.0 引擎加载了 `automation`、`blueprint` 和 `trace`，执行了在场超时与手动覆盖场景，得到预期的合成服务调用、最终状态，且没有被阻止的 I/O。随后本地 Python 进程在解释器清理期间因原生段错误退出。父运行器正确地将该非零退出视为运行时失败，即使此前已输出成功的 JSON 内容。**不宣称 macOS 运行时测试完整通过。**

接受发布前必须通过完整 Linux CI 测试集。运行 `python -m pytest -q --junitxml=junit.xml`；HA 缺失、HA 版本错误、子进程超时或非零退出都会失败，绝不静默跳过。上述链接运行是本实现的 Linux 证据；后续改动需要各自通过一次运行。本记录不宣称执行过 Docker 或验证过物理设备。

## 受控启动元数据

工作进程向 Python 缓存的处理器元数据提供合成值 `synthetic`，并在导入 HA 前关闭 `socket.has_ipv6`。这阻止 HA 平台初始化启动 `uname -p`，也阻止 urllib3 在导入时进行 localhost IPv6 绑定探测。在 Linux 上，ifaddr 在防护下使用 `ctypes.CDLL(None)` 导入，解析进程内已经加载的 libc 符号，从而避免库查找器启动 `ldconfig` 子进程。普通库查找器随后立即恢复。I/O 防护没有为这些操作设置允许列表例外。这些改动仅影响主机元数据/探测；HA 触发器、条件、定时器、重载、脚本和服务分发均为真实执行。它们对版本敏感，并由固定版本运行时测试集覆盖。

## 复现

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

没有任何报告能证明真实继电器状态、无线送达、家庭在场检测精度或生产时长下的定时行为。SVG 时间线展示的是合成期望，而非基准测量结果。

运行时测试集还包括 `tests/fixtures/role_transfer.json`，即合成的下游契约：当前角色关闭，退出使用的插座保持开启。这不是物理负载转移测试。
