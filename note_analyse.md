# Note d’analyse — sinistres et météo

## Partie 1 — Le montant d’un sinistre
- Observation : le montant estimé va de 80 € à 49 912 €.
- Mon hypothèse : le montant varie selon le type de sinistre et l’ampleur des dommages.
- Ce que j’avais décidé de vérifier AVANT : comparer les montants entre types à l’aide des moyennes et médianes.
- Ce que j’ai trouvé : les moyennes par type vont de 677,91 € (bris de glace) à 27 548,10 € (incendie); les médianes vont de 671,50 € à 26 957 €.
- Ma conclusion : les montants diffèrent selon le type dans ces données; confiance élevée dans les statistiques observées, mais elles n’expliquent pas les causes des écarts.

## Partie 2 — Le type de sinistre le plus fréquent
- Observation : les dégâts des eaux représentent 29,1 % des sinistres, devant le vol à 17,5 %.
- Mon hypothèse : les dégâts des eaux sont le type le plus fréquent dans chacune des 30 villes, et pas seulement dans le total.
- Ce que j’avais décidé de vérifier AVANT : comparer les nombres de chaque type dans chaque ville et repérer les premières places et les égalités.
- Ce que j’ai trouvé : les dégâts des eaux arrivent seuls en tête dans les 30 villes; aucune égalité, ni ville où un autre type les devance.
- Ma conclusion : l’hypothèse est confirmée pour les 30 villes étudiées; confiance élevée pour ce constat descriptif, sans explication de sa cause.

## Partie 3 — Octobre 2025
- Observation : du 1er au 28 octobre, il y a 1 940 sinistres, soit 69,3 par jour, la moyenne quotidienne la plus élevée de la période.
- Mon hypothèse : de fortes pluies ont pu contribuer au pic, notamment en augmentant les dégâts des eaux.
- Ce que j’avais décidé de vérifier AVANT : chercher si les dégâts des eaux et les fortes pluies coïncident aux mêmes dates et dans les mêmes villes.
- Ce que j’ai trouvé : les dégâts des eaux représentent 44,8 % des sinistres en octobre contre 26,1 % le reste de la période; à Grenoble, le 20 octobre, 44,7 mm de pluie coïncident avec 6 sinistres.
- Ma conclusion : le pic est confirmé, mais ces observations ne prouvent pas que la pluie l’a causé; confiance élevée dans le constat du pic, limitée dans son explication météorologique.

## Partie 4 — Ce que la météo n’explique pas
- Observation : les corrélations calculées par ville et par jour d’octobre sont proches de zéro.
- Mon hypothèse : s’il existe une association linéaire, davantage de pluie ou de rafales coïncidera avec davantage de sinistres correspondants.
- Ce que j’avais décidé de vérifier AVANT : calculer les corrélations pluie/tous les sinistres, pluie/dégâts des eaux et rafales/sinistres Tempête, par ville et par jour.
- Ce que j’ai trouvé : les coefficients de Pearson sont respectivement r = -0,039, r = -0,042 et r = 0,053.
- Ma conclusion : ces données ne montrent pas de relation linéaire marquée pour ces paires; confiance modérée dans ces associations descriptives, qui ne prouvent ni causalité ni absence d’autres liens.
