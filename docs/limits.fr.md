# Périmètre et preuves

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

Cette version valide un sous-ensemble borné avec de véritables déclencheurs, conditions, temporisateurs, rechargements et distributions d’actions de scripts Home Assistant. Les récepteurs des commandes d’actionneurs et les états d’entrée sont synthétiques. Elle ne prouve ni les protocoles filaires, ni la consommation électrique, ni la précision des capteurs, ni l’état physique d’un relais, ni la sûreté, ni le comportement de toutes les configurations HA possibles.

L’horloge mesure le temps monotone réellement écoulé. Les tests utilisent volontairement des intervalles courts et une marge d’ordonnancement. Nous ne modifions pas les méthodes internes de délai de HA ni les durées des temporisateurs de production, et ne prétendons pas à une équivalence avec le temps virtuel. Les changements d’heure, la planification selon l’horloge civile, le redémarrage complet du processus HA et la persistance Recorder sont hors v1. Le rechargement est testé ; ce n’est pas un redémarrage du processus.

L’entrée ne contient ni modèles exécutables ni configuration d’intégration. Chaque worker utilise un répertoire temporaire vierge, un environnement épuré et une garde d’audit globale. Cela empêche les E/S réseau ou sous-processus Python accidentelles par le chemin admis. Ce n’est pas un bac à sable pour code hostile : les dépendances Python et natives, l’interpréteur et l’hôte sont considérés comme fiables. N’exécutez des sources ou dépendances non fiables que dans un environnement sécurisé distinct. La recette Docker facultative sans réseau renforce l’isolation réseau sans prouver le comportement matériel.

Les rapports publics doivent contenir uniquement des fixtures synthétiques. Des chronologies d’états réels révèlent présence et habitudes même sans jeton. Aucun inventaire domestique, enregistrement ou configuration de production n’est inclus ici. Tous les diagrammes sont marqués synthétiques et reproductibles avec `python scripts/render_diagrams.py`.

Consultez la [validation](validation.fr.md) pour les contrôles mesurés réalisés sur cette version. La prise en charge de l’installation se limite aux environnements de ce dossier ; la recette du conteneur ne signifie pas que toutes les plateformes ont été testées.
