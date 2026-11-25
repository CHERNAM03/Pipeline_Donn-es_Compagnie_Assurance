# AssurRisk — pipeline de traitement

Ce projet initialise une base PostgreSQL, nettoie les données AssurRisk, charge
les données météo et les coordonnées des villes, puis rattache la météo aux
sinistres. Il produit également un journal d'exécution et un fichier de contrôles.

## Contenu du projet

- `pipeline.py` : orchestre les étapes Python et SQL.
- `sql/01_ini.sql` : initialise les tables et les données sources.
- `sql/02_clean.sql` : crée les tables nettoyées `clean_*`.
- `sql/03_tables_meteo.sql` : crée les tables destinées aux données météo.
- `sql/04_rattachement.sql` : associe les observations météo aux villes.
- `sql/05_croisement.sql` : croise les sinistres nettoyés avec la météo.
- `sql/06_controles.sql` : calcule les indicateurs finaux.
- `donnees/meteo_30_villes.json` : données météo utilisées par le pipeline.
- `donnees/villes_coordonnees_meteo.csv` : coordonnées de référence des villes.
- `sorties/` : rapports générés par le pipeline.

## Prérequis

- Python installé.
- PostgreSQL installé et démarré.
- Une base PostgreSQL nommée `AssurRisk1`.
- Les bibliothèques Python `pandas` et `psycopg2`.

Installation des bibliothèques si elles ne sont pas déjà installées :

```powershell
python -m pip install pandas psycopg2-binary
```

Le compte `postgres` utilisé dans `pipeline.py` doit pouvoir se connecter à la
base. Le mot de passe est demandé au lancement et n'est pas affiché.

## Lancer le pipeline

Dans PowerShell, placez-vous à la racine du dossier du projet — le dossier qui
contient `pipeline.py` — puis lancez :

```powershell
python pipeline.py
```

Le script lit le JSON météo local, prépare un tableau, puis exécute les étapes
dans cet ordre :

1. Initialisation de la base (`01_ini.sql`).
2. Nettoyage des données (`02_clean.sql`).
3. Création des tables météo (`03_tables_meteo.sql`).
4. Chargement du tableau météo et du CSV des villes dans PostgreSQL.
5. Rattachement des observations aux villes (`04_rattachement.sql`).
6. Croisement avec les sinistres (`05_croisement.sql`).
7. Contrôles finaux (`06_controles.sql`).

## Attention — réinitialisation de la base

`01_ini.sql` supprime puis recrée les tables sources et réinitialise leurs
données. Chaque exécution complète du pipeline reconstruit donc les tables et
peut remplacer les données présentes dans `AssurRisk1`. Vérifiez la base ciblée
avant de lancer le script.

La base elle-même doit déjà exister. Si elle n'existe pas, créez `AssurRisk1`
dans PostgreSQL avant de lancer le pipeline.

## Résultats et vérifications

Les résultats sont écrits dans `sorties/` :

- `journal_pipeline.csv` : fichier SQL ou étape, libellé, outil utilisé et durée.
- `controles.csv` : volumes et résultats des contrôles intermédiaires et finaux.

Les volumes obtenus peuvent varier si les fichiers d'entrée ou les scripts SQL
changent. À titre de repères pour les données actuellement utilisées, les
contrôles précédents ont affiché 12 098 sinistres nettoyés et finaux,
21 930 lignes météo, 31 lignes de coordonnées (dont `inconnu`, sans coordonnées),
30 villes météo rattachées, aucun sinistre sans météo et aucun doublon météo.

## Données météo

La version actuelle utilise le fichier JSON météo déjà présent dans
`donnees/`. Elle ne fait pas elle-même de requête à l'API météo.

## GitHub

Avant de publier le projet, vérifiez que les fichiers ne contiennent aucun mot
de passe, jeton ou autre secret. Le mot de passe PostgreSQL doit rester privé;
ne le placez jamais dans le dépôt.
