# Cahier de suivi — Projet AssurRisk

## Jour 1 — Lundi 9 : premières manipulations

### Exercice 1 — Remise en main

Le script contient une liste de quatre étapes et un dictionnaire de paires clé-valeur. Le premier élément de la liste, à l’index 0, est « Réinitialiser la base ».

Avec `append`, une nouvelle étape s’ajoute à la fin de la liste. Une paire ajoutée au dictionnaire apparaît dans la boucle qui parcourt ce dictionnaire.

Quelques erreurs rencontrées pendant les manipulations :

| Manipulation                                    | Erreur observée    |
|-------------------------------------------------|--------------------|
| Accéder à `etapes[12]`, qui n’existe pas        | `IndexError`       |
| Retirer `.items()` de la boucle du dictionnaire | `ValueError`       |
| Retirer l’indentation d’une ligne de boucle     | `IndentationError` |

**À quoi sert une boucle ?** Une boucle répète automatiquement des instructions pour chaque élément d’une liste ou d’une collection.

### Exercice 2 — L’inventaire, chronomètre en main

Travail effectué en binôme avec Raoul Zamble; le rendu a été écrit dans son cahier.

### Exercice 3 — Première connexion à la base

Le script s’est connecté à la base dans DBeaver et l’a réinitialisée. La requête `SELECT COUNT(*) FROM fact_sinistre` a renvoyé 12 490 lignes.

Sans `connexion.autocommit = True`, je n’ai pas remarqué de changement important, sauf une connexion à DBeaver plus lente. Les modifications ne sont toutefois pas validées tant que la transaction n’est pas commitée.

### Exercice 4 — Lire la structure des données météo

Le fichier météo contient une liste de 30 objets. Les clés des objets sont `latitude`, `longitude` et `daily`. Le DataFrame `meteo` a la forme `(21930, 8)`, soit 21 930 lignes et 8 colonnes.

À chaque tour de boucle, le script crée un tableau pour une ville et l’ajoute à `morceaux`. La liste est créée avant la boucle pour conserver les 30 tableaux, qui sont ensuite assemblés.

## Jour 2 — Mardi 10 : la chaîne s’enchaîne toute seule

### Exercice 1 — Ranger et numéroter

Les scripts SQL sont organisés dans l’ordre où ils doivent s’exécuter :

1. `01_init.sql`
2. `02_clean.sql`
3. `03_tables_meteo.sql`
4. `04_rattachement.sql`
5. `05_croisement.sql`
6. `06_controles.sql`

`04_rattachement.sql` associe chaque couple latitude/longitude retourné par Open-Meteo à la ville de référence la plus proche. Il ne peut donc pas s’exécuter avant le chargement de la météo.

`02_clean.sql` ne peut pas s’exécuter avant `01_init.sql`, car les tables sources, comme `dim_agence`, n’existent pas encore. Pour nettoyer les données, il faut d’abord initialiser la base, puis lancer le script de nettoyage.

### Exercice 2 — La liste et la boucle

L’ajout d’une quatrième étape à la liste s’effectue en une seule ligne avec la méthode `append`.

### Exercice 3 — Premier lancement complet

Le pipeline a réinitialisé la base, lu 30 villes et construit un tableau météo de 21 930 lignes et 8 colonnes. Il a ensuite exécuté les étapes SQL dans l’ordre prévu.

### Exercice 4 — Le journal des étapes

Lors d’un lancement, la réinitialisation de la base était l’étape la plus longue :

| Fichier               | Étape                              | Outil | Durée (s) |
|-----------------------|------------------------------------|-------|-----------|
| `01_init.sql`         | Réinitialiser la base              | SQL   | 156,8     |
| `02_clean.sql`        | Construire la couche propre        | SQL   | 36,1      |
| `03_tables_meteo.sql` | Créer les tables météo             | SQL   | 0,0       |
| `04_rattachement.sql` | Rattacher la météo aux sinistres   | SQL   | 0,0       |
| `05_croisement.sql`   | Croiser les sinistres et la météo  | SQL   | 0,1       |
| `06_controles.sql`    | Contrôler le résultat              | SQL   | 0,0       |

### Exercice 5 — Contrôler après chaque étape

#### Combien de lignes dans `clean_fact_sinistre` ?

