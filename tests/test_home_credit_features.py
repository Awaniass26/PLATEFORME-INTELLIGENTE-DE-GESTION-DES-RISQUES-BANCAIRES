import unittest

import pandas as pd

from src.features.home_credit import (
    aggregate_bureau,
    aggregate_installments,
    aggregate_previous_applications,
    merge_historical_features,
)
from src.pipelines.home_credit import make_preprocessor


class HomeCreditFeatureTests(unittest.TestCase):
    def test_bureau_aggregation_counts_status_and_handles_missing_sums(self) -> None:
        bureau = pd.DataFrame(
            {
                "SK_ID_CURR": [10, 10, 20],
                "SK_ID_BUREAU": [1, 2, 3],
                "CREDIT_ACTIVE": ["Active", "Closed", "Active"],
                "AMT_CREDIT_SUM": [100.0, 200.0, None],
            }
        )

        features = aggregate_bureau(bureau)

        self.assertEqual(features.loc[10, "BUREAU_COUNT"], 2)
        self.assertEqual(features.loc[10, "BUREAU_AMT_CREDIT_SUM_SUM"], 300.0)
        self.assertTrue(pd.isna(features.loc[20, "BUREAU_AMT_CREDIT_SUM_SUM"]))
        self.assertEqual(features.loc[10, "BUREAU_ACTIVE_Active"], 1)

    def test_previous_applications_and_installments_are_aggregated_by_client(self) -> None:
        previous = pd.DataFrame(
            {
                "SK_ID_CURR": [10, 10],
                "NAME_CONTRACT_STATUS": ["Approved", "Refused"],
                "AMT_CREDIT": [100.0, 200.0],
            }
        )
        installments = pd.DataFrame(
            {
                "SK_ID_CURR": [10, 10],
                "AMT_INSTALMENT": [100.0, 100.0],
                "AMT_PAYMENT": [90.0, 110.0],
                "DAYS_INSTALMENT": [-10.0, -5.0],
                "DAYS_ENTRY_PAYMENT": [-8.0, -8.0],
            }
        )

        previous_features = aggregate_previous_applications(previous)
        installment_features = aggregate_installments(installments)

        self.assertEqual(previous_features.loc[10, "PREVIOUS_COUNT"], 2)
        self.assertEqual(previous_features.loc[10, "PREVIOUS_STATUS_Approved"], 1)
        self.assertEqual(installment_features.loc[10, "INSTALLMENTS_COUNT"], 2)
        self.assertEqual(installment_features.loc[10, "INSTALLMENTS_DAYS_PAST_DUE_MEAN"], 1.0)
        self.assertEqual(installment_features.loc[10, "INSTALLMENTS_PAYMENT_SHORTFALL_SUM"], 10.0)

    def test_merge_keeps_application_rows_and_order(self) -> None:
        applications = pd.DataFrame(
            {
                "SK_ID_CURR": [20, 10, 30],
                "TARGET": [0, 1, 0],
            }
        )
        bureau = pd.DataFrame(
            {
                "SK_ID_CURR": [10, 20],
                "SK_ID_BUREAU": [1, 2],
                "CREDIT_ACTIVE": ["Active", "Closed"],
                "AMT_CREDIT_SUM": [100.0, 200.0],
            }
        )

        merged = merge_historical_features(
            applications,
            bureau_features=aggregate_bureau(bureau),
        )

        self.assertEqual(merged["SK_ID_CURR"].tolist(), [20, 10, 30])
        self.assertEqual(merged["TARGET"].tolist(), [0, 1, 0])
        self.assertEqual(len(merged), len(applications))
        self.assertTrue(pd.isna(merged.loc[2, "BUREAU_COUNT"]))

    def test_duplicate_application_ids_are_rejected(self) -> None:
        applications = pd.DataFrame({"SK_ID_CURR": [1, 1]})

        with self.assertRaisesRegex(ValueError, "SK_ID_CURR"):
            merge_historical_features(applications)

    def test_preprocessor_learns_categories_on_training_rows_only(self) -> None:
        training = pd.DataFrame(
            {
                "amount": [10.0, None, 30.0],
                "category": ["A", "B", "A"],
            }
        )
        validation = pd.DataFrame(
            {
                "amount": [20.0],
                "category": ["unseen"],
            }
        )
        preprocessor = make_preprocessor(training)

        training_matrix = preprocessor.fit_transform(training)
        validation_matrix = preprocessor.transform(validation)

        categories = preprocessor.named_transformers_["categorical"].named_steps[
            "encoder"
        ].categories_[0]
        self.assertEqual(training_matrix.shape[0], 3)
        self.assertEqual(validation_matrix.shape[0], 1)
        self.assertNotIn("unseen", categories)


if __name__ == "__main__":
    unittest.main()
