# 安装与隔离

<!-- language-navigation:start -->
<p dir="ltr">
<a href="install.md" lang="en" dir="ltr">English</a> ·
<a href="install.ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="install.bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="install.cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="install.de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="install.es.md" lang="es" dir="ltr">Español</a> ·
<a href="install.fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="install.fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="install.he.md" lang="he" dir="rtl">עברית</a> ·
<a href="install.hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="install.id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="install.it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="install.ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="install.ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="install.nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="install.pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="install.pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="install.ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="install.th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="install.tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="install.uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="install.vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="install.zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="install.zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->

请使用固定版本的 Home Assistant 运行时及 Python 3.14.2–3.14.x。按照根目录 README，先通过 `--require-hashes` 安装 `requirements.lock`，再通过 `--no-deps .` 安装本包。锁文件涵盖应用和测试依赖。必须使用干净环境；不要安装到生产 Home Assistant 环境。编辑源码时，改用 `pip install --no-deps -e .`。

先运行 `ha-scenario validate examples/stale_sensor.json`。验证不会导入 HA 运行时。随后运行 `ha-scenario run examples/stale_sensor.json --report result.json`。不配置目标服务器。唯一的输出路径来自你显式提供的 `--report` 参数，而非场景文件。

如需更强的网络隔离边界：

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

构建需要联网下载依赖。运行时无网络，只有一次性的可写 `/tmp`；不挂载家庭配置、Docker 套接字或凭据。这是可选部署方案；是否实际执行过这个容器，请查阅验证记录。不要加入主机网络或生产目录挂载。

子进程接口会移除继承的凭据和 `PYTHONPATH`。工作进程的 `-I` 使用已安装的包。仅继承 PATH、SYSTEMROOT 和 LANG；哈希种子固定。Linux 上，工作进程库路径取自当前 Python 安装的 `LIBDIR`，使可迁移的 Python 构建能够找到 libpython。绝不复制继承的 `LD_LIBRARY_PATH`。父进程对子进程设置 30 秒超时，内部超时为 20 秒；时间线请求的等待总计最多 5 秒，最多捕获 256 次操作。原生依赖卡住时，由父进程超时机制终止。

pytest 插件会自动安装。测试可以通过 `ha_scenario_tests.schema.load` 加载场景并调用 `scenario_runner` fixture。JUnit 由 pytest 自身生成。也可在普通 Python 中导入 `run_scenario`。
