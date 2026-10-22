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

- 安装/运行时退出码为 2：检查 Python 3.14.2–3.14.x、精确的 HA 固定版本和干净的虚拟环境。运行器会拒绝其他 HA 版本。报告失败前先从锁文件重新安装。
- 工作进程失败/超时：依赖导入或 HA 初始化失败。用**合成**文件直接运行隔离的工作进程以获得本地堆栈：`python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`。不要发布未经审查的环境诊断信息。
- `calls_mismatch`：比较顺序及重复调用，而不只是最终状态。初始状态在启动前设定；它们不会自动算作启动后的新状态触发器。
- `forbidden_call`：捕获的合成执行器命令匹配了禁止契约。这是真实的自动化分发，而不是物理动作。
- `states_mismatch`：时间线赋值或合成执行器留下了不同的状态。
- `blocked_io` 或 `background_exception`：绝不要为了通过检查而关闭防护。本版本不允许网络集成。请报告合成复现案例和版本。
- 定时器测试偶发失败：增大状态转换与断言截止时间之间的间隔。测量的是真实事件循环调度；不承诺虚拟时钟或精确到微秒的调度。
- 重载：真正的重载可能取消 `for` 定时器。如果策略要求恢复，需要显式的协调自动化；请比较 `reload_reconcile.json`。
- 报告已存在：`--report` 有意拒绝覆盖。请选择新路径。

在非可编辑安装后使用源码树时，应先重新安装包再测试改动。开发时使用 `--no-deps -e .` 安装。
