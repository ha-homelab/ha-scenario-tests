# Resolução de problemas

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

- Saída 2 durante a instalação ou execução: verifique Python 3.14.2–3.14.x, a versão exata fixada de HA e um ambiente virtual limpo. O runner rejeita outras versões de HA. Reinstale as dependências bloqueadas antes de comunicar uma falha.
- Falha ou tempo esgotado do worker: falhou a importação de uma dependência ou a configuração de HA. Execute diretamente o worker isolado com um ficheiro **sintético** para obter uma trace local: `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Não publique diagnósticos do ambiente sem os rever.
- `calls_mismatch`: compare a ordem e as chamadas duplicadas, não apenas o estado final. Os estados do seed são definidos antes do arranque; não contam automaticamente como novo trigger de estado após o arranque.
- `forbidden_call`: um comando capturado de um atuador sintético correspondeu ao contrato negativo. Trata-se de despacho real de automação, não de atuação física.
- `states_mismatch`: uma atribuição na cronologia ou um atuador sintético deixou um estado diferente.
- `blocked_io` ou `background_exception`: nunca desligue a proteção para obter um resultado verde. Esta versão não admite integrações de rede. Comunique a reprodução sintética e a versão.
- Testes de temporizadores instáveis: aumente a separação entre a transição de estado e o prazo verificado. Mede-se o escalonamento real do ciclo de eventos; não é prometido um relógio virtual nem escalonamento exato ao microssegundo.
- Recarregamento: os temporizadores `for` podem ser cancelados pelo recarregamento real. É necessária uma automação explícita de reconciliação quando a política exige recuperação; compare `reload_reconcile.json`.
- Relatório existente: `--report` recusa deliberadamente sobrescrevê-lo. Escolha um caminho novo.

Se usar a árvore de código-fonte depois de uma instalação não editável, reinstale o pacote antes de testar alterações. Para desenvolvimento, instale com `--no-deps -e .`.
