# Registo de validação

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

## 2026-10-15: validação de execução em Linux

A [execução GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) passou no commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, com CPython 3.14.8 em Ubuntu e Home Assistant fixado em 2026.10.0. O comando completo `python3 -m pytest -q` terminou com **54 testes aprovados em 21.42 s**, sem testes ignorados. Inclui os sete testes de execução com HA real: quatro cenários de exemplo, um caso com expectativa intencionalmente errada e ação proibida, o relatório JSON da CLI localizada e o contrato de transferência de papel de um projeto dependente. Cada teste inicia um worker controlado novo; as asserções de falha esperada são testadas como falhas, não apresentadas como cenários bem-sucedidos.

Também passaram Ruff, verificações de ligações da documentação e SVG, construções de fonte e wheel, a política de publicação de fontes e a pesquisa de segredos em todo o histórico. Isto valida o despacho sintético de serviços e o comportamento dos estados sob a proteção de E/S Python documentada. Não estabelece uma sandbox de segurança ao nível do sistema operativo, não valida a execução de Docker nem comprova o comportamento físico de dispositivos.

## 2026-10-15: verificações de desenvolvimento em macOS

O código-fonte, a admissão estrita de entradas, a proteção de auditoria Python, as traduções CLI e a regeneração SVG foram verificados localmente com Python 3.14.7 em macOS arm64. `python -m pytest -q -m 'not runtime'` aprovou **47 testes**; esse comando exclui explicitamente sete casos com HA real. `python -m ruff check src tests scripts` passou. Isto não substitui a suite completa de execução.

O motor real Home Assistant 2026.10.0 carregou `automation`, `blueprint` e `trace` e executou os cenários de tempo de presença e substituição manual com as chamadas sintéticas esperadas, estados finais e sem E/S bloqueada. O processo Python local terminou depois com uma falha de segmentação nativa durante o encerramento do interpretador. O runner pai trata corretamente esse código não nulo como falha de execução, mesmo quando precedido por um JSON bem-sucedido. **Não se afirma a aprovação de um teste completo de execução em macOS.**

A suite Linux CI completa é obrigatória antes de aceitar uma versão. Execute `python -m pytest -q --junitxml=junit.xml`: HA ausente, versões incorretas, tempos esgotados de filhos e saídas não nulas causam falhas, nunca omissões silenciosas. A execução ligada acima é a evidência Linux desta implementação; alterações posteriores exigem a sua própria execução aprovada. Não se afirma neste registo qualquer execução Docker ou validação de dispositivos físicos.

## Metadados de arranque controlados

O worker fornece o valor sintético `synthetic` aos metadados de processador em cache de Python e desativa `socket.has_ipv6` antes de importar HA. Isto impede a inicialização da plataforma HA de lançar `uname -p` e evita a tentativa de bind IPv6 local durante a importação de urllib3. Em Linux, ifaddr é importado sob proteção através de `ctypes.CDLL(None)`, resolvendo símbolos libc já carregados no processo; evita-se assim o subprocesso `ldconfig` da pesquisa de bibliotecas. A pesquisa normal é imediatamente restaurada. A proteção de E/S não tem exceções de autorização para estas operações. As alterações afetam apenas metadados e sondagens do host; triggers, condições, temporizadores, recarregamento, scripts e despacho de serviços HA são reais. São sensíveis às versões e cobertos pela suite de execução fixada.

## Reproduzir

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Nenhum relatório comprova o estado real do relé, a entrega por rádio, a precisão da presença doméstica ou a temporização com durações de produção. A cronologia SVG mostra expectativas sintéticas, não medições de desempenho.

A suite de execução também inclui `tests/fixtures/role_transfer.json`, o contrato sintético do projeto dependente: o papel atual desliga-se e a tomada retirada desse papel permanece ligada. Não é um teste de transferência física de carga.
