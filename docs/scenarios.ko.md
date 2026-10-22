# 시나리오 계약 v1

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

기준 검증기는 `src/ha_scenario_tests/schema.py`입니다. JSON만 허용하며 최대 64 KiB입니다. 알 수 없는 키, 중복 JSON 키, 심볼릭 링크 입력, 유한하지 않은 수, 잘못된 타입은 거부합니다. 가정의 설정을 공개 예제로 복사하지 마세요.

필수 루트 필드는 `schema: "ha-scenario/v1"`, 짧은 소문자 `name`, `seed`, `automations`, `timeline`, `expect`입니다. 선택적인 `settle_seconds`의 기본값은 0.1입니다. 모든 엔티티 ID는 `scenario_` 접두사를 사용하며 초기 데이터에 선언해야 합니다. 지원 도메인은 `light`, `switch`, `input_boolean`, `binary_sensor`입니다. 지원 상태는 `on`, `off`, `unknown`, `unavailable`입니다.

자동화에는 `id`, `triggers`, `actions`, 선택적인 `conditions`와 `mode`(`single` 또는 `restart`)가 있습니다. 상태 트리거에는 `trigger`, `entity_id`, `to`가 필수이며 `from`, `for_seconds`는 선택 사항입니다. 이벤트 트리거는 `trigger: "event"`와 `event_type: "scenario_name"`을 사용하며 `automation_reloaded`도 지원합니다. 조건은 상태 비교만 가능합니다. 동작에는 `action`과 하나의 `entity_id`가 있으며, 초기화된 light/switch/input_boolean 엔티티에서 `turn_on`, `turn_off`, `toggle`을 실행합니다. 템플릿, 선택기, 기기 동작, 블루프린트, 디스크의 스크립트, 서비스 데이터는 허용하지 않습니다.

타임라인 단계에는 `after`(이전 단계가 완료된 후의 상대적인 초)와 정확히 하나의 작업이 들어갑니다.

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

다른 작업으로는 `"event": "scenario_manual_off"` 또는 `"reload": true`가 있습니다. 다시 불러오기는 HA의 실제 자동화 서비스를 호출하며, 이 서비스는 생성된 임시 `configuration.yaml`을 읽습니다. 테스트가 완료 이벤트를 발생시켜 다시 불러오기를 흉내 내는 것이 아닙니다.

`expect.calls`는 반복을 포함한 `{action, entity_id}` 레코드의 정확한 순서 목록입니다. 빈 목록은 모든 액추에이터 호출을 금지합니다. 선택적인 `expect.forbidden`은 절대 발생해서는 안 되는 호출을 나열합니다. `expect.states`는 초기화된 ID를 최종 상태에 매핑합니다. 최종 상태가 우연히 일치하더라도 예상하지 못한 호출이 있으면 실패합니다.

제한은 초기 엔티티 64개, 자동화 16개, 자동화당 트리거 8개와 조건 8개, 자동화당 동작 16개, 타임라인 단계 32개, 요청된 총 대기 5초, 캡처된 호출 256개입니다. 백그라운드 작업 오류나 차단된 I/O가 있으면 실행이 실패합니다. 보고서에는 단조 시계로 측정한 호출/단계 경과 시간, 로드한 구성요소, 최종 상태, 실패 코드가 포함됩니다.

부모는 워커의 전체 보고서를 검증한 뒤 반환합니다. `passed`는 실제 Boolean 타입이어야 하고 `physical_validation`은 false여야 하며, 스키마, HA 버전, 시나리오 이름, 필드, 경계값이 프로토콜과 일치해야 합니다. 부모는 성공 플래그만 믿지 않고 시나리오에 대해 호출/상태 단언도 확인합니다. 잘못된 출력과 워커의 모든 0이 아닌 종료 코드는 자식이 성공처럼 보이는 JSON 객체를 출력했더라도 런타임 오류입니다.

제공되는 오래된 데이터 예제는 `unavailable`로 전송 손실을 표현합니다. `last_changed`에서 원본의 최신성을 추론하거나 센서 타임스탬프 파싱을 테스트하거나 실제 센서의 만료 동작을 입증하지 않습니다. 수동 재정의는 명시적인 합성 정책이며, 이 도구가 기존 자동화에 해당 정책을 추가하지는 않습니다.
