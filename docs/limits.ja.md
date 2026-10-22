# 対象範囲と証拠

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

本リリースは、実際の Home Assistant のトリガー、条件、タイマー、再読み込み、スクリプト操作のディスパッチを使って、範囲を限定したサブセットを検証します。アクチュエーターの受信先と入力状態は合成です。通信プロトコル、消費電流、センサー精度、リレーの物理状態、安全性、あらゆる HA 設定の動作を証明するものではありません。

時計は実際の単調経過時間を測ります。テストでは意図的に短い間隔とスケジューリングの余裕を設けます。HA 内部の遅延メソッドの改変、本番タイマーの長さの書き換え、仮想時間との同等性の主張は行いません。夏時間、実時刻に基づくスケジュール、HA プロセス全体の再起動、Recorder の永続化は v1 の対象外です。再読み込みはテストしますが、プロセスの再起動とは異なります。

入力には実行可能なテンプレートや統合設定を含みません。各ワーカーはクリーンな一時ディレクトリ、不要な変数を除去した環境、全体に適用する監査ガードを使用します。これにより、許可された経路での意図しない Python ネットワーク/サブプロセス I/O を防ぎます。悪意あるコードのサンドボックスではありません。Python/ネイティブ依存関係、インタープリター、ホストは信頼する前提です。信頼できないソースや依存関係は別途保護した環境でのみ実行してください。任意の Docker network-none 手順はネットワーク隔離を強化しますが、ハードウェアの動作は証明しません。

公開レポートには合成 fixture のみを含めてください。実際の状態タイムラインは、トークンがなくても在宅状況や習慣を明らかにします。ここには家庭内機器一覧、録音・録画、本番設定は含まれません。すべての図は合成と明記され、`python scripts/render_diagrams.py` で再生成できます。

本リリースで実施し測定したチェックは[検証](validation.ja.md)を参照してください。インストールのサポートはその記録にある環境に限られます。コンテナー手順があることは、すべてのプラットフォームをテスト済みという意味ではありません。
