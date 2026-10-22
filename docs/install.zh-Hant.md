# 安裝與隔離

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

請使用固定版本的 Home Assistant 執行時及 Python 3.14.2–3.14.x。按照根目錄 README，先透過 `--require-hashes` 安裝 `requirements.lock`，再透過 `--no-deps .` 安裝本套件。鎖定檔涵蓋應用和測試相依套件。必須使用乾淨環境；不要安裝到正式環境 Home Assistant 環境。編輯原始碼時，改用 `pip install --no-deps -e .`。

先執行 `ha-scenario validate examples/stale_sensor.json`。驗證不會匯入 HA 執行時。隨後執行 `ha-scenario run examples/stale_sensor.json --report result.json`。不設定目標伺服器。唯一的輸出路徑來自你明確提供的 `--report` 引數，而非場景檔案。

如需更強的網路隔離邊界：

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

建置需要聯網下載相依套件。執行時無網路，只有一次性的可寫 `/tmp`；不掛載家庭設定、Docker socket或認證資訊。這是可選部署方案；是否實際執行過這個容器，請查閱驗證記錄。不要加入主機網路或正式環境目錄掛載。

子程序介面會移除繼承的認證資訊和 `PYTHONPATH`。工作程序的 `-I` 使用已安裝的套件。僅繼承 PATH、SYSTEMROOT 和 LANG；雜湊種子固定。Linux 上，工作程序的程式庫路徑取自當前 Python 安裝的 `LIBDIR`，使可遷移的 Python 建置能夠找到 libpython。絕不複製繼承的 `LD_LIBRARY_PATH`。父程序對子程序設定 30 秒逾時，內部逾時為 20 秒；時間軸請求的等待總計最多 5 秒，最多捕獲 256 次操作。原生相依套件卡住時，由父程序逾時機制終止。

pytest 外掛會自動安裝。測試可以透過 `ha_scenario_tests.schema.load` 載入場景並呼叫 `scenario_runner` fixture。JUnit 由 pytest 自身生成。也可在普通 Python 中匯入 `run_scenario`。
