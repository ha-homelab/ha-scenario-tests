# Âmbito e evidências

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

Esta versão valida um subconjunto limitado com triggers, condições, temporizadores, recarregamento e despacho de ações de scripts reais do Home Assistant. Os recetores dos comandos dos atuadores e os estados de entrada são sintéticos. Não comprova protocolos físicos de comunicação, consumo de corrente, precisão dos sensores, estado físico de um relé, segurança ou comportamento de todas as configurações possíveis de HA.

O relógio mede tempo monótono real decorrido. Os testes usam deliberadamente intervalos curtos e margem de escalonamento. Não alteramos os métodos internos de atraso do HA, não reescrevemos durações de temporizadores de produção nem afirmamos equivalência com tempo virtual. Mudanças de hora, agendamento por relógio civil, reinício completo do processo HA e persistência do Recorder estão fora da v1. O recarregamento é testado; não é um reinício de processo.

A entrada não contém modelos executáveis nem configuração de integrações. Cada worker usa uma diretoria temporária limpa, um ambiente depurado e uma proteção global de auditoria. Isto evita E/S acidental de rede ou subprocessos Python pelo caminho admitido. Não é uma sandbox para código hostil: confia-se nas dependências Python e nativas, no interpretador e no host. Execute fontes ou dependências não fiáveis apenas num ambiente protegido separado. A receita Docker opcional sem rede reforça o isolamento de rede, mas não comprova o comportamento do hardware.

Os relatórios públicos devem conter apenas fixtures sintéticas. Cronologias de estados reais revelam ocupação e hábitos mesmo sem token. Aqui não estão incluídos inventários domésticos, gravações ou configuração de produção. Todos os diagramas são identificados como sintéticos e reproduzíveis com `python scripts/render_diagrams.py`.

Consulte a [validação](validation.md) para conhecer as verificações medidas realizadas nesta versão. O suporte de instalação limita-se aos ambientes desse registo; a receita do contentor não afirma que todas as plataformas foram testadas.
