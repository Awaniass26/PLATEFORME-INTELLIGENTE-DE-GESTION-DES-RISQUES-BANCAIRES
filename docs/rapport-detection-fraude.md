# Rapport — détection de fraude

Résultats du notebook
[`04_detection_fraude.ipynb`](../notebooks/04_detection_fraude.ipynb), exécuté
localement le 13 novembre 2026 sur `data/raw/fraud/creditcard.csv`.

## Données et découpage

- 284 807 transactions, 31 colonnes, aucune valeur manquante.
- 492 fraudes (0,1727 %) et 284 315 transactions légitimes.
- 1 081 lignes identiques sur les 31 colonnes ; elles sont signalées mais pas
  supprimées silencieusement.
- Découpage par ordre temporel, sans mélanger le passé et le futur :

| Période | Lignes | Fraudes | Prévalence | Intervalle `Time` |
|---|---:|---:|---:|---:|
| Entraînement | 170 888 | 360 | 0,2107 % | 0–120 396 |
| Validation | 56 957 | 57 | 0,1001 % | 120 397–145 247 |
| Test final | 56 962 | 75 | 0,1317 % | 145 248–172 792 |

`Time` sert au découpage mais n'est pas fourni aux modèles ; `Amount` et `V1` à
`V28` sont utilisés comme variables explicatives. Les faibles nombres
d'événements en validation et test rendent les seuils et mesures sensibles à
quelques transactions.

## Comparaison sur la validation

Les modèles sont classés par Average Precision, souvent appelée PR-AUC/AP.
L'Average Precision est une synthèse pondérée de la courbe précision-rappel ;
elle est plus informative que l'accuracy brute sur une cible aussi rare.

| Modèle | ROC-AUC validation | PR-AUC / Average Precision |
|---|---:|---:|
| XGBoost avec `scale_pos_weight` | 0,97834 | **0,77894** |
| Logistique + SMOTE | 0,96440 | 0,77382 |
| Random Forest pondérée | 0,97140 | 0,77302 |
| Logistique `class_weight="balanced"` | 0,97091 | 0,77231 |

SMOTE est appliqué seulement aux lignes du train, à l'intérieur du pipeline,
après imputation et standardisation. La validation et le test gardent leur
prévalence naturelle.

## Seuil fondé sur les coûts

Les coûts réels ne sont pas fournis par le dataset. Le notebook teste donc des
ratios **illustratifs** entre le coût d'un faux négatif et celui d'un faux
positif (1:1, 5:1, 10:1, 20:1, 50:1). Pour chaque ratio, le seuil qui minimise
`FN × coût_FN + FP × coût_FP` est sélectionné sur la validation uniquement.

Pour XGBoost :

| Ratio coût FN:FP | Seuil validation | FP validation | FN validation | Coût relatif validation |
|---:|---:|---:|---:|---:|
| 1:1 | 0,94079 | 3 | 14 | 17 |
| 5:1 | 0,94079 | 3 | 14 | 73 |
| **10:1 (référence provisoire)** | **0,77261** | **10** | **13** | **140** |
| 20:1 | 0,77261 | 10 | 13 | 270 |
| 50:1 | 0,25064 | 60 | 11 | 610 |

Le tableau illustre le compromis : quand manquer une fraude coûte plus cher,
le seuil baisse et davantage de transactions légitimes sont signalées. Les
ratios ne sont pas des valeurs monétaires constatées. Ils doivent être remplacés
par le coût moyen d'une enquête et la perte attendue par fraude manquée, définis
et approuvés par le métier.

## Évaluation sur le test temporel

Le modèle retenu sur la PR-AUC de validation est XGBoost. Le seuil 0,77261,
choisi sur la validation pour le scénario 10:1, est ensuite appliqué sans
modification au test final :

| Mesure test | Résultat |
|---|---:|
| ROC-AUC | 0,97463 |
| PR-AUC / Average Precision | 0,79718 |
| Seuil fixe issu de la validation | 0,77261 |
| Vrais négatifs | 56 875 |
| Faux positifs (alertes inutiles) | 12 |
| Faux négatifs (fraudes manquées) | 18 |
| Vrais positifs (fraudes détectées) | 57 |
| Précision au seuil choisi | 82,61 % |
| Rappel au seuil choisi | 76,00 % |
| Coût relatif (FN × 10 + FP × 1) | 192 |

Ces comptes concernent seulement 75 fraudes dans la période de test ; une
variation de quelques événements changerait sensiblement le rappel. Le coût
relatif de 192 n'est interprétable qu'à l'intérieur du scénario hypothétique
10:1, et n'est pas une perte monétaire.

### Montants des erreurs

Sur le test, les 12 faux positifs représentent un montant de transaction cumulé
de 27 138,27 ; les 18 fraudes manquées, 2 638,27 ; les 57 fraudes détectées,
5 090,99. Le champ `Amount` est un montant descriptif du dataset. Il ne mesure
ni la perte effectivement subie, ni la récupération, ni le coût de revue.

## Limites et suites

- SMOTE synthétise des observations ; il ne crée pas de vraies transactions et
  peut modifier le calibrage des probabilités.
- Le jeu historique anonymisé n'offre ni identité client, ni coût de revue,
  ni perte nette observée.
- Les performances sont pédagogiques et ne justifient pas un déploiement.
- Avant tout usage métier, choisir les coûts réels, vérifier la calibration,
  mesurer le taux d'alertes supportable, étudier la stabilité dans le temps et
  refaire l'évaluation sur plusieurs fenêtres temporelles.
