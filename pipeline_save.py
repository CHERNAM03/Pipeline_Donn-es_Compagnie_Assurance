# Bibliothèques utilisées : connexion PostgreSQL, lecture/écriture des données,
# chronométrage des étapes et gestion des fichiers de sortie.
import psycopg2
from getpass import getpass
import json
import pandas as pd
import time
import io
import os

# Création du dossier de résultats s'il n'existe pas déjà.
os.makedirs("sorties", exist_ok=True)

# Définition des colonnes des deux rapports et initialisation des fichiers CSV avec leurs en-têtes.
colonnes_journal = ["fichier", "etape", "outil", "secondes"]
colonnes_controles = ["etape", "controle", "valeur"]

pd.DataFrame(columns=colonnes_journal).to_csv(
    "sorties/journal_pipeline.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)
pd.DataFrame(columns=colonnes_controles).to_csv(
    "sorties/controles.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)
controles = []

# Demande le mot de passe sans l'afficher dans le terminal.
mot_de_passe = getpass("Mot de passe PostgreSQL : ")

# Ouverture de la connexion à la base AssurRisk1 et création du curseur qui exécutera le SQL.
connexion = psycopg2.connect(
    host="localhost", 
    port=5432,
    dbname="AssurRisk1",
    user="postgres", 
    password=mot_de_passe)
connexion.autocommit = True
curseur = connexion.cursor()
print("connexion ouverte")

# Lecture de la réponse météo JSON déjà téléchargée et affiche quelques informations
# pour vérifier sa structure avant de la transformer.
meteo_brute = json.load(open("donnees/meteo_30_villes.json", encoding="utf-8"))
print(type(meteo_brute)) # une LISTE
print(len(meteo_brute)) # de combien d'objets ?
print(meteo_brute[0].keys())  # clés présentes dans le premier objet

# Transformation des données journalières de chaque ville en DataFrame et ajout
# des coordonnées à chaque ligne.
morceaux = []
for localisation in meteo_brute:
 tableau = pd.DataFrame(localisation["daily"])
 tableau["latitude"] = localisation["latitude"]
 tableau["longitude"] = localisation["longitude"]
 morceaux.append(tableau)
meteo = pd.concat(morceaux, ignore_index=True)
print(meteo.shape)


# Ces scripts SQL préparent la base : initialisation, nettoyage, puis création
# des tables qui recevront les données météo.
etapes_avant = [
 ("01_init.sql", "Reinitialiser la base"),
 ("02_clean.sql", "Construire la couche propre"),
 ("03_tables_meteo.sql", "Creer les tables qui attendent la meteo"),
]
journal = []

# Exécuter les étapes SQL préalables et mesurer la durée de chacune.
for fichier, libelle in etapes_avant:
    debut = time.time()
    with open("sql/" + fichier, encoding="utf-8") as fichier_sql:
        requete = fichier_sql.read()
    curseur.execute(requete)
    print(" [SQL]", libelle)
    duree = round(time.time() - debut, 1)
    journal.append([fichier, libelle, "SQL", duree])

    # Après le nettoyage, vérification du volume de la table des sinistres propres.
    if fichier == "02_clean.sql":
        curseur.execute("SELECT COUNT(*) FROM clean_fact_sinistre")
        nombre_sinistres = curseur.fetchone()[0]
        print(" contrôle : clean_fact_sinistre =", nombre_sinistres, "lignes")
        controles.append([
            fichier,
            "Nombre de lignes dans clean_fact_sinistre",
            nombre_sinistres
        ])

# Chargement en bloc des données météo en mémoire dans PostgreSQL.
# Cette étape doit suivre la création des tables et précéder le rattachement.
debut = time.time()
tampon = io.StringIO()
meteo.to_csv(tampon, index=False, header=False)
tampon.seek(0)
curseur.copy_expert(
    """
    COPY meteo_assurrisk (
        time, weather_code, temperature_2m_max, temperature_2m_min,
        precipitation_sum, wind_gusts_10m_max, latitude, longitude
    ) FROM STDIN WITH (FORMAT csv)
    """,
    tampon
)
print(" [PYTHON]", len(meteo), "lignes de météo chargées")

# Lecture du fichier  CSV de coordonnées, le convertir en flux CSV en mémoire,
# puis chargement des lignes dans la table PostgreSQL correspondante.
villes = pd.read_csv(
    "donnees/villes_coordonnees_meteo.csv",
    encoding="utf-8-sig"
)
tampon_villes = io.StringIO()
villes.to_csv(tampon_villes, index=False, header=False)
tampon_villes.seek(0)
curseur.copy_expert(
    """
    COPY villes_coordonnees_meteo (ville, latitude, longitude)
    FROM STDIN WITH (FORMAT csv)
    """,
    tampon_villes
)
print(" [PYTHON]", len(villes), "lignes de coordonnées chargées")

# Ajouter le chargement Python au journal avec sa durée.
journal.append(["chargement_meteo.py", "Charger les données météo et villes", "Python",
                round(time.time() - debut, 1)])

# Vérification et enregistrement du nombre de lignes réellement présentes dans chaque
# table après le chargement.
curseur.execute("SELECT COUNT(*) FROM meteo_assurrisk")
nombre_lignes_meteo = curseur.fetchone()[0]
print(" contrôle : meteo_assurrisk =", nombre_lignes_meteo, "lignes")
controles.append([
    "chargement_meteo.py",
    "Nombre de lignes dans meteo_assurrisk",
    nombre_lignes_meteo
])

curseur.execute("SELECT COUNT(*) FROM villes_coordonnees_meteo")
nombre_lignes_villes = curseur.fetchone()[0]
print(" contrôle : villes_coordonnees_meteo =", nombre_lignes_villes, "lignes")
controles.append([
    "chargement_meteo.py",
    "Nombre de lignes dans villes_coordonnees_meteo",
    nombre_lignes_villes
])

# Ces scripts utilisent les données chargées : rattachement météo aux villes,
# croisement avec les sinistres, puis contrôles SQL finaux.
etapes_apres = [
    ("04_rattachement.sql", "Rattacher la météo aux sinistres"),
    ("05_croisement.sql", "Croiser les sinistres et la météo"),
    ("06_controles.sql", "Contrôler le résultat"),
]

# Exécuter les traitements SQL finaux et ajout de leur durée au journal.
for fichier, libelle in etapes_apres:
    debut = time.time()
    with open("sql/" + fichier, encoding="utf-8") as fichier_sql:
        requete = fichier_sql.read()
    curseur.execute(requete)
    duree = round(time.time() - debut, 1)
    journal.append([fichier, libelle, "SQL", duree])
    print(" [SQL]", libelle, "-", duree, "s")

    # Contrôle le volume météo rattaché et le nombre de villes correspondantes.
    if fichier == "04_rattachement.sql":
        curseur.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT ville)
            FROM meteo_assurrisk_ville
            """
        )
        nombre_rattachements, nombre_villes_rattachees = curseur.fetchone()
        print(
            " contrôle : meteo_assurrisk_ville =",
            nombre_rattachements, "lignes et",
            nombre_villes_rattachees, "villes"
        )
        controles.extend([
            [fichier, "Nombre de lignes dans meteo_assurrisk_ville", nombre_rattachements],
            [fichier, "Nombre de villes rattachées", nombre_villes_rattachees],
        ])
    # Compte les sinistres croisés et sépare ceux avec ou sans météo.
    elif fichier == "05_croisement.sql":
        curseur.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE temperature_2m_max IS NOT NULL) AS avec_meteo,
                COUNT(*) FILTER (WHERE temperature_2m_max IS NULL) AS sans_meteo
            FROM fact_sinistre_meteo
            """
        )
        total, avec_meteo, sans_meteo = curseur.fetchone()
        print(
            " contrôle : fact_sinistre_meteo =",
            total, "lignes;", avec_meteo, "avec météo;",
            sans_meteo, "sans météo"
        )
        controles.extend([
            [fichier, "Nombre total de lignes dans fact_sinistre_meteo", total],
            [fichier, "Sinistres avec météo", avec_meteo],
            [fichier, "Sinistres sans météo", sans_meteo],
        ])
    # Récupèration les résultats de la requête de contrôle finale et les conserve.
    elif fichier == "06_controles.sql":
        resultats = curseur.fetchone()
        noms_controles = [colonne[0] for colonne in curseur.description]
        for nom, valeur in zip(noms_controles, resultats):
            print(" contrôle final :", nom, "=", valeur)
            controles.append([fichier, nom, valeur])

# Rédiger le journal des durées et l'ensemble des contrôles dans le dossier sorties.
suivi = pd.DataFrame(journal, columns=["fichier", "etape", "outil", "secondes"])
suivi.to_csv("sorties/journal_pipeline.csv", sep=";", decimal=",", index=False, encoding="utf-8-sig")
pd.DataFrame(controles, columns=colonnes_controles).to_csv(
    "sorties/controles.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)
