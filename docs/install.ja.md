# インストールと隔離

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

固定バージョンの Home Assistant ランタイムを Python 3.14.2–3.14.x で使用してください。ルートの README に従い、`--require-hashes` で `requirements.lock` をインストールしてから、`--no-deps .` で本パッケージをインストールします。ロックファイルはアプリケーションとテストの依存関係を含みます。クリーンな環境が必要です。本番の Home Assistant 環境にはインストールしないでください。ソースを編集する場合は、代わりに `pip install --no-deps -e .` を使用します。

最初に `ha-scenario validate examples/stale_sensor.json` を実行します。検証では HA ランタイムをインポートしません。次に `ha-scenario run examples/stale_sensor.json --report result.json` を実行します。対象サーバーは設定しません。出力パスはシナリオではなく、明示的に指定した `--report` 引数からのみ取得します。

ネットワークの隔離を強化する場合：

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

ビルドには依存関係を取得するためのインターネット接続が必要です。実行時はネットワークを使わず、書き込み可能な `/tmp` は使い捨てです。家庭の設定、Docker ソケット、認証情報はマウントしません。これは任意のデプロイ手順です。このコンテナーを実際に実行したかどうかは検証記録を確認してください。ホストネットワークや本番環境のマウントを追加しないでください。

サブプロセスのインターフェースは、継承した認証情報と `PYTHONPATH` を除去します。ワーカーの `-I` はインストール済みパッケージを使用します。継承するのは PATH、SYSTEMROOT、LANG のみで、ハッシュのシードは固定です。Linux では実行中の Python インストールの `LIBDIR` からワーカーのライブラリパスを導き、移設可能な Python ビルドでも libpython を検出できるようにします。継承した `LD_LIBRARY_PATH` は決してコピーしません。子プロセスには親側で 30 秒、内部で 20 秒のタイムアウトがあり、タイムラインで要求できる待機は合計 5 秒、記録できる操作は 256 件までです。ネイティブ依存関係のハングは親のタイムアウトによって終了します。

pytest プラグインは自動的にインストールされます。テストは `ha_scenario_tests.schema.load` でシナリオを読み込み、`scenario_runner` fixture を呼び出せます。JUnit は pytest 自体が生成します。通常の Python コードから `run_scenario` をインポートすることもできます。
