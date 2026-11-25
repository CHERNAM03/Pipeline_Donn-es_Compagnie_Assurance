# Enquêtes sur les sinistres AssurRisk

Ce document rassemble les observations, hypothèses, vérifications et conclusions
réalisées à partir des données de sinistres et de météo.

## 1. Le dégât des eaux est-il le type le plus fréquent dans les 30 villes ?

### Observation

Dans les 30 villes étudiées, le dégât des eaux est le type de sinistre le plus
fréquent. Sur l’ensemble des dossiers, il représente 29,1 % des sinistres; le
vol arrive ensuite avec 17,5 %.

### Question et hypothèse

**Question :** le dégât des eaux arrive-t-il en tête dans chacune des 30 villes ?

**Hypothèse :** il est réellement plus fréquent que les autres types dans chaque
ville, et pas seulement dans le total parce que certaines villes comptent
davantage de sinistres.

### Vérification décidée à l’avance

Comparer, pour chaque ville, le nombre de sinistres de chaque type et leur
classement. Si l’hypothèse est fausse, au moins une ville devrait avoir un autre
type en tête ou une égalité.

### Résultats

- Le dégât des eaux est seul en tête dans les **30 villes sur 30**.
- Il n’y a **aucune égalité** en tête et aucune ville où un autre type le devance.
- Sa part varie de **23,1 % à 34,8 %** selon la ville.

### Conclusion et confiance

L’hypothèse est confirmée pour les données étudiées : le dégât des eaux est le
type le plus fréquent dans chacune des 30 villes. La confiance dans ce constat
descriptif est élevée, car le classement a été vérifié ville par ville. Cette
analyse n’explique pas pourquoi ce type arrive en tête.

## 2. Que s’est-il passé en octobre 2025 ?

### Observation

Le nombre de sinistres est particulièrement élevé en octobre 2025. Les données
couvrent la période du **1er janvier 2024 au 28 octobre 2025**.

### Question et hypothèse

**Question :** le pic d’octobre coïncide-t-il avec des conditions météo
exceptionnelles ?

**Hypothèse :** de fortes pluies ont pu contribuer à l’augmentation des
sinistres, notamment des dégâts des eaux.

### Vérification décidée à l’avance

Vérifier si les dégâts des eaux sont concentrés aux mêmes dates et dans les
mêmes villes que les fortes pluies. Une coïncidence peut rendre l’hypothèse
plausible, mais ne suffit pas à démontrer une causalité ni un lien avec le
changement climatique.

### Résultats

- Il y a **1 940 sinistres en octobre**, du 1er au 28, soit **69,3 par jour**.
- C’est la moyenne quotidienne la plus élevée de la période; la suivante est de
  **36,7 par jour**, en février 2025.
- Les dégâts des eaux représentent **44,8 %** des sinistres en octobre, contre
  **26,1 %** le reste de la période, soit **18,7 points de plus**.
- À Grenoble, le 20 octobre, **44,7 mm** de pluie coïncident avec **6 sinistres**.
  Ce total inclut tous les types, pas seulement les dégâts des eaux.
- La comparaison des totaux bruts (1 940 en octobre contre 10 158 le reste de
  la période) est peu pertinente, car les périodes n’ont pas la même durée.

La répartition régionale ressemble globalement à celle du reste de la période.
La Normandie passe de 9,3 % à 11,3 % (+2 points), et les Hauts-de-France
augmentent de 1,5 point. L’Occitanie baisse de 1,3 point et la Bretagne de
1,1 point. Ces écarts ne démontrent pas qu’une tempête a causé le pic.

| Région                     | Octobre (%) | Reste (%) | Écart (points) |
|----------------------------|-------------|-----------|----------------|
| Normandie                  | 11,3        | 9,3       | +2,0           |
| Hauts-de-France            | 7,6         | 6,2       | +1,5           |       
| Pays de la Loire           | 6,5         | 6,1       | +0,4           |
| Provence-Alpes-Côte d’Azur | 13,5        | 13,1      | +0,4           |
| Auvergne-Rhône-Alpes       | 10,7        | 10,6      | +0,1           |
| Centre-Val de Loire        | 3,0         | 3,2       | −0,2           |
| Bourgogne-Franche-Comté    | 6,1         | 6,4       | −0,3           |
| Île-de-France              | 2,8         | 3,2       | −0,4           |
| Nouvelle-Aquitaine         | 6,8         | 7,3       | −0,5           |
| Grand Est                  | 12,1        | 12,7      | −0,6           |
| Bretagne                   | 5,3         | 6,3       | −1,1           |
| Occitanie                  | 14,3        | 15,6      | −1,3           |

