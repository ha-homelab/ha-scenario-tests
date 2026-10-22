# トラブルシューティング

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

- インストール/実行時の終了コード 2：Python 3.14.2–3.14.x、HA の正確な固定バージョン、クリーンな仮想環境を確認します。ランナーはほかの HA バージョンを拒否します。失敗を報告する前にロックファイルから再インストールしてください。
- ワーカーの失敗/タイムアウト：依存関係のインポートまたは HA セットアップに失敗しています。ローカルのトレースバックを得るには、**合成**ファイルを使って隔離ワーカーを直接実行します：`python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`。確認していない環境診断情報は公開しないでください。
- `calls_mismatch`：最終状態だけでなく、順序と重複した呼び出しを比較してください。初期状態は起動前に設定され、起動後の新しい状態トリガーとして自動的に数えられるわけではありません。
- `forbidden_call`：記録した合成アクチュエーターのコマンドが禁止契約に一致しました。これは実際のオートメーションのディスパッチであり、物理的な作動ではありません。
- `states_mismatch`：タイムラインの代入または合成アクチュエーターが異なる状態を残しました。
- `blocked_io` または `background_exception`：合格させるためにガードを無効化してはいけません。本リリースはネットワーク統合を許可しません。合成の再現例とバージョンを報告してください。
- 不安定なタイマーテスト：状態遷移とアサートする期限との間隔を広げます。測定するのは実際のイベントループのスケジューリングです。仮想時計や正確なマイクロ秒単位のスケジューリングを約束しません。
- 再読み込み：実際の再読み込みによって `for` タイマーがキャンセルされる場合があります。ポリシーが復旧を要求するなら明示的な整合化オートメーションが必要です。`reload_reconcile.json` と比較してください。
- 既存レポート：`--report` は意図的に上書きを拒否します。新しいパスを選んでください。

非編集可能インストールの後にソースツリーを使う場合、変更をテストする前にパッケージを再インストールします。開発時は `--no-deps -e .` でインストールしてください。
