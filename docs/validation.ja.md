# 検証記録

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

## 2026-10-15 Linux ランタイム検証

[GitHub Actions 実行 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) はコミット `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4` で成功しました。環境は Ubuntu 上の CPython 3.14.8 と固定された Home Assistant 2026.10.0 です。完全なコマンド `python3 -m pytest -q` は、スキップなしで **54 件合格、21.42 秒**で完了しました。これには実際の HA を使う 7 件すべてのランタイムテストが含まれます。内訳は 4 つの例示シナリオ、意図的に失敗する期待値/禁止操作のケース、ローカライズされた CLI JSON レポート、下流の役割移行契約です。各ランタイムテストは新しい制御下のワーカーを開始します。失敗が期待されるアサーションは失敗としてテストし、成功したシナリオとしては報告しません。

同じ実行で Ruff、文書リンク/SVG の確認、ソースと wheel のビルド、ソース公開ポリシー、全履歴の秘密情報スキャンも成功しました。これは記載した Python I/O ガードの下での合成サービスのディスパッチと状態動作を検証します。OS のセキュリティサンドボックスを確立したり、Docker の実行を検証したり、物理デバイスの動作を証明したりするものではありません。

## 2026-10-15 macOS 開発時チェック

ソース、厳格な入力受け入れ、Python 監査ガード、CLI 翻訳、SVG 再生成を macOS arm64 の Python 3.14.7 でローカル確認しました。`python -m pytest -q -m 'not runtime'` は **47 件**合格しました。このコマンドは実際の HA を使う 7 ケースを明示的に除外します。`python -m ruff check src tests scripts` も成功しました。これは完全なランタイムテスト群の代わりにはなりません。

実際の Home Assistant 2026.10.0 エンジンは `automation`、`blueprint`、`trace` を読み込み、在室タイムアウトと手動オーバーライドのシナリオを実行しました。合成サービス呼び出しと最終状態は期待どおりで、ブロックされた I/O はありませんでした。その後ローカルの Python プロセスは、インタープリター終了処理中のネイティブなセグメンテーション違反で終了しました。親ランナーは、直前に成功した JSON ペイロードがあっても、この非ゼロ終了を正しくランタイム失敗として扱います。**macOS の完全なランタイムテストが合格したとは主張しません。**

リリースを受け入れる前に、完全な Linux CI テスト群が必要です。`python -m pytest -q --junitxml=junit.xml` を実行してください。HA の欠如、誤った HA バージョン、子のタイムアウト、子の非ゼロ終了は失敗となり、黙ってスキップしません。上記リンクの実行はこの実装の Linux における証拠です。以後の変更にはそれぞれ合格した実行が必要です。この記録では Docker 実行や物理デバイスの検証を主張しません。

## 制御されたブートストラップメタデータ

ワーカーは Python がキャッシュしたプロセッサーメタデータに合成値 `synthetic` を与え、HA のインポート前に `socket.has_ipv6` を無効にします。これにより HA のプラットフォーム初期化による `uname -p` の起動と、urllib3 のインポート時の localhost IPv6 bind 検査を防ぎます。Linux では、ifaddr をガード下で `ctypes.CDLL(None)` を使ってインポートし、プロセスにロード済みの libc シンボルを解決します。これでライブラリ検索処理の `ldconfig` サブプロセスを回避します。通常のライブラリ検索処理は直ちに復元します。I/O ガードにこれらの操作の許可リスト例外はありません。変更対象はホストのメタデータ/検査のみです。HA のトリガー、条件、タイマー、再読み込み、スクリプト、サービスのディスパッチは実際に動作します。これらはバージョンに依存し、固定ランタイムのテスト群でカバーされています。

## 再現

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

実際のリレー状態、無線の到達、家庭内の在室検知精度、本番の長さのタイミングを証明するレポートはありません。SVG タイムラインは合成の期待値であり、ベンチマーク測定ではありません。

ランタイムテスト群には下流の合成契約 `tests/fixtures/role_transfer.json` も含まれます。現在の役割はオフになり、役割を退いたプラグはオンのままです。物理的な負荷移行テストではありません。
