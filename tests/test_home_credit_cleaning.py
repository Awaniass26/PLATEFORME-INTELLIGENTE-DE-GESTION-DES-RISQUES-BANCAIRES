import unittest

import pandas as pd

from src.data.home_credit import clean_application_data


class CleanApplicationDataTests(unittest.TestCase):
    def test_sentinel_is_missing_and_flagged_without_mutating_input(self) -> None:
        source = pd.DataFrame(
            {
                "SK_ID_CURR": [1, 2, 3],
                "DAYS_EMPLOYED": [-1200, 365243, -30],
            }
        )

        cleaned = clean_application_data(source)

        self.assertEqual(cleaned["DAYS_EMPLOYED_ANOMALY"].tolist(), [0, 1, 0])
        self.assertTrue(pd.isna(cleaned.loc[1, "DAYS_EMPLOYED"]))
        self.assertEqual(cleaned.loc[0, "DAYS_EMPLOYED"], -1200)
        self.assertNotIn("DAYS_EMPLOYED_ANOMALY", source.columns)
        self.assertEqual(source.loc[1, "DAYS_EMPLOYED"], 365243)

    def test_missing_required_column_is_reported(self) -> None:
        source = pd.DataFrame({"SK_ID_CURR": [1]})

        with self.assertRaisesRegex(ValueError, "DAYS_EMPLOYED"):
            clean_application_data(source)

    def test_existing_missing_employment_value_is_preserved(self) -> None:
        source = pd.DataFrame(
            {
                "SK_ID_CURR": [1, 2],
                "DAYS_EMPLOYED": pd.Series([pd.NA, 365243], dtype="Int64"),
            }
        )

        cleaned = clean_application_data(source)

        self.assertTrue(pd.isna(cleaned.loc[0, "DAYS_EMPLOYED"]))
        self.assertTrue(pd.isna(cleaned.loc[1, "DAYS_EMPLOYED"]))
        self.assertEqual(cleaned["DAYS_EMPLOYED_ANOMALY"].tolist(), [0, 1])

    def test_duplicate_application_id_is_not_silently_removed(self) -> None:
        source = pd.DataFrame(
            {
                "SK_ID_CURR": [1, 1],
                "DAYS_EMPLOYED": [-100, -200],
            }
        )

        with self.assertRaisesRegex(ValueError, "SK_ID_CURR"):
            clean_application_data(source)


if __name__ == "__main__":
    unittest.main()
