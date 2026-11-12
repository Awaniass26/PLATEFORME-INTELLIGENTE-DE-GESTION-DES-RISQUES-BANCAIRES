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
| Credit Card Fraud Detection | Détection de fraude et étude du déséquilibre | [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | À récupérer ; aucun fichier trouvé |

Les données sont stockées localement dans `data/raw/` et exclues de Git. Les
tables secondaires Home Credit et les CSV Lending Club sont volumineux ; les
deux CSV Lending Club font environ 1,68 Go et 1,78 Go, au-delà de la limite
GitHub de 100 Mo par fichier. Les fichiers sources doivent être utilisés selon
leurs licences ; le dépôt public ne contient que le code et la documentation.

L'inventaire détaillé et les premiers constats sont dans
[`docs/inventaire-donnees.md`](docs/inventaire-donnees.md) et
[`docs/observations-initiales.md`](docs/observations-initiales.md). Le notebook
[`notebooks/01_inventaire_initial.ipynb`](notebooks/01_inventaire_initial.ipynb)
exécute les premiers `info()` et `describe()`.

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

1. **Cadrage et inventaire :** documenter les sources, vérifier les fichiers,
   puis produire les premiers `DataFrame.info()` et `DataFrame.describe()`.
2. **EDA et qualité :** commencer par Home Credit ; analyser valeurs manquantes,
   distributions, valeurs extrêmes, corrélations et déséquilibre des classes.
3. **Prétraitement :** créer des pipelines scikit-learn reproductibles et
   anti-fuite ; agréger les tables secondaires Home Credit.
4. **Scoring :** comparer une régression logistique, une Random Forest et, si
   disponible dans l'environnement, XGBoost/LightGBM avec ROC-AUC, PR-AUC,
   rappel et matrice de confusion.

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
