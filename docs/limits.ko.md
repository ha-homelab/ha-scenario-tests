# 범위와 증거

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

이 릴리스는 실제 Home Assistant 트리거, 조건, 타이머, 다시 불러오기, 스크립트 동작 전달을 사용해 제한된 부분집합을 검증합니다. 액추에이터 수신부와 입력 상태는 합성 데이터입니다. 통신 프로토콜, 소비 전류, 센서 정확도, 릴레이의 물리적 상태, 안전성 또는 가능한 모든 HA 설정의 동작을 입증하지는 않습니다.

시계는 실제로 경과한 단조 시간을 사용합니다. 테스트는 의도적으로 짧은 간격과 스케줄링 여유를 둡니다. HA 내부 지연 메서드를 패치하거나 운영 타이머의 시간을 바꾸거나 가상 시간과 동등하다고 주장하지 않습니다. 일광 절약 시간, 실제 시각 기반 스케줄링, HA 프로세스 전체 재시작, Recorder 영속성은 v1 범위 밖입니다. 다시 불러오기는 테스트하지만 프로세스 재시작은 아닙니다.

입력에는 실행 가능한 템플릿이나 통합 설정이 없습니다. 각 워커는 깨끗한 임시 디렉터리, 정리된 환경, 전역 감사 가드를 사용합니다. 이는 허용된 경로에서 우발적인 Python 네트워크/하위 프로세스 I/O를 방지합니다. 악성 코드 샌드박스는 아닙니다. Python/네이티브 의존성, 인터프리터, 호스트는 신뢰합니다. 신뢰할 수 없는 소스나 의존성은 별도로 보호한 환경에서만 실행하세요. 선택적인 Docker network-none 방식은 네트워크 격리를 강화하지만 하드웨어 동작을 입증하지는 않습니다.

공개 보고서에는 합성 fixture만 포함해야 합니다. 실제 상태 타임라인은 토큰이 없어도 재실 여부와 생활 습관을 드러냅니다. 여기에는 가정 내 기기 목록, 녹음·녹화, 운영 설정이 포함되지 않습니다. 모든 다이어그램에는 합성임을 표시하며 `python scripts/render_diagrams.py`로 재현할 수 있습니다.

이 릴리스에서 측정한 검사 결과는 [검증](validation.md)을 참고하세요. 설치 지원은 해당 기록에 있는 환경으로 제한됩니다. 컨테이너 실행 방법이 있다고 해서 모든 플랫폼을 테스트했다는 뜻은 아닙니다.