La table brute `fact_sinistre` contenait 12 490 lignes. Après le nettoyage par `02_clean.sql`, `clean_fact_sinistre` en contient 12 098.

Le résultat est conforme aux attentes. Le nettoyage exclut notamment les doublons, les dates de survenance anormales, les contrats non actifs, les localisations manquantes et les montants anormaux; certains libellés sont corrigés.

#### Quelle étape vérifier en premier si le nombre était incorrect ?

Je vérifierais d’abord `02_clean.sql`, notamment ses filtres `WHERE`, la suppression des doublons (`DISTINCT` ou `ROW_NUMBER`) et les jointures. Une mauvaise jointure peut multiplier les lignes ou en éliminer. Je vérifierais ensuite les données sources et leur chargement par `01_init.sql`.

#### Que ne dit pas un contrôle pl  acé uniquement à la fin ?

Un contrôle final peut signaler une anomalie sans localiser son origine ni préciser la règle de gestion qui a échoué. Les contrôles intermédiaires permettent de circonscrire le problème à une étape.

#### Mise en commun — types de contrôles

| Type de contrôle                 | Moment d’utilisation                                       | Anomalie recherchée                            |
|----------------------------------|------------------------------------------------------------|------------------------------------------------|
| Volumétrie (comptage des lignes) | Après une étape de nettoyage ou de transformation          | Table vide ou rupture de flux     
| Intégrité et clés orphelines     | Après un croisement ou une jointure                 | Lignes perdues, doublons ou enregistrements orphelins |
| Valeurs nulles                   | Sur les colonnes critiques : montants, dates, identifiants | Données manquantes ou mal formatées            |
| Cohérence et plages de valeurs   | Sur les métriques : montants, températures, etc.           | Valeur impossible ou erreur de logique métier  |

## Jour 3 — Jeudi 12 : la météo entre dans la chaîne

### Exercice 1 — Du JSON à la base

Comptage des lignes dans DBeaver :

| Table                      | Lignes |
|----------------------------|--------|
| `meteo_assurrisk`          | 21 930 |
| `villes_coordonnees_meteo` | 31     |
| `meteo_assurrisk_ville`    | 21 930 |
| `fact_sinistre_meteo`      | 12 098 |

La table des coordonnées a une ligne de plus que les 30 villes : la ligne `inconnu`, avec des coordonnées `NULL`.

### Exercice 2 — La garde

Avant d’appeler l’API, le script doit lire les coordonnées des villes à interroger et créer les tables PostgreSQL qui recevront les données météo.

Si plusieurs personnes lancent le pipeline en même temps sans garde, les requêtes simultanées peuvent ralentir les réponses de l’API. Une garde aide à éviter cette surcharge.

### Exercice 3 — Brancher la météo au bon endroit

Les étapes SQL sont des fichiers à lire et à exécuter, tandis que le chargement météo est du Python (pandas et `COPY` via le curseur). Le séparer rend explicite qu’il doit se placer entre la création des tables et le rattachement.

### Exercice 4 — Rattachement et croisement

Le rattachement et le croisement sont exécutés après le chargement Python des données météo et des coordonnées.

### Exercice 5 — Comprendre les fonctions du pipeline

Les valeurs qui changent d’un appel à l’autre (fichier, libellé, outil et durée) sont les paramètres de `journaliser_etape`. Par exemple, `jouer_sql()` transmet `"SQL"` et `charger_table()` transmet `"Python"`.

La fonction centralise la structure de chaque entrée du journal. Après l’ajout de la colonne statut, elle ajoute également `"ok"` à chaque étape. Un seul `journal.append` dans la fonction remplace les ajouts répétés dans les différents traitements.

J’ai aussi écrit `compter_lignes(nom_table)` : cette fonction interroge la base et renvoie le nombre de lignes avec `return`.

**Contrôles obtenus :**

| Contrôle             | Résultat |
|----------------------|----------|
| Sinistres propres    | 12 098   |
| Lignes météo         | 21 930   |
| Villes rattachées    | 30       |
| Sinistres finaux     | 12 098   |
| Sinistres sans météo | 0        |
| Doublons météo       | 0        |

## Jour 4 — Vendredi 13 : livrer et montrer

### Exercice 1 — Le pipeline range derrière lui

