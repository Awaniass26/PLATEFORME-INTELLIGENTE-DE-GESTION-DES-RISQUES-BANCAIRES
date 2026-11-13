# Première comparaison de modèles — Home Credit

Résultats d'exécution de
[`03_feature_engineering_modelisation.ipynb`](../notebooks/03_feature_engineering_modelisation.ipynb)
le 13 novembre 2026. La table de modélisation contient 307 511 dossiers et
254 colonnes après agrégation historique. Les résultats mesurent une
validation stratifiée de 20 % du jeu `application_train` ; ils ne sont pas une
évaluation sur le jeu test de la compétition.

## Agrégations historiques

Les tables ont été réduites à un résumé par `SK_ID_CURR` avant la jointure :

| Table | Lignes brutes | Clients agrégés | Variables produites |
|---|---:|---:|---:|
| `bureau` | 1 716 428 | 305 811 | 60 |
| `previous_application` | 1 670 214 | 338 857 | 45 |
| `installments_payments` | 13 605 401 | 339 587 | 26 |

La jointure conserve les 307 511 dossiers et leur ordre. Les agrégations ne
lisent pas `TARGET`. Les imputations, le scaler et l'encodage catégoriel sont
ajustés dans chaque pipeline après le split train/validation.

## Résultats de validation

Modèles évalués sur les 61 503 lignes de validation, avec seuil descriptif
fixé à 0,5 :

| Modèle | ROC-AUC | PR-AUC / AP | Rappel | Précision | FP | FN |
|---|---:|---:|---:|---:|---:|---:|
| XGBoost | **0,7805** | **0,2792** | 0,6846 | 0,1852 | 14 954 | 1 566 |
| Régression logistique | 0,7662 | 0,2500 | **0,6979** | 0,1689 | 17 053 | 1 500 |
| Random Forest | 0,7479 | 0,2232 | 0,4393 | **0,2156** | 7 934 | 2 784 |

La prévalence de défaut est de 8,07 % ; XGBoost présente la meilleure
Average Precision sur ce split. Le choix du seuil 0,5 est provisoire et génère
encore beaucoup de faux positifs ; il ne représente pas un seuil métier
recommandé.

## Limites et prochaine étape

- Résultat issu d'un seul split stratifié et de paramètres initiaux, sans
  validation croisée ni optimisation d'hyperparamètres.
- La sélection de XGBoost utilise la PR-AUC de validation, mais le rapport ne
  présente pas de test final indépendant du split de validation.
- Le seuil devra être choisi selon un objectif explicite (coût d'erreur,
  capacité d'examen et rappel attendu) et évalué sur un test indépendant.
- Le pipeline sérialisé et le CSV complet de métriques sont générés localement
  dans `models/` et `reports/generated/`, exclus de Git.

Ces résultats sont pédagogiques et ne peuvent pas servir directement à une
décision réelle de crédit.
