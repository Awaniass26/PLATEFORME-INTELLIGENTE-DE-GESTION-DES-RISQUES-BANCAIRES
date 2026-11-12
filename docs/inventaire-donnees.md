# Inventaire des données

Inventaire vérifié le 12 novembre 2026. Les fichiers ci-dessous sont rangés
dans `data/raw/`. Ils ne sont pas suivis par Git : le dépôt public ne contient
que la structure de dossiers et la documentation.

## Disponibilité

| Jeu | Fichiers disponibles | État et remarques |
|---|---|---|
| Home Credit Default Risk | `application_train.csv`, `application_test.csv`, `bureau.csv`, `bureau_balance.csv`, `previous_application.csv`, `installments_payments.csv`, `POS_CASH_balance.csv`, `credit_card_balance.csv`, `HomeCredit_columns_description.csv`, `sample_submission.csv` | Disponible. `application_train.csv` porte la cible `TARGET`; les tables secondaires se relient au moyen des identifiants de prêt/client décrits dans le dictionnaire. |
| Default of Credit Card Clients (UCI) | `default of credit card clients.xls` | Disponible. L'en-tête lisible se trouve à la deuxième ligne de la feuille Excel (`header=1` avec pandas). La cible est `default payment next month`. |
| Credit Card Fraud Detection | `creditcard.csv` | Disponible. La cible de classification est `Class`. |
| Lending Club Loan Data | `accepted_2007_to_2018Q4.csv`, `rejected_2007_to_2018Q4.csv` | Disponible. Les deux CSV décompressés totalisent environ 3,3 Go. Les demandes rejetées n'ont pas d'issue de remboursement : ne pas leur attribuer une cible de défaut. |
| Bank Marketing (UCI) | `bank.csv`, `bank-full.csv`, `bank-additional.csv`, `bank-additional-full.csv` et deux fichiers descriptifs | Disponible. Fichiers séparés par des points-virgules. Les variantes `full` sont les versions complètes ; ne pas concaténer les deux versions du dataset. |

## Organisation

- `data/raw/` conserve les fichiers d'origine, sans transformation.
- `data/interim/` recevra les étapes de préparation intermédiaires.
- `data/processed/` recevra les jeux prêts pour l'entraînement.
- Les datasets restent indépendants : leurs populations, périodes et définitions
  de cible ne sont pas interchangeables.

## Sources

- [Home Credit Default Risk (Kaggle)](https://www.kaggle.com/competitions/home-credit-default-risk/data)
- [Default of Credit Card Clients (UCI, dataset 350)](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
- [Credit Card Fraud Detection (Kaggle)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- [Lending Club Loan Data (Kaggle)](https://www.kaggle.com/datasets/wordsforthewise/lending-club)
- [Bank Marketing (UCI, dataset 222)](https://archive.ics.uci.edu/dataset/222/bank+marketing)

Vérifier les licences et conditions de redistribution de chaque source avant
toute republication des données.
