# シナリオ契約 v1

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

正規のバリデーターは `src/ha_scenario_tests/schema.py` です。JSON のみ、最大 64 KiB を受け付けます。不明なキー、重複 JSON キー、シンボリックリンクの入力、非有限数、不正な型は拒否されます。家庭の設定を公開例にコピーしないでください。

必須のルートフィールドは `schema: "ha-scenario/v1"`、短い小文字の `name`、`seed`、`automations`、`timeline`、`expect` です。任意の `settle_seconds` は既定で 0.1 です。すべてのエンティティ ID は `scenario_` プレフィックスを使用し、初期データに宣言する必要があります。対応ドメインは `light`、`switch`、`input_boolean`、`binary_sensor`、対応状態は `on`、`off`、`unknown`、`unavailable` です。

オートメーションには `id`、`triggers`、`actions`、任意の `conditions` と `mode`（`single` または `restart`）があります。状態トリガーには `trigger`、`entity_id`、`to` が必須で、`from` と `for_seconds` は任意です。イベントトリガーは `trigger: "event"` と `event_type: "scenario_name"` を使用し、`automation_reloaded` にも対応します。条件は状態比較のみです。操作には `action` と 1 つの `entity_id` があり、初期化済み light/switch/input_boolean エンティティに対して `turn_on`、`turn_off`、`toggle` を実行します。テンプレート、セレクター、デバイス操作、ブループリント、ディスク上のスクリプト、サービスデータは許可されません。

タイムラインの各ステップには `after`（前のステップが完了してからの相対秒数）と、ちょうど 1 つの操作を含めます。

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

ほかの操作は `"event": "scenario_manual_off"` または `"reload": true` です。再読み込みは HA の実際のオートメーションサービスを呼び出し、生成した一時的な `configuration.yaml` を読み取ります。テストは完了イベントを発火して再読み込みを模倣するわけではありません。

`expect.calls` は、繰り返しも含めた `{action, entity_id}` レコードの厳密な順序付きリストです。空リストはすべてのアクチュエーター呼び出しを禁止します。任意の `expect.forbidden` は決して発生してはいけない呼び出しを列挙します。`expect.states` は初期化済み ID を最終状態に対応付けます。最終状態がたまたま一致しても、想定外の呼び出しがあれば失敗します。

上限は初期エンティティ 64、オートメーション 16、各オートメーションにトリガー 8、条件 8、操作 16、タイムラインステップ 32、要求待機合計 5 秒、記録する呼び出し 256 件です。バックグラウンドタスクのエラーやブロックされた I/O は実行を失敗させます。レポートには単調時計による呼び出し/ステップの経過時間、読み込んだコンポーネント、最終状態、失敗コードを含みます。

親プロセスはワーカーの完全なレポートを検証してから返します。`passed` は実際に Boolean 型でなければならず、`physical_validation` は false、スキーマ、HA バージョン、シナリオ名、フィールド、範囲はプロトコルに一致する必要があります。親は成功フラグを信用するだけでなく、シナリオに対して呼び出し/状態のアサーションも確認します。不正な出力やワーカーの非ゼロ終了は、子が成功らしい JSON オブジェクトを出力していてもランタイムエラーです。

付属の古いデータの例は、通信喪失を `unavailable` で表します。`last_changed` から情報源の鮮度を推測したり、センサーのタイムスタンプ解析をテストしたり、実センサーの期限切れ動作を証明したりはしません。手動オーバーライドは明示的な合成ポリシーであり、ツールが既存オートメーションにそのポリシーを追加することはありません。
