import unittest

import numpy as np

from src.evaluation.fraud import (
    evaluate_fraud_threshold,
    select_cost_sensitive_threshold,
)


class FraudEvaluationTests(unittest.TestCase):
    def test_cost_threshold_uses_validation_only_and_minimizes_weighted_errors(self):
        truth = np.array([0, 0, 0, 1, 1])
        probabilities = np.array([0.05, 0.2, 0.7, 0.4, 0.9])

        result = select_cost_sensitive_threshold(
            truth,
            probabilities,
            false_negative_cost=10,
            false_positive_cost=1,
        )

        self.assertEqual(result["threshold"], 0.4)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["false_negatives"], 0)
        self.assertEqual(result["validation_cost"], 1)

    def test_equal_cost_prefers_higher_threshold_on_a_tie(self):
        truth = np.array([0, 1])
        probabilities = np.array([0.4, 0.6])

        result = select_cost_sensitive_threshold(
            truth,
            probabilities,
            false_negative_cost=1,
            false_positive_cost=1,
        )

        self.assertEqual(result["threshold"], 0.6)

    def test_evaluation_reports_all_confusion_matrix_cells(self):
        result = evaluate_fraud_threshold(
            np.array([0, 0, 1, 1]),
            np.array([0.1, 0.8, 0.7, 0.2]),
            threshold=0.5,
        )

        self.assertEqual(result["true_negatives"], 1)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["false_negatives"], 1)
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["precision"], 0.5)
        self.assertEqual(result["recall"], 0.5)

    def test_invalid_costs_and_probabilities_are_reported(self):
        with self.assertRaisesRegex(ValueError, "false_negative_cost"):
            select_cost_sensitive_threshold(
                [0, 1],
                [0.2, 0.8],
                false_negative_cost=0,
                false_positive_cost=1,
            )
        with self.assertRaisesRegex(ValueError, "probabilités"):
            evaluate_fraud_threshold([0, 1], [0.2, 1.2], threshold=0.5)


if __name__ == "__main__":
    unittest.main()
