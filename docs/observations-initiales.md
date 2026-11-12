# Premières observations

Résultats du notebook `01_inventaire_initial.ipynb`, exécuté le 12 novembre
2026. Pour Lending Club, les statistiques descriptives portent sur les 20 000
premières lignes de chaque CSV, pas sur l'ensemble des fichiers.

## Taille et déséquilibre des cibles

| Jeu / variante analysée | Forme (lignes × colonnes) | Répartition de la cible |
|---|---:|---|
| Home Credit `application_train` | 307 511 × 122 | `TARGET=0` : 282 686 (91,93 %) ; `TARGET=1` : 24 825 (8,07 %) |
| UCI Credit Card Clients | 30 000 × 25 | défaut `0` : 23 364 (77,88 %) ; défaut `1` : 6 636 (22,12 %) |
| Credit Card Fraud | 284 807 × 31 | `Class=0` : 284 315 (99,83 %) ; `Class=1` : 492 (0,17 %) |
| Bank Marketing `bank-full` | 45 211 × 17 | `no` : 39 922 (88,30 %) ; `yes` : 5 289 (11,70 %) |
| Bank Marketing `bank-additional-full` | 41 188 × 21 | `no` : 36 548 (88,73 %) ; `yes` : 4 640 (11,27 %) |
| Lending Club `accepted` (échantillon) | 20 000 × 151 | `loan_status` comporte plusieurs états ; définir la cible et les états à retenir avant l'entraînement |
| Lending Club `rejected` (échantillon) | 20 000 × 9 | pas de résultat de remboursement observé ; exclure du scoring supervisé de défaut |

## Premier contrôle qualité Home Credit

- La table d'entraînement comporte 122 colonnes et environ 505 MiB en mémoire
  une fois chargée dans pandas.
- La cible est fortement déséquilibrée : environ un défaut observé pour 12,4
  dossiers. L'accuracy seule ne sera donc pas une métrique suffisante.
- Dans les colonnes examinées, `AMT_ANNUITY` a 12 valeurs manquantes et
  `AMT_GOODS_PRICE` en a 278. Le traitement des valeurs manquantes doit être
  appris uniquement sur les données d'entraînement.
- Les statistiques `describe()` signalent des valeurs extrêmes à examiner,
  notamment `AMT_INCOME_TOTAL` (maximum observé : 117 000 000). Elles ne doivent
  pas être supprimées sans justification métier.

Ce relevé est un point de départ, pas encore l'audit approfondi des valeurs
manquantes, outliers, corrélations et biais.
