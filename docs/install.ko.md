# 설치와 격리

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

버전을 고정한 Home Assistant 런타임을 Python 3.14.2–3.14.x에서 사용하세요. 루트 README에 나온 대로 `--require-hashes`로 `requirements.lock`을 설치한 다음 `--no-deps .`로 이 패키지를 설치하세요. 잠금 파일에는 애플리케이션과 테스트 의존성이 포함됩니다. 깨끗한 환경이 필요하며, 운영 중인 Home Assistant 환경에는 설치하지 마세요. 소스를 수정할 때는 대신 `pip install --no-deps -e .`를 사용하세요.

먼저 `ha-scenario validate examples/stale_sensor.json`을 실행하세요. 검증은 HA 런타임을 가져오지 않습니다. 다음으로 `ha-scenario run examples/stale_sensor.json --report result.json`을 실행하세요. 대상 서버는 설정하지 않습니다. 유일한 출력 경로는 시나리오가 아니라 명시적으로 제공한 `--report` 인수에서 가져옵니다.

네트워크 격리를 강화하려면 다음과 같이 실행하세요.

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

빌드에는 의존성을 다운로드할 인터넷 연결이 필요합니다. 실행 중에는 네트워크가 없고 쓰기 가능한 `/tmp`는 일회용입니다. 집의 설정, Docker 소켓, 자격 증명은 마운트하지 않습니다. 이는 선택적인 배포 방법이며, 이 컨테이너를 실제 실행했는지는 검증 기록을 확인하세요. 호스트 네트워크나 운영 환경 마운트를 추가하지 마세요.

하위 프로세스 인터페이스는 상속받은 자격 증명과 `PYTHONPATH`를 제거합니다. 워커의 `-I`는 설치된 패키지를 사용합니다. PATH, SYSTEMROOT, LANG만 상속하며 해시 시드는 고정합니다. Linux에서는 실행 중인 Python 설치의 `LIBDIR`에서 워커 라이브러리 경로를 유도하므로 재배치 가능한 Python 빌드도 libpython을 찾을 수 있습니다. 상속받은 `LD_LIBRARY_PATH`는 절대 복사하지 않습니다. 자식 프로세스에는 부모 측 30초 제한과 내부 20초 제한이 있으며, 타임라인에 요청할 수 있는 총 대기 시간은 5초, 캡처할 수 있는 동작은 256개입니다. 네이티브 의존성이 멈추면 부모의 시간 제한으로 종료합니다.

pytest 플러그인은 자동 설치됩니다. 테스트는 `ha_scenario_tests.schema.load`로 시나리오를 불러오고 `scenario_runner` fixture를 호출할 수 있습니다. JUnit은 pytest 자체에서 생성합니다. 일반 Python 코드에서도 `run_scenario`를 가져올 수 있습니다.
