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
| Home Credit Default Risk | Scoring de crédit, jeu principal, feature engineering multi-tables | [Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk/data) | À récupérer ; aucun fichier trouvé |
| Default of Credit Card Clients (UCI) | Comparaison de modèles de scoring et comportement de remboursement | [UCI, dataset 350](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | Présent : fichier Excel `.xls` |
| Credit Card Fraud Detection | Détection de fraude et étude du déséquilibre | [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) | À récupérer ; aucun fichier trouvé |
| Lending Club Loan Data | Défaut et remboursement des prêts, estimation des pertes | [Kaggle](https://www.kaggle.com/datasets/wordsforthewise/lending-club) | Présent : CSV `accepted` et `rejected` |
| Bank Marketing | Souscription à un produit bancaire et comportement client | [UCI, dataset 222](https://archive.ics.uci.edu/dataset/222/bank+marketing) | À récupérer ; les dossiers présents ne contiennent pas le jeu de données |

Les données sont stockées localement dans `data/raw/` et exclues de Git. Les
CSV Lending Club présents font environ 1,68 Go et 1,78 Go : ils dépassent les
limites de taille d'un fichier GitHub. Les fichiers sources doivent être
téléchargés séparément depuis leurs éditeurs et utilisés selon leurs licences.

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

L'environnement Python et les dépendances seront définis avec les premiers
notebooks et scripts. Avant de lancer les analyses, vérifier que les fichiers
attendus sont présents sous `data/raw/<jeu>/`. Les données brutes ne doivent
pas être ajoutées au dépôt Git.

## Considérations

Les analyses doivent signaler les données manquantes, les biais potentiels et
les limites de représentativité. Les mesures de performance ne suffisent pas à
justifier une décision automatisée concernant une personne.
