# EDA — UCI Credit Card et Bank Marketing

Résultats de [`05_eda_uci_bank_marketing.ipynb`](../notebooks/05_eda_uci_bank_marketing.ipynb),
exécuté le 13 novembre 2026. Les trois sources sont analysées séparément.
`bank-full` et `bank-additional-full` ne sont pas concaténés.

## UCI Default of Credit Card Clients

- 30 000 lignes, 25 colonnes, aucune valeur NaN explicite.
- L'identifiant `ID` est unique et il n'y a pas de ligne entièrement dupliquée.
  35 lignes partagent les mêmes valeurs hors identifiant ; elles ne sont pas
  supprimées automatiquement, car un profil d'attributs identique n'établit
  pas que deux dossiers correspondent à une seule observation.
- La cible comporte 6 636 défauts (22,12 %) et 23 364 non-défauts (77,88 %).
- Les codes `EDUCATION=0/5/6` apparaissent 345 fois au total ; la source attend
  les niveaux 1 à 4. `MARRIAGE=0` apparaît 54 fois alors que les niveaux
  documentés sont 1 à 3. Ce sont des codes à revoir ou regrouper comme
  indéterminés dans une étape de préparation, pas des lignes à effacer.
- `SEX` ne contient que les codes 1 et 2.

### Associations avec la cible

Les médianes observées sont de 90 000 contre 150 000 pour `LIMIT_BAL`, de 34
ans dans les deux classes, de 1 contre 0 pour `PAY_0` et de 1 636 contre
2 459,5 pour `PAY_AMT1` (respectivement défaut et non-défaut). Les tests de
Mann–Whitney pré-définis sur ces cinq variables sont ajustés par Bonferroni.
Après correction, l'âge ne montre pas de différence statistique (`p ajustée
≈ 1`), contrairement aux variables de limite, de remboursement et de paiement.

Le taux de défaut descriptif croît selon le statut `PAY_0` : il est de 12,81 %
pour le code 0, 33,95 % pour le code 1, 69,14 % pour le code 2 et 75,78 % pour
le code 3. Certaines catégories ont très peu d'observations ; ne pas
interpréter individuellement leurs taux comme des estimations stables.

Les tests du chi-deux pré-définis (sexe, éducation, mariage, `PAY_0` et
`PAY_2`) rejettent l'indépendance après correction de Bonferroni. Cela reste
des associations descriptives, pas des effets causaux.

## Bank Marketing `bank-full`

- 45 211 lignes, 17 colonnes ; aucune valeur manquante ni ligne complète
  dupliquée.
- 5 289 réponses positives (11,70 %).
- La source utilise les chaînes `unknown` plutôt que des NaN : par exemple
  `poutcome` est inconnu pour 36 959 dossiers et `contact` pour 13 020.
- `pdays=-1` signifie que le client n'avait pas été contacté lors d'une
  campagne précédente : 36 954 dossiers (81,74 %).
- Le taux de souscription par `poutcome` varie de 9,16 % pour `unknown` à
  64,73 % après un succès précédent.
- Le taux de souscription est de 12,88 % pour les clients ayant eu au plus
  trois contacts dans la campagne et de 7,35 % pour ceux qui en ont eu plus de
  trois ; il ne s'agit pas d'une comparaison causale.
- La source indique que les lignes de `bank-full` sont ordonnées dans le
  temps. Toute validation ultérieure doit préserver cet ordre plutôt que
  mélanger au hasard le passé et le futur.

## Bank Marketing Additional `bank-additional-full`

- 41 188 lignes, 21 colonnes ; aucune valeur NaN, mais 12 lignes entièrement
  identiques. Elles sont documentées et conservées dans l'EDA en attendant
  d'établir si elles sont des répétitions de données ou de véritables
  observations.
- 4 640 réponses positives (11,27 %).
- Les codes spéciaux `pdays=999` marquent les clients non contactés auparavant
  et couvrent 39 673 dossiers (96,32 %).
- L'issue `poutcome=success` est associée descriptivement à 65,11 % de
  souscriptions, contre 8,83 % pour `nonexistent`.
- Les indicateurs macroéconomiques ont des distributions distinctes entre les
  classes dans cet échantillon. Ils peuvent refléter le calendrier des
  campagnes et la conjoncture, plutôt qu'un comportement causal individuel.

## Fuite de cible et préparation

La documentation UCI de `bank-additional` avertit que `duration` est la durée
du dernier appel : elle est inconnue avant le contact et, une fois l'appel
terminé, la réponse est déjà connue. Les médianes descriptives sont d'environ
426 secondes pour les réponses positives et 164 secondes pour les négatives
dans `bank-full`, et de 449 contre 163,5 secondes dans `bank-additional`.
Cette association ne rend pas la variable disponible pour une prédiction
pré-contact : **exclure `duration` d'un tel modèle**. Les mêmes précautions
s'appliquent à toute autre variable qui ne serait connue qu'après la décision.

Les p-values qui s'affichent à zéro dans les tableaux sont inférieures à la
précision numérique flottante de SciPy, et non exactement nulles. Les grands
effectifs rendent les tests très sensibles ; tenir compte des médianes et
tailles d'effet. Les analyses ne sont pas des décisions causales.

## Décisions retenues

1. Traiter les variables de retard UCI `PAY_0` à `PAY_6` comme des niveaux de
   statut/catégories ordonnées, pas comme des montants continus ordinaires.
2. Documenter et regrouper explicitement les codes UCI hors nomenclature dans
   un pipeline ajusté seulement sur l'entraînement.
3. Conserver `unknown` et les sentinelles `pdays` comme catégories/informations
   distinctes jusqu'à l'étape de préparation.
4. Ne pas supprimer sans revue les 12 doublons de `bank-additional-full` ni
   les profils UCI répétés hors identifiant.
5. Pour une campagne marketing prospective, retirer `duration` et respecter
   l'ordre temporel de `bank-full` dans la validation.

Ces jeux ont des campagnes, périodes et populations différentes ; ne pas les
fusionner ni comparer directement leurs taux sans tenir compte de ce contexte.
