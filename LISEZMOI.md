# AssurRisk — pipeline de traitement des sinistres et de la météo
Le projet nettoie les données d’assurance et prépare les tables dans PostgreSQL.
Il charge les données météo, les rattache aux villes et les croise avec les sinistres.
Prérequis : Python, PostgreSQL démarré, base `AssurRisk1` créée et dépendances `pandas` et `psycopg2` installées.
Depuis la racine du projet, lancez `python pipeline.py`, puis saisissez le mot de passe PostgreSQL demandé.
# Depot