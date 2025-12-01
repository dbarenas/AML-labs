import unittest
from pathlib import Path

from pyod import IForest
from pyod_demo.feature_engineering import FeatureEngineer, SuspiciousAccountService, TransactionRepository


class PyODDetectionTest(unittest.TestCase):
    def setUp(self) -> None:
        data_path = Path(__file__).resolve().parent.parent / "data" / "aml_data.csv"
        self.repository = TransactionRepository(data_path)
        self.engineer = FeatureEngineer(days_window=30)
        self.detector = IForest(contamination=0.01, random_state=42)
        self.service = SuspiciousAccountService(self.repository, self.engineer, self.detector)

    def test_suspicious_accounts_appear_in_top_scores(self) -> None:
        transactions = self.repository.load()
        suspicious_accounts = {tx.AccountID for tx in transactions if tx.IsSuspicious}

        ranked = self.service.rank_accounts()
        total_accounts = len(ranked)
        top_count = max(1, int(total_accounts * 0.05))
        top_accounts = {feature.account_id for feature, _ in ranked[:top_count]}

        detected = [acc for acc in suspicious_accounts if acc in top_accounts]
        if suspicious_accounts:
            detection_rate = len(detected) / len(suspicious_accounts)
        else:
            detection_rate = 1.0

        self.assertGreaterEqual(
            detection_rate,
            0.7,
            msg=f"El modelo solo detectó {detection_rate*100:.1f}% de las cuentas simuladas como sospechosas",
        )


if __name__ == "__main__":
    unittest.main()
