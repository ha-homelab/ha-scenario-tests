# Contrat de scénario v1

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

Le validateur de référence est `src/ha_scenario_tests/schema.py`. JSON uniquement, au maximum 64 KiB. Les clés inconnues, clés JSON en double, entrées par lien symbolique, nombres non finis et types invalides sont rejetés. Ne copiez pas la configuration du domicile dans les exemples publics.

Champs racines requis : `schema: "ha-scenario/v1"`, un `name` court en minuscules, `seed`, `automations`, `timeline`, `expect`. Le champ facultatif `settle_seconds` vaut 0.1 par défaut. Tous les identifiants d’entité utilisent le préfixe `scenario_` et doivent être déclarés dans le seed. Domaines pris en charge : `light`, `switch`, `input_boolean`, `binary_sensor`. États pris en charge : `on`, `off`, `unknown`, `unavailable`.

Une automatisation possède `id`, `triggers`, `actions`, éventuellement `conditions` et `mode` (`single` ou `restart`). Les déclencheurs d’état nécessitent `trigger`, `entity_id`, `to` ; `from` et `for_seconds` sont facultatifs. Les déclencheurs d’événement utilisent `trigger: "event"` et `event_type: "scenario_name"` ; `automation_reloaded` est également pris en charge. Les conditions se limitent à des comparaisons d’états. Les actions contiennent `action` et un seul `entity_id` : `turn_on`, `turn_off`, `toggle` sur des entités light/switch/input_boolean initialisées dans le seed. Aucun modèle, sélecteur, action d’appareil, blueprint, script sur disque ou donnée de service n’est admis.

Les étapes de chronologie contiennent `after` (secondes relatives depuis la fin de l’étape précédente) et exactement une opération :

```json
{"after": 0.04, "set": {"entity_id": "binary_sensor.scenario_presence", "state": "on"}}
```

Autres opérations : `"event": "scenario_manual_off"` ou `"reload": true`. Le rechargement appelle le véritable service d’automatisation de HA, qui lit le `configuration.yaml` temporaire généré ; le test ne simule pas le rechargement en déclenchant son événement de fin.

`expect.calls` est la liste ordonnée exacte des enregistrements `{action, entity_id}`, répétitions comprises ; une liste vide interdit tous les appels d’actionneur. `expect.forbidden` énumère éventuellement les appels qui ne doivent jamais survenir. `expect.states` associe les identifiants du seed à leurs états finaux. Des appels inattendus font échouer le test même si l’état final correspond par hasard.

Limites : 64 entités dans le seed, 16 automatisations, 8 déclencheurs et 8 conditions par automatisation, 16 actions par automatisation, 32 étapes de chronologie, 5 secondes d’attente demandée au total, 256 appels enregistrés. Les erreurs des tâches d’arrière-plan et les E/S bloquées font échouer l’exécution. Le rapport comprend les durées monotones écoulées des appels et étapes, les composants chargés, les états finaux et les codes d’échec.

Le parent valide le rapport complet du worker avant de le renvoyer. `passed` doit être un véritable booléen, `physical_validation` doit être false, et le schéma, la version HA, le nom du scénario, les champs et les bornes doivent correspondre au protocole. Le parent vérifie aussi les assertions d’appels et d’états par rapport au scénario au lieu de se fier à un indicateur de réussite. Une sortie invalide et tout code de sortie non nul du worker constituent des erreurs d’exécution, même si l’enfant a affiché un objet JSON semblant indiquer une réussite.

L’exemple stale fourni représente une perte de transport par `unavailable`. Il ne déduit pas la fraîcheur de la source depuis `last_changed`, ne teste pas l’analyse des horodatages des capteurs et ne prouve pas l’expiration d’un capteur réel. La dérogation manuelle est une politique synthétique explicite ; l’outil n’ajoute pas cette politique à une automatisation existante.
