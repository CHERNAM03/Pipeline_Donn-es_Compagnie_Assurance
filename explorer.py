import pandas as pd
import psycopg2
import warnings
import getpass

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

mot_de_passe = getpass.getpass("Mot de passe PostgreSQL : ")
connexion = psycopg2.connect(host="localhost", port=5432, dbname="AssurRisk1",
 user="postgres", password=mot_de_passe)
df = pd.read_sql("SELECT * FROM fact_sinistre_meteo", connexion)
print("Données chargées :", df.shape)
df["montant_estime"] = df["montant_estime"].astype(float)
df["franchise"] = df["franchise"].astype(float)
df["date_survenance"] = pd.to_datetime(df["date_survenance"])
df["date_declaration"] = pd.to_datetime(df["date_declaration"])


# EXERCICE 1

# 1. Combien de lignes et combien de colonnes compte la table ?
print(df.shape)
# [12098 rows x 18 columns]>
# 2. Y a-t-il des valeurs manquantes ? Si oui, dans quelles colonnes ?
print(df.isna().sum())

# On n'a pas de valeurs manquantes, on a false = 0 partout

# 3. Quel est le montant le plus faible de la table, et le plus élevé ?
print(df["montant_estime"].describe())

# le montant le plus faible est   80
# le montant le plus élévé est de 49912.
# 
# 4. Combien de types de sinistre différents y a-t-il ?*
print(df["type_sinistre"].value_counts().count())

#### ON a 8 types de sinistres

# 5. Quelle est la moyenne et la médiane de la colonne franchise ?

print(df["franchise"].agg(["mean", "median"]))

## mean      228.703091
## median    200.000000

# la moyenne est tres sensible aux valeurs extremes


print(df.groupby("type_sinistre")["franchise"].agg(["mean", "median"]))

#                              mean  median
# type_sinistre                            
# Bris de glace           81.355932    80.0
# Dégât des eaux         299.262621   300.0
# Grêle                  200.000000   200.0
# Incendie               496.052632   500.0
# Inondation             500.000000   500.0
# Responsabilité civile    0.000000     0.0
# Tempête                298.296199   300.0
# Vol                    150.378251   150.0


print(df.groupby("type_sinistre")["montant_estime"].agg(["mean", "median"]))

#                                mean   median
# type_sinistre                               
# Bris de glace            677.911017    671.5
# Dégât des eaux          4478.319909   4464.5
# Grêle                   3333.384950   3255.0
# Incendie               27548.103618  26957.0
# Inondation             18111.012500  18306.5
# Responsabilité civile   2597.454950   2543.0
# Tempête                11477.944954  11288.5
# Vol                     7688.765957   7611.0


#### La franchise ressemble à un barème fixe : ses valeurs sont souvent standardisées
#### (la médiane générale était de 200 €). Le montant estimé ressemble davantage à 
#### de vrais montants de sinistres, car il varie selon le sinistre et le type de dommage.

# Fréquence de chaque type sur l'ensemble du tableau (en pourcentage).
print("\nRépartition globale par type (%) :")
print(df["type_sinistre"].value_counts(normalize=True).mul(100).round(1))

# 2. Ce que je propose
# Je pense que le dégât des eaux est le type le plus fréquent dans chacune des 30 villes,
#  et pas seulement dans le total de la table.

comptes = pd.crosstab(df["ville_sinistre"], df["type_sinistre"])
de = comptes["Dégât des eaux"]
meilleur_autre = comptes.drop(columns="Dégât des eaux").max(axis=1)

