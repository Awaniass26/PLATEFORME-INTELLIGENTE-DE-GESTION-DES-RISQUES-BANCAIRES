"""Agrégations historiques Home Credit, sans utiliser la cible."""

import numpy as np
import pandas as pd

CLIENT_ID = "SK_ID_CURR"


def _validate_columns(frame: pd.DataFrame, required: set[str], table: str) -> None:
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colonnes requises absentes de {table} : {missing}")


def _aggregate_numeric(
    frame: pd.DataFrame,
    columns: list[str],
    prefix: str,
) -> pd.DataFrame:
    groups = frame.groupby(CLIENT_ID, sort=False)
    features = pd.concat(
        [
            groups[columns].mean().add_suffix("_MEAN"),
            groups[columns].median().add_suffix("_MEDIAN"),
            groups[columns].max().add_suffix("_MAX"),
            groups[columns].min().add_suffix("_MIN"),
            groups[columns].sum(min_count=1).add_suffix("_SUM"),
        ],
        axis=1,
    )
    features.columns = [f"{prefix}_{column}" for column in features.columns]
    return features


def aggregate_bureau(frame: pd.DataFrame) -> pd.DataFrame:
    """Résumer les crédits externes par client."""
    _validate_columns(
        frame,
        {CLIENT_ID, "CREDIT_ACTIVE", "SK_ID_BUREAU"},
        "bureau",
    )
    numeric_columns = [
        column
        for column in [
            "DAYS_CREDIT",
            "CREDIT_DAY_OVERDUE",
            "DAYS_CREDIT_ENDDATE",
            "AMT_CREDIT_MAX_OVERDUE",
            "CNT_CREDIT_PROLONG",
            "AMT_CREDIT_SUM",
            "AMT_CREDIT_SUM_DEBT",
            "AMT_CREDIT_SUM_LIMIT",
            "AMT_CREDIT_SUM_OVERDUE",
            "DAYS_CREDIT_UPDATE",
            "AMT_ANNUITY",
        ]
        if column in frame.columns
    ]
    features = _aggregate_numeric(frame, numeric_columns, "BUREAU")
    features["BUREAU_COUNT"] = frame.groupby(CLIENT_ID, sort=False).size()

    active_counts = pd.crosstab(frame[CLIENT_ID], frame["CREDIT_ACTIVE"])
    active_counts = active_counts.add_prefix("BUREAU_ACTIVE_")
    return features.join(active_counts, how="left")


def aggregate_previous_applications(frame: pd.DataFrame) -> pd.DataFrame:
    """Résumer les demandes précédentes et leurs statuts par client."""
    _validate_columns(frame, {CLIENT_ID, "NAME_CONTRACT_STATUS"}, "previous_application")
    numeric_columns = [
        column
        for column in [
            "AMT_APPLICATION",
            "AMT_CREDIT",
            "AMT_DOWN_PAYMENT",
            "AMT_GOODS_PRICE",
            "AMT_ANNUITY",
            "DAYS_DECISION",
            "CNT_PAYMENT",
            "RATE_DOWN_PAYMENT",
        ]
        if column in frame.columns
    ]
    features = _aggregate_numeric(frame, numeric_columns, "PREVIOUS")
    features["PREVIOUS_COUNT"] = frame.groupby(CLIENT_ID, sort=False).size()

    status_counts = pd.crosstab(frame[CLIENT_ID], frame["NAME_CONTRACT_STATUS"])
    status_counts = status_counts.add_prefix("PREVIOUS_STATUS_")
    return features.join(status_counts, how="left")


def aggregate_installments(frame: pd.DataFrame) -> pd.DataFrame:
    """Résumer les retards et montants de paiement par client."""
    _validate_columns(
        frame,
        {
            CLIENT_ID,
            "AMT_INSTALMENT",
            "AMT_PAYMENT",
            "DAYS_INSTALMENT",
            "DAYS_ENTRY_PAYMENT",
        },
        "installments_payments",
    )
    payments = frame[
        [
            CLIENT_ID,
            "AMT_INSTALMENT",
            "AMT_PAYMENT",
            "DAYS_INSTALMENT",
            "DAYS_ENTRY_PAYMENT",
        ]
    ].copy()
    payments["PAYMENT_SHORTFALL"] = (
        payments["AMT_INSTALMENT"] - payments["AMT_PAYMENT"]
    ).clip(lower=0)
    payments["DAYS_PAST_DUE"] = (
        payments["DAYS_ENTRY_PAYMENT"] - payments["DAYS_INSTALMENT"]
    ).clip(lower=0)
    payments["PAYMENT_TO_INSTALLMENT_RATIO"] = payments["AMT_PAYMENT"].div(
        payments["AMT_INSTALMENT"].where(payments["AMT_INSTALMENT"].gt(0))
    )
    payments["PAYMENT_TO_INSTALLMENT_RATIO"] = (
        payments["PAYMENT_TO_INSTALLMENT_RATIO"]
        .replace([np.inf, -np.inf], np.nan)
    )

    numeric_columns = [
        "AMT_INSTALMENT",
        "AMT_PAYMENT",
        "PAYMENT_SHORTFALL",
        "DAYS_PAST_DUE",
        "PAYMENT_TO_INSTALLMENT_RATIO",
    ]
    features = _aggregate_numeric(payments, numeric_columns, "INSTALLMENTS")
    features["INSTALLMENTS_COUNT"] = payments.groupby(CLIENT_ID, sort=False).size()
    return features


def merge_historical_features(
    applications: pd.DataFrame,
    *,
    bureau_features: pd.DataFrame | None = None,
    previous_application_features: pd.DataFrame | None = None,
    installment_features: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Joindre les agrégations historiques sans modifier ni dupliquer les dossiers."""
    _validate_columns(applications, {CLIENT_ID}, "application")
    if applications[CLIENT_ID].duplicated().any():
        raise ValueError("SK_ID_CURR doit être unique dans la table application.")

    result = applications.copy()
    original_ids = applications[CLIENT_ID].reset_index(drop=True)
    aggregations = [
        bureau_features,
        previous_application_features,
        installment_features,
    ]
    for features in aggregations:
        if features is None:
            continue
        if features.index.has_duplicates:
            raise ValueError("Les agrégations historiques doivent avoir un client par ligne.")
        result = result.merge(
            features,
            left_on=CLIENT_ID,
            right_index=True,
            how="left",
            validate="one_to_one",
            sort=False,
        )

    if len(result) != len(applications) or not result[CLIENT_ID].equals(original_ids):
        raise RuntimeError("La jointure a modifié le nombre ou l'ordre des dossiers.")
    return result
