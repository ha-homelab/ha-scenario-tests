# Dépannage

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

- Code de sortie 2 pendant l’installation ou l’exécution : vérifiez Python 3.14.2–3.14.x, la version HA épinglée exacte et un environnement virtuel vierge. Le runner rejette les autres versions de HA. Réinstallez les dépendances verrouillées avant de signaler un échec.
- Échec ou expiration du worker : l’import d’une dépendance ou l’initialisation de HA a échoué. Exécutez directement le worker isolé avec un fichier **synthétique** pour obtenir une trace locale : `python -I -m ha_scenario_tests.worker < examples/presence_timeout.json`. Ne publiez pas de diagnostics d’environnement non examinés.
- `calls_mismatch` : comparez l’ordre et les appels en double, pas seulement l’état final. Les états du seed sont définis avant le démarrage ; ils ne comptent pas automatiquement comme un nouveau déclencheur d’état après le démarrage.
- `forbidden_call` : une commande enregistrée d’actionneur synthétique correspond au contrat négatif. Il s’agit d’une véritable distribution d’automatisation, pas d’une action physique.
- `states_mismatch` : une affectation dans la chronologie ou un actionneur synthétique a laissé un état différent.
- `blocked_io` ou `background_exception` : ne désactivez jamais la garde pour obtenir un résultat vert. Cette version n’admet aucune intégration réseau. Signalez la reproduction synthétique et la version.
- Tests de temporisateurs instables : augmentez l’écart entre une transition d’état et l’échéance vérifiée. L’ordonnancement réel de la boucle d’événements est mesuré ; aucune horloge virtuelle ni précision à la microseconde n’est promise.
- Rechargement : les temporisateurs `for` peuvent être annulés par le véritable rechargement. Une automatisation explicite de réconciliation est nécessaire si la politique exige une récupération ; comparez `reload_reconcile.json`.
- Rapport existant : `--report` refuse volontairement de l’écraser. Choisissez un nouveau chemin.

Si vous utilisez l’arbre source après une installation non modifiable, réinstallez le paquet avant de tester vos changements. Pour le développement, installez avec `--no-deps -e .`.
