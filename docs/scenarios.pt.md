# Contrato de cenário v1

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

O validador de referência é `src/ha_scenario_tests/schema.py`. Apenas JSON, no máximo 64 KiB. São rejeitadas chaves desconhecidas ou duplicadas, entrada por ligação simbólica, números não finitos e tipos inválidos. Não copie configuração doméstica para exemplos públicos.

Campos obrigatórios na raiz: `schema: "ha-scenario/v1"`, um `name` curto em minúsculas, `seed`, `automations`, `timeline`, `expect`. O campo opcional `settle_seconds` tem o valor predefinido 0.1. Todos os ID de entidade usam o prefixo `scenario_` e têm de estar declarados no seed. Domínios suportados: `light`, `switch`, `input_boolean`, `binary_sensor`. Estados suportados: `on`, `off`, `unknown`, `unavailable`.

Uma automação tem `id`, `triggers`, `actions` e, opcionalmente, `conditions` e `mode` (`single` ou `restart`). Os triggers de estado exigem `trigger`, `entity_id`, `to`; `from` e `for_seconds` são opcionais. Os triggers de eventos usam `trigger: "event"` e `event_type: "scenario_name"`; também é suportado `automation_reloaded`. As condições são apenas comparações de estado. As ações contêm `action` e um único `entity_id`: `turn_on`, `turn_off`, `toggle` em entidades light/switch/input_boolean definidas no seed. Não são admitidos modelos, seletores, ações de dispositivos, blueprints, scripts do disco ou dados de serviço.

Os passos da cronologia contêm `after` (segundos relativos desde a conclusão do passo anterior) e exatamente uma operação:

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Outras operações: `"event": "scenario_manual_off"` ou `"reload": true`. O recarregamento chama o serviço real de automações do HA, que lê o `configuration.yaml` temporário gerado; o teste não imita o recarregamento ao emitir o seu evento de conclusão.

`expect.calls` é a lista ordenada exata de registos `{action, entity_id}`, incluindo repetições; uma lista vazia proíbe todas as chamadas a atuadores. `expect.forbidden` enumera opcionalmente chamadas que nunca podem ocorrer. `expect.states` associa os ID do seed aos estados finais. Chamadas inesperadas fazem falhar o teste mesmo que o estado final coincida por acaso.

Limites: 64 entidades no seed, 16 automações, 8 triggers e 8 condições por automação, 16 ações por automação, 32 passos na cronologia, 5 segundos totais de esperas solicitadas e 256 chamadas capturadas. Erros de tarefas em segundo plano e E/S bloqueada fazem falhar a execução. O relatório inclui os tempos monótonos decorridos das chamadas e passos, os componentes carregados, os estados finais e os códigos de falha.

O pai valida o relatório completo do worker antes de o devolver. `passed` tem de ser um valor de tipo booleano, `physical_validation` tem de ser false, e esquema, versão HA, nome do cenário, campos e limites têm de corresponder ao protocolo. O pai também verifica as asserções de chamadas e estados contra o cenário em vez de confiar num indicador de sucesso. Saída inválida e qualquer código de saída não nulo do worker são erros de execução, mesmo que o filho imprima um objeto JSON com aspeto de sucesso.

O exemplo stale fornecido representa perda de transporte por `unavailable`. Não infere a atualidade da origem a partir de `last_changed`, não testa a análise de marcas temporais do sensor nem comprova a expiração real de sensores. A substituição manual é uma política sintética explícita; a ferramenta não acrescenta essa política a uma automação existente.