### Conclusion et confiance

Le pic d’octobre et la part plus élevée des dégâts des eaux sont confirmés
dans la table. Le rôle possible des pluies reste une hypothèse : les
coïncidences observées ne prouvent pas qu’elles ont causé le pic. La confiance
est élevée pour le constat du pic, mais limitée pour son explication par la
météo.

## 3. Combien de temps s’écoule avant la déclaration ?

### Observation

Je veux mesurer le délai entre la date de survenance d’un sinistre et sa date
de déclaration.

### Question et hypothèse

**Question :** les délais de déclaration varient-ils selon le type de sinistre ?

**Hypothèse :** si les délais sont similaires, les moyennes et médianes par type
devraient être proches; des différences importantes indiqueraient des délais
distincts entre types.

### Vérification décidée à l’avance

Calculer le délai en jours entre `date_survenance` et `date_declaration`, puis
comparer les moyennes et médianes par type. Vérifier également les valeurs
manquantes, les déclarations le jour même et les déclarations antérieures au
sinistre.

### Résultats

- Les **12 098 dossiers** ont une date de déclaration.
- Le délai va de **1 à 27 jours**; la moyenne est de **13,9 jours** et la
  médiane de **14 jours**.
- Les moyennes par type vont de **13,5 jours** pour la responsabilité civile à
  **14,4 jours** pour l’inondation.
- La médiane est de **14 jours** pour presque tous les types et de **15 jours**
  pour l’inondation.
- Aucune déclaration n’a lieu le jour même ou avant la survenance.

### Conclusion et confiance

Dans les dossiers étudiés, les sinistres sont généralement déclarés environ
deux semaines après leur survenance. Les délais moyens sont proches selon le
type; je ne constate pas de grande différence descriptive. La confiance dans
les statistiques calculées sur cette table est élevée, mais elles n’expliquent
pas les délais et ne permettent pas de généraliser à d’autres dossiers.

## 4. Le statut du dossier varie-t-il selon le type de sinistre ?

### Observation

La répartition des statuts semble différente selon le type de sinistre.

### Question et hypothèse

**Question :** le statut d’un dossier est-il associé au type de sinistre ?

**Hypothèse :** si les proportions de statuts varient selon le type, les données
montrent une association descriptive entre ces deux variables.

### Vérification décidée à l’avance

Comparer les pourcentages de chaque statut à l’intérieur de chaque type de
sinistre, plutôt que les nombres bruts, qui dépendent de la taille des groupes.

### Résultats

- Parmi les incendies, **98,7 %** des dossiers sont clôturés.
- Parmi les inondations, **75 %** des dossiers sont refusés.
- Pour les dégâts des eaux, **34,0 %** sont clôturés et **25,5 %** expertisés.

| Type de sinistre      | Clôturé (%) | Déclaré (%) | En cours (%) | Expertisé (%) | Refusé (%) |
|-----------------------|-------------|-------------|--------------|---------------|------------|
| Bris de glace         | 14,1        | 8,2         | 35,3         | 7,1           | 35,3       |
| Dégât des eaux        | 34,0        | 9,2         | 22,7         | 25,5          | 8,5        |
| Grêle                 | 31,1        | 6,7         | 31,1         | 0,0           | 31,1       |
| Incendie              | 98,7        | 1,3         | 0,0          | 0,0           | 0,0        |
| Inondation            | 25,0        | 0,0         | 0,0          | 0,0           | 75,0       |
| Responsabilité civile | 55,6        | 0,0         | 0,0          | 44,4          | 0,0        |
| Tempête               | 45,9        | 1,7         | 6,6          | 32,8          | 13,1       |
| Vol v                 | 47,3        | 5,5         | 23,6         | 23,6          | 0,0        |

### Conclusion et confiance

Dans les dossiers étudiés, la répartition des statuts varie selon le type de
sinistre. Cela décrit une association, mais ne permet pas à lui seul d’expliquer
les écarts ni d’établir qu’un type de sinistre cause un statut donné.
