# Instalação e contenção

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

Use o ambiente de execução Home Assistant fixado com Python 3.14.2–3.14.x. Instale `requirements.lock` com `--require-hashes` e depois este pacote com `--no-deps .`, como mostra o README principal. O ficheiro de bloqueio abrange as dependências da aplicação e dos testes. É necessário um ambiente limpo; não instale no seu ambiente Home Assistant de produção. Ao editar o código-fonte, use antes `pip install --no-deps -e .`.

Execute primeiro `ha-scenario validate examples/stale_sensor.json`. A validação não importa o ambiente HA. Depois execute `ha-scenario run examples/stale_sensor.json --report result.json`. Não é configurado nenhum servidor de destino. O único caminho de saída vem do seu argumento explícito `--report`, não do cenário.

Para reforçar a separação de rede:

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

A construção necessita de acesso à Internet para as dependências. A execução não tem rede e dispõe de um `/tmp` gravável descartável; não monta a configuração doméstica, o socket Docker ou credenciais. Esta receita de implementação é opcional; consulte o registo de validação para saber se este contentor exato foi executado. Não adicione rede do host nem montagens de produção.

A interface de subprocessos remove as credenciais herdadas e `PYTHONPATH`. O worker com `-I` usa o pacote instalado. Só PATH, SYSTEMROOT e LANG são herdados; a semente do hash é fixa. Em Linux, o caminho de bibliotecas do worker deriva do `LIBDIR` da instalação Python em execução, permitindo a versões relocáveis do Python encontrar libpython. Um `LD_LIBRARY_PATH` herdado nunca é copiado. O processo filho tem um limite de 30 segundos imposto pelo pai, um limite interno de 20 segundos, no máximo 5 segundos de esperas solicitadas na cronologia e 256 ações capturadas. O limite do pai termina bloqueios de dependências nativas.

O plugin pytest instala-se automaticamente. Um teste pode carregar um cenário com `ha_scenario_tests.schema.load` e chamar a fixture `scenario_runner`. O próprio pytest gera JUnit. `run_scenario` também pode ser importado em código Python normal.
