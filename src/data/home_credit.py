"""Nettoyage minimal et traçable des données de demande Home Credit."""

import pandas as pd

DAYS_EMPLOYED_SENTINEL = 365243


def clean_application_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Convertir le code sentinelle d'emploi en valeur manquante avec indicateur.

    Les valeurs manquantes restantes et les valeurs extrêmes sont conservées :
    leur traitement appartient aux étapes d'analyse et aux pipelines appris
    uniquement sur les données d'entraînement.
    """
    required_columns = {"SK_ID_CURR", "DAYS_EMPLOYED"}
    missing_columns = required_columns.difference(frame.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colonnes Home Credit requises absentes : {missing}")

    if frame["SK_ID_CURR"].duplicated().any():
        raise ValueError("SK_ID_CURR doit être unique dans la table application.")

    cleaned = frame.copy()
    sentinel_rows = cleaned["DAYS_EMPLOYED"].eq(DAYS_EMPLOYED_SENTINEL).fillna(False)
    cleaned["DAYS_EMPLOYED_ANOMALY"] = sentinel_rows.astype("int8")
    cleaned.loc[sentinel_rows, "DAYS_EMPLOYED"] = float("nan")
    return cleaned
