# 范围与证据

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

本版本通过真正的 Home Assistant 触发器、条件、定时器、重载和脚本操作分发，验证一个有界子集。执行器接收端和输入状态均为合成数据。它不能证明通信协议、电流消耗、传感器精度、继电器物理状态、安全性或所有可能的 HA 配置行为。

时钟使用真实流逝的单调时间。测试有意采用短间隔和调度余量。我们不修改 HA 内部延迟方法，不改写生产定时器时长，也不宣称与虚拟时间等价。夏令时、墙上时钟调度、完整 HA 进程重启和 Recorder 持久化不在 v1 范围内。重载经过测试；它并不是进程重启。

输入不含可执行模板或集成配置。每个工作进程使用干净临时目录、精简环境和全局审计防护。这能防止在准入路径中意外发生 Python 网络/子进程 I/O，但不是恶意代码沙箱：Python/原生依赖、解释器和主机均视为可信。只应在另行加固的环境中运行不可信源码或依赖。可选 Docker network-none 方案增强网络隔离，但不能证明硬件行为。

公开报告应只包含合成 fixture。即使没有令牌，真实状态时间线也会泄露居家情况和生活习惯。这里不包含家庭设备清单、录制内容或生产配置。所有图表均标明为合成数据，可用 `python scripts/render_diagrams.py` 复现。

本版本实际执行并测量的检查见[验证](validation.zh-Hans.md)。安装支持仅限该记录所列环境；提供容器方案不代表每个平台都测试过。