# Comparer les nombres et les parts par ville, sans masquer les égalités.
rapport_villes = pd.DataFrame({
    "sinistres": comptes.sum(axis=1),
    "dégâts des eaux": de,
    "part dégâts des eaux (%)": (
        de / comptes.sum(axis=1) * 100
    ).round(1),
    "meilleur autre type": comptes.drop(columns="Dégât des eaux").idxmax(axis=1),
    "nombre meilleur autre type": meilleur_autre,
    "avance": de - meilleur_autre,
})
print("\nClassement des types par ville :")
print(rapport_villes.to_string())
print(
    "\nDégât des eaux seul premier :",
    int((de > meilleur_autre).sum()), "sur", len(comptes), "villes"
)
print("Égalité en tête :", int((de == meilleur_autre).sum()), "villes")
print("Un autre type est devant :", int((de < meilleur_autre).sum()), "villes")

# Variation de la part des dégâts des eaux d'une ville à l'autre.
part = (
    df.groupby("ville_sinistre")["type_sinistre"]
    .apply(lambda s: s.value_counts(normalize=True).mul(100).round(1))
)
print("\nStatistiques de la part des dégâts des eaux par ville :")
print(part.xs("Dégât des eaux", level=1).describe())

# EXERCICE 2 — Pic de sinistres en octobre 2025
debut_octobre = pd.Timestamp("2025-10-01")
debut_novembre = pd.Timestamp("2025-11-01")
est_en_octobre = (
    (df["date_survenance"] >= debut_octobre) &
    (df["date_survenance"] < debut_novembre)
)
octobre = df.loc[est_en_octobre]
reste = df.loc[~est_en_octobre]

# Comparer octobre au reste de la période et vérifier la couverture des données.
print("Sinistres en octobre :", len(octobre))
print("Sinistres hors octobre :", len(reste))
print(
    "Période couverte :",
    df["date_survenance"].min().date(),
    "à",
    df["date_survenance"].max().date()
)

# Reconstituer chaque jour entre les premières et dernières dates du jeu.
# Cela compte aussi les jours sans sinistre, sous l'hypothèse que la période
# de collecte est continue entre ces deux dates.
date_min = df["date_survenance"].min().normalize()
date_max = df["date_survenance"].max().normalize()
calendrier = pd.date_range(date_min, date_max, freq="D")
sinistres_par_jour = (
    df.groupby(df["date_survenance"].dt.normalize()).size()
    .reindex(calendrier, fill_value=0)
)

# Nombre de sinistres et moyenne quotidienne pour chaque mois couvert.
mensuel = sinistres_par_jour.rename("sinistres").to_frame()
mensuel["mois"] = mensuel.index.to_period("M")
mensuel = mensuel.groupby("mois").agg(
    sinistres=("sinistres", "sum"),
    jours_observes=("sinistres", "count")
)
mensuel["moyenne par jour observé"] = (
    mensuel["sinistres"] / mensuel["jours_observes"]
).round(1)

print("\nMois classés par moyenne quotidienne :")
print(
    mensuel.sort_values(
        "moyenne par jour observé",
        ascending=False
    ).to_string()
)

# Répartition quotidienne des sinistres en octobre, jours sans sinistre inclus.
par_jour = sinistres_par_jour.loc[
    (sinistres_par_jour.index >= debut_octobre) &
    (sinistres_par_jour.index < debut_novembre)
]
print("\nNombre de sinistres par jour en octobre :")
print(par_jour.describe())

# Comparer le nombre et la part de chaque type en octobre et hors octobre.
par_type = pd.DataFrame({
    "Octobre (nombre)": octobre["type_sinistre"].value_counts(),
    "Octobre (%)": octobre["type_sinistre"].value_counts(
        normalize=True
    ).mul(100),
    "Reste (nombre)": reste["type_sinistre"].value_counts(),
    "Reste (%)": reste["type_sinistre"].value_counts(
        normalize=True
    ).mul(100),
}).fillna(0).round(1)

print("\nRépartition par type :")
print(par_type.sort_values("Octobre (nombre)", ascending=False).to_string())

