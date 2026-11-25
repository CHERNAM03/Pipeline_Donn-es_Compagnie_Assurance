# Synthèse du pipeline AssurRisk

Ce document décrit le fonctionnement de `pipeline.py` pour une personne qui
n'a pas suivi les étapes de création. Le pipeline se lance depuis le dossier
`demarrage` avec `python pipeline.py`. Il lit un fichier JSON météo déjà
présent sur le disque; dans sa version actuelle, il n'appelle pas directement
l'API.

## Préparation des fichiers de sortie

- **Fait :** crée le dossier `sorties` s'il n'existe pas et prépare les deux rapports CSV avec leurs en-têtes.
- **Produit :** `sorties/journal_pipeline.csv` et `sorties/controles.csv`.
- **Contrôle :** la présence du dossier et des en-têtes permet d'avoir les emplacements des rapports prêts dès le début.
- **En cas d'échec :** une erreur de fichier ou de droits d'écriture apparaît dans le terminal; le pipeline s'arrête avant la connexion à la base.

## Connexion à PostgreSQL

- **Fait :** demande le mot de passe, se connecte à la base `AssurRisk1` et crée un curseur pour exécuter des commandes SQL.
- **Produit :** une connexion active et un curseur utilisable par le script.
- **Contrôle :** le message `connexion ouverte` s'affiche après la connexion réussie.
- **En cas d'échec :** PostgreSQL ou `psycopg2` affiche une erreur dans le terminal, par exemple si la base, le serveur ou le mot de passe est incorrect.

## Lecture et préparation des données météo

- **Fait :** lit `donnees/meteo_30_villes.json`, transforme les données journalières de chaque ville en DataFrame et rassemble les tableaux.
- **Produit :** le DataFrame `meteo`, qui contient les observations météo et leurs coordonnées; le résultat attendu est de 21 930 lignes et 8 colonnes.
- **Contrôle :** le script affiche le type, le nombre de villes, les clés du premier objet JSON et la forme de `meteo`.
- **En cas d'échec :** fichier absent, JSON invalide ou clés inattendues provoquent une exception visible dans le terminal; les étapes SQL ne sont alors pas exécutées.

## Étape SQL 01 — `01_init.sql`

- **Fait :** initialise les tables sources de la base AssurRisk.
- **Produit :** les tables brutes des assurés, agences, contrats, garanties, sinistres et indemnisations.
- **Contrôle :** le message de l'étape apparaît et sa durée est ajoutée au journal en mémoire.
- **En cas d'échec :** l'erreur PostgreSQL s'affiche dans le terminal; le script s'arrête et les étapes suivantes ne sont pas exécutées.

## Étape SQL 02 — `02_clean.sql`

- **Fait :** crée les tables `clean_*` en nettoyant et en sélectionnant les données utiles des tables sources.
- **Produit :** les tables propres de reporting, notamment `clean_fact_sinistre`.
- **Contrôle :** le pipeline compte et affiche les lignes de `clean_fact_sinistre`, puis ajoute ce résultat à `controles.csv`.
- **En cas d'échec :** PostgreSQL signale l'erreur et le pipeline s'arrête; si le nombre de lignes est inattendu, le contrôle permet de repérer le problème après le nettoyage.

## Étape SQL 03 — `03_tables_meteo.sql`

- **Fait :** crée les tables vides destinées à recevoir les observations météo et les coordonnées des villes.
- **Produit :** `meteo_assurrisk` et `villes_coordonnees_meteo`, prêtes à être chargées.
- **Contrôle :** la prochaine étape Python vérifie les nombres de lignes effectivement chargées dans ces tables.
- **En cas d'échec :** PostgreSQL affiche l'erreur; le chargement Python ou les étapes SQL qui suivent ne peuvent pas aboutir.

## Étape Python — chargement météo et coordonnées

- **Fait :** sérialise le DataFrame météo et le CSV des villes en flux CSV en mémoire, puis les importe avec la commande PostgreSQL `COPY`.
- **Produit :** les observations dans `meteo_assurrisk` et les 31 lignes du fichier dans `villes_coordonnees_meteo` (dont la ligne `inconnu`, sans coordonnées).
- **Contrôle :** affiche les nombres de lignes chargées, puis compte les lignes présentes dans chacune des deux tables et enregistre ces comptes.
- **En cas d'échec :** une erreur de lecture, de format ou de `COPY` apparaît dans le terminal; le rattachement et le croisement ne sont pas lancés.

## Étape SQL 04 — `04_rattachement.sql`

- **Fait :** associe chaque point météo à la ville de coordonnées la plus proche; les villes sans coordonnées ne peuvent pas participer au calcul.
- **Produit :** la table `meteo_assurrisk_ville`, contenant les observations météo avec leur ville attribuée.
- **Contrôle :** le pipeline compte les lignes de cette table et le nombre de villes distinctes, puis ajoute ces résultats à `controles.csv`.
- **En cas d'échec :** l'erreur SQL est affichée et le script s'arrête; un résultat vide ou un nombre de villes inattendu indique un problème de données ou de rattachement.

## Étape SQL 05 — `05_croisement.sql`

- **Fait :** joint chaque sinistre propre à la météo correspondante selon la ville et la date de survenance; la jointure conserve aussi les sinistres sans météo.
- **Produit :** la table finale `fact_sinistre_meteo`.
- **Contrôle :** le pipeline compte les lignes totales, celles avec météo et celles sans météo, puis enregistre les résultats.
- **En cas d'échec :** une erreur SQL arrête le pipeline; un nombre de lignes différent du nombre de sinistres propres ou des sinistres sans météo révèle un problème à investiguer.

## Étape SQL 06 — `06_controles.sql`

- **Fait :** calcule un bilan global des sinistres propres, des données météo, du résultat final, des lignes sans météo et des doublons météo.
- **Produit :** une ligne de résultats contenant les indicateurs finaux.
- **Contrôle :** le pipeline affiche chaque indicateur et l'ajoute à `controles.csv`.
- **En cas d'échec :** l'erreur SQL ou l'absence de résultat est visible dans le terminal; les indicateurs permettent de localiser les écarts, sans corriger automatiquement les données.

## Écriture des rapports

- **Fait :** écrit les durées des étapes et les résultats des contrôles accumulés pendant l'exécution.
- **Produit :** les fichiers `sorties/journal_pipeline.csv` et `sorties/controles.csv`, ouvrables dans un tableur.
- **Contrôle :** vérifier que les deux fichiers contiennent leurs en-têtes et les lignes correspondant aux étapes exécutées.
- **En cas d'échec :** une erreur d'écriture apparaît dans le terminal; si une étape précédente a interrompu le script, les CSV peuvent ne contenir que leurs en-têtes initiaux.
