# Dossier de validation

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

## 2026-10-15 : validation d’exécution Linux

L’[exécution GitHub Actions 38843681199](https://github.com/ha-homelab/ha-scenario-tests/actions/runs/38843681199) a réussi au commit `0ea7e5a5d24dc89ebe896b1a2387396b3fce18f4`, avec CPython 3.14.8 sous Ubuntu et Home Assistant épinglé à 2026.10.0. La commande complète `python3 -m pytest -q` a terminé avec **54 tests réussis en 21.42 s**, sans test ignoré. Cela comprend les sept tests d’exécution avec HA réel : quatre scénarios d’exemple, un cas d’attente volontairement incorrecte et d’action interdite, le rapport JSON de la CLI localisée et le contrat de transfert de rôle pour un projet en aval. Chaque test d’exécution démarre un nouveau worker contrôlé ; les assertions d’échec attendu sont testées comme des échecs, pas présentées comme des scénarios réussis.

Ruff, les contrôles des liens documentaires et SVG, les constructions source et wheel, la politique de publication des sources et la recherche de secrets dans tout l’historique ont également réussi dans cette exécution. Cela valide la distribution synthétique de services et le comportement des états sous la garde d’E/S Python documentée. Cela n’établit pas de bac à sable de sécurité du système d’exploitation, ne valide pas une exécution Docker et ne prouve pas le comportement d’appareils physiques.

## 2026-10-15 : contrôles de développement macOS

Les sources, l’admission stricte des entrées, la garde d’audit Python, les traductions de la CLI et la régénération SVG ont été vérifiées localement avec Python 3.14.7 sous macOS arm64. `python -m pytest -q -m 'not runtime'` a réussi **47 tests** ; cette commande exclut explicitement sept cas avec HA réel. `python -m ruff check src tests scripts` a réussi. Cela ne remplace pas la suite complète d’exécution.

Le véritable moteur Home Assistant 2026.10.0 a chargé `automation`, `blueprint` et `trace`, puis exécuté les scénarios de délai de présence et de dérogation manuelle avec les appels synthétiques attendus, les états finaux et sans E/S bloquées. Le processus Python local s’est ensuite terminé par une erreur de segmentation native lors de l’arrêt de l’interpréteur. Le runner parent traite correctement ce code non nul comme un échec d’exécution, même si un JSON réussi l’a précédé. **Aucun test d’exécution macOS entièrement réussi n’est revendiqué.**

La suite CI Linux complète est requise avant d’accepter une version. Exécutez `python -m pytest -q --junitxml=junit.xml` ; absence de HA, mauvaise version HA, expiration du délai enfant et sortie enfant non nulle provoquent des échecs, jamais des omissions silencieuses. L’exécution liée plus haut constitue la preuve Linux pour cette implémentation ; les changements ultérieurs exigent leur propre exécution réussie. Ce dossier ne revendique aucune exécution Docker ni validation d’appareil physique.

## Métadonnées d’amorçage contrôlées

Le worker fournit la valeur synthétique `synthetic` aux métadonnées processeur mises en cache de Python et désactive `socket.has_ipv6` avant d’importer HA. Cela empêche l’initialisation de la plateforme HA de lancer `uname -p` et évite le test de liaison IPv6 locale à l’import d’urllib3. Sous Linux, ifaddr est importé sous la garde avec `ctypes.CDLL(None)`, qui résout les symboles libc déjà chargés dans le processus ; cela évite le sous-processus `ldconfig` de recherche de bibliothèque. La recherche normale est immédiatement rétablie. La garde d’E/S n’a aucune exception d’autorisation pour ces opérations. Ces changements affectent uniquement les métadonnées et sondes de l’hôte ; les déclencheurs, conditions, temporisateurs, rechargements, scripts et distributions de services HA sont réels. Ils dépendent des versions et sont couverts par la suite d’exécution épinglée.

## Reproduire

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m pip install --no-deps .
.venv/bin/python -m ruff check src tests scripts
.venv/bin/python -m pytest -q --junitxml=junit.xml
.venv/bin/python scripts/render_diagrams.py
```

Aucun rapport ne prouve l’état réel d’un relais, la livraison radio, la précision de présence domestique ou les durées de production. La chronologie SVG montre des attentes synthétiques, pas des mesures de performance.

La suite d’exécution comprend aussi `tests/fixtures/role_transfer.json`, le contrat synthétique en aval : le rôle actuel s’éteint et la prise retirée du rôle reste allumée. Ce n’est pas un test de transfert physique de charge.