# Comparer la répartition des sinistres par région entre les deux périodes.
comparaison = pd.DataFrame({
    "Octobre (%)": octobre["region_sinistre"].value_counts(normalize=True) * 100,
    "Reste (%)": reste["region_sinistre"].value_counts(normalize=True) * 100
}).fillna(0)
comparaison["Écart (points)"] = (
    comparaison["Octobre (%)"] - comparaison["Reste (%)"]
)
print("\nRépartition par région (octobre et reste) :")
print(comparaison.round(1).sort_values("Écart (points)", ascending=False))

# Examiner les précipitations et sinistres pour chaque couple ville-date
# d'octobre présent dans les données de sinistres.
par_ville_date = octobre.groupby(
    ["date_survenance", "ville_sinistre"]
).agg(
    sinistres=("sinistre_id", "count"),
    pluie_mm=("precipitation_sum", "first")
)
print("\nCouples ville-date d'octobre triés par précipitations :")
print(par_ville_date.sort_values("pluie_mm", ascending=False).to_string())

# Calcul des coeifficients de corrélations

# Compter les sinistres par ville et par jour
comptes = octobre.groupby(["date_survenance", "ville_sinistre"]).agg(
    total=("sinistre_id", "count"),
    eaux=("type_sinistre", lambda s: (s == "Dégât des eaux").sum()),
    tempetes=("type_sinistre", lambda s: (s == "Tempête").sum())
).reset_index()

# Récupérer la météo d'octobre
meteo = pd.read_sql_query("""
    SELECT time, ville, precipitation_sum, wind_gusts_10m_max
    FROM meteo_assurrisk_ville
    WHERE time >= '2025-10-01' AND time < '2025-10-29'
""", connexion)
meteo["time"] = pd.to_datetime(meteo["time"])

# Associer météo et nombres de sinistres; les jours sans sinistre comptent comme zéro
corr = meteo.merge(
    comptes,
    left_on=["time", "ville"],
    right_on=["date_survenance", "ville_sinistre"],
    how="left"
)
corr[["total", "eaux", "tempetes"]] = corr[["total", "eaux", "tempetes"]].fillna(0)

print(corr["precipitation_sum"].corr(corr["total"]))
print(corr["precipitation_sum"].corr(corr["eaux"]))
print(corr["wind_gusts_10m_max"].corr(corr["tempetes"]))


# EXERCICE 2
# Analyse de la date de déclaration à partir du délai en jours.
print("\n1. Dimensions de la table :")
print(df.shape)

print("\n2. Aperçu des données :")
print(df.head())

print("\n3. Valeurs manquantes :")
print(df.isna().sum())

delai = (df["date_declaration"] - df["date_survenance"]).dt.days

print("\n4. Statistiques du délai de déclaration (jours) :")
print(delai.describe())

print("\n5. Nombre de sinistres par délai de déclaration (jours) :")
print(delai.value_counts().sort_index().to_string())

print("\n6. Délai de déclaration par type de sinistre (jours) :")
analyse_delai = df.assign(delai_jours=delai).groupby("type_sinistre").agg(
    nombre_dossiers=("delai_jours", "count"),
    delai_moyen=("delai_jours", "mean"),
    delai_median=("delai_jours", "median"),
)
print(analyse_delai.round(1).to_string())
delais_par_type = pd.crosstab(
    df["type_sinistre"],
    delai,
    normalize="index"
).mul(100).round(1)

print("\nRépartition des délais par type (%) :")
print(delais_par_type.to_string())

print("\nDéclarations avant la date du sinistre :", int((delai < 0).sum()))
print("Déclarations le jour même :", int((delai == 0).sum()))


# Je choisis une deuxième colonne : statut_sinistre.
# Pour refaire l’étape 3 (« ce que je devrais voir »), tu peux écrire :

print("\nNombre de dossiers par statut :")
print(df["statut_sinistre"].value_counts())

print("\nRépartition des statuts par type de sinistre (%) :")
statuts_par_type = pd.crosstab(
    df["type_sinistre"],
    df["statut_sinistre"],
    normalize="index"
).mul(100).round(1)

print(statuts_par_type.to_string())

connexion.close()
