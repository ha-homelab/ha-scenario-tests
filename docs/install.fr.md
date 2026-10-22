# Installation et confinement

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

Utilisez l’environnement Home Assistant épinglé avec Python 3.14.2–3.14.x. Installez `requirements.lock` avec `--require-hashes`, puis ce paquet avec `--no-deps .`, comme indiqué dans le README racine. Le fichier de verrouillage couvre les dépendances de l’application et des tests. Un environnement vierge est requis ; n’installez rien dans votre environnement Home Assistant de production. Pour modifier le code source, utilisez plutôt `pip install --no-deps -e .`.

Exécutez d’abord `ha-scenario validate examples/stale_sensor.json`. La validation n’importe pas l’environnement HA. Exécutez ensuite `ha-scenario run examples/stale_sensor.json --report result.json`. Aucun serveur cible n’est configuré. L’unique chemin de sortie provient de votre argument explicite `--report`, pas du scénario.

Pour renforcer la séparation réseau :

```sh
docker build -t ha-scenario-tests .
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m ha-scenario-tests
```

La construction nécessite Internet pour les dépendances. L’exécution n’a pas de réseau et dispose d’un `/tmp` inscriptible jetable ; elle ne monte ni configuration du domicile, ni socket Docker, ni identifiants. C’est une recette de déploiement facultative ; consultez le dossier de validation pour savoir si ce conteneur précis a été exécuté. N’ajoutez ni réseau hôte ni montages de production.

L’interface de sous-processus supprime les identifiants hérités et `PYTHONPATH`. Le worker avec `-I` utilise le paquet installé. Seuls PATH, SYSTEMROOT et LANG sont hérités ; la graine de hachage est fixe. Sous Linux, le chemin de bibliothèque du worker est dérivé du `LIBDIR` de l’installation Python active, ce qui permet aux distributions Python déplaçables de trouver libpython. Une valeur héritée de `LD_LIBRARY_PATH` n’est jamais recopiée. Le processus enfant a un délai parental de 30 secondes, un délai interne de 20 secondes, au maximum 5 secondes d’attentes demandées dans la chronologie et 256 actions enregistrées. Le délai parental met fin aux blocages des dépendances natives.

Le plugin pytest s’installe automatiquement. Un test peut charger un scénario avec `ha_scenario_tests.schema.load` et appeler la fixture `scenario_runner`. pytest génère lui-même JUnit. `run_scenario` peut aussi être importé dans du Python ordinaire.
