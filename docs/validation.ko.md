# 검증 기록

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

## 2026-10-15 Linux 런타임 검증

[GitHub Actions 실행 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199)는 Ubuntu의 CPython 3.14.8과 고정된 Home Assistant 2026.10.0을 사용하여 커밋 `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`에서 통과했습니다. 전체 명령 `python3 -m pytest -q`는 건너뛴 테스트 없이 **21.42초 만에 54개 통과**로 완료했습니다. 여기에는 실제 HA 런타임 테스트 7개가 모두 포함됩니다. 예제 시나리오 4개, 의도적으로 실패하는 기대/금지 동작 사례, 현지화된 CLI JSON 보고서, 하위 사용자의 역할 이전 계약입니다. 각 런타임 테스트는 새 제어 워커를 시작하며, 실패가 예상되는 단언은 실패로 테스트하고 성공 시나리오로 보고하지 않습니다.

같은 실행에서 Ruff, 문서 링크/SVG 검사, 소스 및 wheel 빌드, 소스 공개 정책, 전체 이력 비밀 검사도 통과했습니다. 이는 문서화된 Python I/O 가드 아래에서 합성 서비스 전달과 상태 동작을 검증합니다. OS 보안 샌드박스를 입증하거나 Docker 실행을 검증하거나 물리적 기기의 동작을 증명하지는 않습니다.

## 2026-10-15 macOS 개발 검사

소스, 엄격한 입력 허용, Python 감사 가드, CLI 번역, SVG 재생성을 macOS arm64의 Python 3.14.7로 로컬에서 확인했습니다. `python -m pytest -q -m 'not runtime'`은 **47개 테스트**를 통과했으며, 이 명령은 실제 HA 사례 7개를 명시적으로 제외합니다. `python -m ruff check src tests scripts`도 통과했습니다. 이는 전체 런타임 테스트 모음을 대체하지 않습니다.

실제 Home Assistant 2026.10.0 엔진은 `automation`, `blueprint`, `trace`를 로드하고 재실 시간 초과와 수동 재정의 시나리오를 실행했습니다. 합성 서비스 호출과 최종 상태가 예상과 일치했고 차단된 I/O는 없었습니다. 이후 로컬 Python 프로세스가 인터프리터 정리 도중 네이티브 세그멘테이션 오류로 종료했습니다. 부모 실행기는 그 전에 성공 JSON 데이터가 있었더라도 이 0이 아닌 종료를 런타임 실패로 올바르게 처리합니다. **macOS 런타임 테스트가 완전히 통과했다고 주장하지 않습니다.**

릴리스를 승인하려면 전체 Linux CI 모음이 필요합니다. `python -m pytest -q --junitxml=junit.xml`을 실행하세요. HA 누락, 잘못된 HA 버전, 자식 시간 초과, 0이 아닌 자식 종료는 실패하며 조용히 건너뛰지 않습니다. 위 링크의 실행은 이 구현에 대한 Linux 증거이며, 후속 변경에는 각각 통과한 실행이 필요합니다. 이 기록은 Docker 실행이나 물리적 기기 검증을 주장하지 않습니다.

## 제어된 부트스트랩 메타데이터

워커는 Python이 캐시한 프로세서 메타데이터에 합성 값 `synthetic`을 제공하고 HA를 가져오기 전에 `socket.has_ipv6`를 비활성화합니다. 이는 HA 플랫폼 초기화가 `uname -p`를 생성하는 것과 urllib3가 가져오기 시 localhost IPv6 bind 탐지를 수행하는 것을 방지합니다. Linux에서는 가드 아래에서 `ctypes.CDLL(None)`을 사용해 ifaddr를 가져오고 프로세스에 이미 로드된 libc 심볼을 확인하므로 라이브러리 탐색기의 `ldconfig` 하위 프로세스를 피합니다. 일반 라이브러리 탐색기는 즉시 복원합니다. I/O 가드에는 이 작업들을 위한 허용 목록 예외가 없습니다. 이 변경은 호스트 메타데이터/탐지에만 영향을 줍니다. HA 트리거, 조건, 타이머, 다시 불러오기, 스크립트, 서비스 전달은 실제로 동작합니다. 버전에 민감하며 고정된 런타임 테스트 모음이 이를 다룹니다.

## 재현

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

어떤 보고서도 실제 릴레이 상태, 무선 전달, 가정 내 재실 정확도, 운영 시간 길이의 타이밍을 입증하지 않습니다. SVG 타임라인은 벤치마크 측정이 아니라 합성 기대를 보여줍니다.

런타임 모음에는 하위 사용자의 합성 계약인 `tests/fixtures/role_transfer.json`도 포함됩니다. 현재 역할은 꺼지고 역할에서 제외된 플러그는 켜진 상태를 유지합니다. 이는 물리적 부하 이전 테스트가 아닙니다.
