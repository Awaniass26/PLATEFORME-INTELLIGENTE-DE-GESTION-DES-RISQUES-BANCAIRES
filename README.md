# Plateforme intelligente de gestion des risques bancaires

Projet pédagogique de data science et de machine learning consacré à l'analyse
des risques bancaires : défaut de crédit, fraude et comportements clients. Le
cadrage métier détaillé est décrit dans
[`Module 03 Machine Learning.docx`](./Module%2003%20Machine%20Learning.docx).

> **Limite d'usage :** les modèles sont des prototypes pédagogiques. Ils ne sont
> pas conçus pour prendre de vraies décisions de crédit ou affecter des clients.

## Objectifs

- Explorer et documenter cinq jeux de données financiers publics.
- Étudier en priorité le risque de défaut avec Home Credit.
- Construire des pipelines de préparation reproductibles, sans fuite de données.
- Comparer les modèles avec des métriques adaptées aux classes déséquilibrées.
- Examiner les biais, l'explicabilité et les limites de représentativité.

Les jeux de données proviennent de populations et de contextes différents. Ils
seront analysés dans des notebooks et pipelines distincts, et ne seront pas
fusionnés artificiellement.

## Jeux de données

| Jeu de données | Usage prévu | Source | État dans l'espace de travail |
|---|---|---|---|
| Home Credit Default Risk | Scoring de crédit, jeu principal, feature engineering multi-tables | [Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk/data) | Présent : tables train/test et tables secondaires |
| Default of Credit Card Clients (UCI) | Comparaison de modèles de scoring et comportement de remboursement | [UCI, dataset 350](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | Présent : fichier Excel `.xls` |
| Credit Card Fraud Detection | Détection de fraude et étude du déséquilibre | [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | Présent : `creditcard.csv` |
| Lending Club Loan Data | Défaut et remboursement des prêts, estimation des pertes | [Kaggle](https://www.kaggle.com/datasets/wordsforthewise/lending-club) | Présent : CSV `accepted` et `rejected` |
| Bank Marketing | Souscription à un produit bancaire et comportement client | [UCI, dataset 222](https://archive.ics.uci.edu/dataset/222/bank+marketing) | Présent : variantes `bank` et `bank-additional` |

Les données sont stockées localement dans `data/raw/` et exclues de Git. Les
tables secondaires Home Credit et les CSV Lending Club sont volumineux ; les
deux CSV Lending Club font environ 1,68 Go et 1,78 Go, au-delà de la limite
GitHub de 100 Mo par fichier. Les fichiers sources doivent être utilisés selon
leurs licences ; le dépôt public ne contient que le code et la documentation.

L'inventaire détaillé et les premiers constats sont dans
[`docs/inventaire-donnees.md`](docs/inventaire-donnees.md) et
[`docs/observations-initiales.md`](docs/observations-initiales.md). Les notebooks
[`01_inventaire_initial.ipynb`](notebooks/01_inventaire_initial.ipynb) et
[`02_eda_home_credit.ipynb`](notebooks/02_eda_home_credit.ipynb) couvrent
l'inventaire et l'analyse approfondie prioritaire de Home Credit. Le notebook
[`03_feature_engineering_modelisation.ipynb`](notebooks/03_feature_engineering_modelisation.ipynb)
réalise les agrégations multi-tables et compare des modèles de crédit.
[`04_detection_fraude.ipynb`](notebooks/04_detection_fraude.ipynb) compare les
modèles fraude, le suréchantillonnage et les seuils sensibles aux coûts.
[`05_eda_uci_bank_marketing.ipynb`](notebooks/05_eda_uci_bank_marketing.ipynb)
explore les deux autres jeux UCI.

Les rapports détaillés sont dans
[`docs/rapport-qualite-home-credit.md`](docs/rapport-qualite-home-credit.md) et
[`docs/rapport-modeles-home-credit.md`](docs/rapport-modeles-home-credit.md)
ainsi que [`docs/rapport-detection-fraude.md`](docs/rapport-detection-fraude.md)
et [`docs/rapport-eda-uci-bank-marketing.md`](docs/rapport-eda-uci-bank-marketing.md).

## Architecture

```text
.
├── data/
│   ├── raw/                 # Fichiers d'origine, non suivis par Git
│   │   ├── home_credit/
│   │   ├── uci_credit_card/
│   │   ├── fraud/
│   │   ├── lending_club/
│   │   └── bank_marketing/
│   ├── interim/             # Données transformées intermédiaires
│   └── processed/           # Données prêtes pour les modèles
├── docs/                    # Cadrage, inventaire et rapports
├── notebooks/               # Exploration et modélisation documentées
├── src/
│   ├── data/                # Chargement et validation des données
│   ├── features/            # Construction des variables
│   ├── pipelines/           # Prétraitement et entraînement
│   └── evaluation/          # Métriques et rapports de modèles
├── models/                  # Modèles entraînés, non suivis par Git
├── reports/                 # Figures et résultats générés
├── tests/
├── .gitignore
└── README.md
```

## Feuille de route

1. **Cadrage et inventaire — terminé :** sources, fichiers, premiers
   `DataFrame.info()` et `DataFrame.describe()`.
2. **EDA Home Credit — première analyse terminée :** qualité, valeurs
   manquantes, distributions, valeurs extrêmes, corrélations, tests
   statistiques et nettoyage du code sentinelle. Étendre ensuite l'EDA aux
   autres jeux.
3. **Home Credit — implémenté :** agrégations historiques
   pour `bureau`, `previous_application` et `installments_payments` ;
   prétraitement scikit-learn ajusté dans les pipelines après le découpage
   train/validation ; comparaison logistique, Random Forest et XGBoost dans le
   notebook `03`. XGBoost obtient une PR-AUC/AP de 0,2792 sur ce split.
4. **Fraude — implémenté :** comparaison logistique pondérée, logistique +
   SMOTE, Random Forest pondérée et XGBoost pondéré ; choix d'un seuil sur la
   validation à partir de scénarios de coûts, puis mesure sur un test temporel
   final. Les métriques mesurées et les réserves sont dans le rapport fraude.
5. **EDA UCI Credit Card et Bank Marketing — terminée :** contrôles qualité,
   tests statistiques exploratoires, analyse des codes inconnus et repérage de
   la fuite de cible `duration`.

La revue des coûts de fraude reste à confirmer avec les responsables métier :
les ratios fournis dans le notebook sont des scénarios illustratifs.

## Démarrage

Python 3.10 ou plus récent est recommandé.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter lab
```

Les notebooks sont prévus pour être lancés depuis la racine du dépôt. Vérifier
que les fichiers attendus sont présents sous `data/raw/<jeu>/` avant l'analyse.
Les données brutes ne doivent pas être ajoutées au dépôt Git.

## Considérations

Les analyses doivent signaler les données manquantes, les biais potentiels et
les limites de représentativité. Les mesures de performance ne suffisent pas à
justifier une décision automatisée concernant une personne.