En retirant `exist_ok=True`, la création du dossier `sorties` échoue lors d’une seconde exécution avec `FileExistsError`, car le dossier existe déjà. `exist_ok=True` permet au script de continuer si ce dossier existe.

### Exercice 2 — Casser une étape exprès

**À quel moment le pipeline s’arrête-t-il ?** Le journal ne contient que ses en-têtes si l’exécution s’interrompt avant son écriture finale. Le traceback du terminal permet de repérer l’erreur; lors de l’essai, c’était un `FileNotFoundError` pour `sql/01_ini.sql`.

**Le journal permet-il d’identifier l’étape en échec ?** Pas toujours : s’il est écrit seulement à la fin, les messages `[SQL]` du terminal montrent jusqu’où le pipeline est allé.

**Dans quel état se trouve la base ?** Avec `connexion.autocommit = True`, les commandes terminées avant l’erreur peuvent déjà être enregistrées. La base peut donc être dans un état partiel. Il faut relever le traceback avant de relancer le pipeline, car `01_init.sql` réinitialise les tables.

### Exercice 3 — Le journal et deux lancements

| Étape                   | Lancement 1 (s) | Lancement 2 (s) |
|-------------------------|-----------------|-----------------|
| `01_init.sql`           | 65,7            | 114,6           |
| `02_clean.sql`          | 14,9            | 26,6            |
| `03_tables_meteo.sql`   | 0,1             | 0,1             |
| Chargement mété         | 0,2             | 0,3             |
| `04_rattachement.sql`   | 0,1             | 0,2             |
| `05_croisement.sql`     | 0,1             | 0,3             |
| `06_controles.sql`      | 0,0             | 0,1             |

Les deux lancements comportent les mêmes étapes; les durées peuvent varier. Les contrôles relevés sont 12 098 sinistres propres et finaux, 21 930 lignes météo, 30 villes rattachées, aucun sinistre sans météo et aucun doublon météo.

### Exercice 4 — Versionner le projet avec Git

Un premier essai de `git commit` a répondu `nothing to commit` parce que `cahier.md` n’avait pas été ajouté à la zone de préparation. La séquence correcte pour ce fichier est :

```powershell
git add .\cahier.md
git commit -m "Mise à jour du cahier"
```

J’ai appris à versionner mes dossiers, à créer des commits et à consulter l’historique avec `git log`. Il reste à comprendre comment `git restore` agit sur un fichier suivi par Git lorsque l’exécution du programme génère aussi un journal CSV.

### Bonus — Ce que j’ai retenu

J’ai compris l’intérêt des fonctions quand j’ai ajouté le statut `"ok"` au journal : une seule fonction commune permet de l’ajouter à chaque étape.

## Notes d’analyse

### Enquête sur octobre 2025

Les données confirment qu’octobre 2025 est un mois particulièrement chargé et que les dégâts des eaux y occupent une part plus importante que le reste de la période. Cela rend l’hypothèse d’un rôle des pluies plausible, sans prouver qu’elles ont causé le pic. Pour la vérifier, il faudrait comparer, pour chaque ville et chaque jour, les dégâts des eaux lors des journées pluvieuses avec ceux des journées peu ou pas pluvieuses.

La phrase qui m’a le plus aidé à formuler une vérification est : « Si mon explication est vraie, je devrais voir beaucoup de sinistres liés aux dégâts des eaux concentrés à quelques dates ou dans certaines villes. »

### Franchise

La franchise moyenne est d’environ 228,70 € et sa médiane est de 200 €; elle semble souvent suivre un barème fixe.

## Bilan de la semaine

- **Ce que je sais faire :** versionner mes dossiers avec Git, créer des commits et consulter l’historique du projet.
- **Ce qui reste flou :** utiliser `git restore` et comprendre ce qui est restauré par Git par rapport à ce que le script régénère à l’exécution.
- **Le moment où j’ai compris :** l’ajout du statut `"ok"` au journal m’a montré comment une fonction commune évite de répéter la même modification à plusieurs endroits.


# Note sur l'importance de git restore

« git restore a remis explorer.py dans l’état du dernier commit, “Version cassee de   -explorer.py trois”, qui contenait déjà le code cassé ; le fichier est donc resté cassé. »