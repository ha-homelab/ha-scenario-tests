# 문제 해결

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

- 설치/실행 시 종료 코드 2: Python 3.14.2–3.14.x, 정확히 고정된 HA 버전, 깨끗한 가상 환경을 확인하세요. 실행기는 다른 HA 버전을 거부합니다. 실패를 보고하기 전에 잠금 파일로 다시 설치하세요.
- 워커 실패/시간 초과: 의존성 가져오기 또는 HA 설정이 실패했습니다. 로컬 traceback을 얻으려면 **합성** 파일로 격리된 워커를 직접 실행하세요: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. 검토하지 않은 환경 진단 자료를 공개하지 마세요.
- `calls_mismatch`: 최종 상태뿐 아니라 순서와 중복 호출을 비교하세요. 초기 상태는 시작 전에 설정하며, 시작 후의 새 상태 트리거로 자동 집계되지 않습니다.
- `forbidden_call`: 캡처한 합성 액추에이터 명령이 금지 계약과 일치했습니다. 이는 실제 자동화 전달이며 물리적 작동은 아닙니다.
- `states_mismatch`: 타임라인 할당 또는 합성 액추에이터가 다른 상태를 남겼습니다.
- `blocked_io` 또는 `background_exception`: 통과 결과를 얻으려고 가드를 끄지 마세요. 이 릴리스는 네트워크 통합을 허용하지 않습니다. 합성 재현 사례와 버전을 보고하세요.
- 불안정한 타이머 테스트: 상태 전환과 단언하는 기한 사이의 간격을 늘리세요. 실제 이벤트 루프 스케줄링을 측정하며 가상 시계나 정확한 마이크로초 스케줄링은 보장하지 않습니다.
- 다시 불러오기: 실제 다시 불러오기로 `for` 타이머가 취소될 수 있습니다. 정책상 복구가 필요하다면 명시적인 조정 자동화가 필요합니다. `reload_reconcile.json`과 비교하세요.
- 기존 보고서: `--report`는 의도적으로 덮어쓰기를 거부합니다. 새 경로를 선택하세요.

편집 불가 방식으로 설치한 뒤 소스 트리를 사용한다면 변경 사항을 테스트하기 전에 패키지를 다시 설치하세요. 개발할 때는 `--no-deps -e .`로 설치하세요.
