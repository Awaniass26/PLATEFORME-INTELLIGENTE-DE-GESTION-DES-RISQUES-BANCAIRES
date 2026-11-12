# Rapport de qualité — Home Credit

**Périmètre :** `application_train.csv` (307 511 lignes, 122 colonnes), contrôle
exécuté localement le 12 novembre 2026. Les observations et le notebook
reproductible sont dans [`02_eda_home_credit.ipynb`](../notebooks/02_eda_home_credit.ipynb).
Les données brutes ne sont pas modifiées.

## Qualité générale

- `SK_ID_CURR` est unique : 307 511 identifiants distincts, aucun doublon.
- Aucune ligne entière dupliquée et aucune cible manquante.
- 55 des 122 colonnes n'ont aucune valeur manquante.
- 50 colonnes ont plus de 20 % de valeurs manquantes ; 41 en ont plus de 50 %
  et 17 en ont plus de 60 %.
- Les trois variables de surface commune (`COMMONAREA_AVG`, `_MODE`, `_MEDI`)
  ont chacune 214 865 valeurs manquantes (69,87 %).
- Les valeurs manquantes sont parfois plus fréquentes chez les dossiers en
  défaut : `EXT_SOURCE_3` est manquante pour 22,87 % des dossiers en défaut et
  19,56 % des autres dossiers. Il faut donc étudier l'indicateur de manque et
  éviter une imputation qui effacerait cette information sans analyse.

## Cible et déséquilibre

| `TARGET` | Nombre | Proportion |
|---|---:|---:|
| 0 — pas de défaut observé | 282 686 | 91,93 % |
| 1 — défaut observé | 24 825 | 8,07 % |

Une stratégie de classification ne doit pas être jugée par l'accuracy seule.
Utiliser au minimum PR-AUC, rappel, ROC-AUC et matrice de confusion, avec un
seuil opérationnel discuté séparément.

## Valeurs extrêmes et anomalie

Le critère de Tukey repère des observations au-delà de ses bornes pour les
variables de montant, sans démontrer qu'elles sont erronées :

| Variable | Hors bornes IQR | Proportion | Maximum |
|---|---:|---:|---:|
| `AMT_INCOME_TOTAL` | 14 035 | 4,56 % | 117 000 000 |
| `AMT_CREDIT` | 6 562 | 2,13 % | 4 050 000 |
| `AMT_ANNUITY` | 7 504 | 2,44 % | 258 025,50 |
| `AMT_GOODS_PRICE` | 14 728 | 4,79 % | 4 050 000 |

Ne pas supprimer ces valeurs automatiquement. Vérifier les unités et le
dictionnaire métier ; comparer les transformations robustes sur la validation.

`DAYS_EMPLOYED=365243` apparaît 55 374 fois (18,01 %). Le dictionnaire définit
la variable comme le nombre de jours depuis le début de l'emploi actuel ; ce
nombre dépasse une durée plausible. Le nettoyage conserve la ligne, transforme
ce code en valeur manquante et ajoute `DAYS_EMPLOYED_ANOMALY`. Les autres
manquants restent à traiter dans les pipelines d'entraînement.

## Associations avec la cible

Les plus fortes corrélations linéaires numériques observées avec `TARGET` sont
`EXT_SOURCE_3` (-0,1789), `EXT_SOURCE_2` (-0,1605) et `EXT_SOURCE_1` (-0,1553).
Ces associations ne sont pas causales. Elles méritent une vérification métier,
une analyse de disponibilité et une revue de risque de fuite avant de retenir
les variables.

Le taux de défaut passe d'environ 18,35 % dans le décile le plus bas de
`EXT_SOURCE_2` à 2,97 % dans le décile le plus élevé. Ce gradient descriptif
est cohérent avec les corrélations négatives, mais ne constitue pas une règle
de décision individuelle.

### Hypothèses testées

Pour `EXT_SOURCE_2`, `EXT_SOURCE_3` et `DAYS_BIRTH`, le test bilatéral de
Mann–Whitney compare les distributions des groupes TARGET=1 et TARGET=0. Les
trois tests restent significatifs après correction de Bonferroni (les p-values
calculées par SciPy sous-fluent à zéro en virgule flottante ; elles sont
inférieures à 1e-300). Le rang-bisérial résume la direction et l'ampleur de la
différence de rangs.

| Variable | Médiane défaut | Médiane sans défaut | Effet rang-bisérial |
|---|---:|---:|---:|
| `EXT_SOURCE_2` | 0,4404 | 0,5739 | -0,3122 |
| `EXT_SOURCE_3` | 0,3791 | 0,5460 | -0,3588 |
| `DAYS_BIRTH` (jours) | -14 282 | -15 877 | +0,1660 |

Les médianes correspondent à environ 39,1 ans chez les dossiers en défaut et
43,5 ans chez les autres. Le signe positif sur `DAYS_BIRTH` s'explique par sa
convention négative : les valeurs plus proches de zéro indiquent des personnes
plus jeunes. L'effectif rend les p-values très petites ; interpréter aussi les
effets et les facteurs confondants.

## Équité et limites d'interprétation

Le taux observé varie selon `CODE_GENDER` (6,999 % pour F et 10,142 % pour M).
La catégorie XNA ne contient que quatre dossiers. Ces chiffres sont descriptifs
et non ajustés ; ils ne prouvent pas un effet causal. La variable sensible ne
doit pas être retenue automatiquement comme prédicteur et nécessite une revue
d'équité et de conformité.

Les résultats concernent les dossiers Home Credit disponibles, pas toute la
population de demandeurs ni une population bancaire universelle. Le prototype
ne doit pas être utilisé pour prendre des décisions réelles de crédit.

## Décisions de prétraitement retenues

1. Conserver les lignes et identifiants uniques ; refuser les identifiants
   dupliqués plutôt que supprimer silencieusement des observations.
2. Convertir `DAYS_EMPLOYED=365243` en valeur manquante et garder un indicateur.
3. Ne pas tronquer les montants extrêmes sans validation métier.
4. Ajuster imputeurs, encodeurs et scalers après séparation train/validation,
   uniquement sur les données d'entraînement.
5. Mesurer la performance avec PR-AUC, rappel et ROC-AUC ; examiner les erreurs
   et les résultats par groupes pertinents.
