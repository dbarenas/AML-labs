from __future__ import annotations

from pathlib import Path

from pyod import IForest
from pyod_demo.feature_engineering import FeatureEngineer, SuspiciousAccountService, TransactionRepository
from pyod_demo.models import SuspiciousRanking

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "aml_data.csv"


def main() -> None:
    repository = TransactionRepository(DATA_FILE)
    engineer = FeatureEngineer(days_window=30)
    detector = IForest(contamination=0.01, random_state=42)
    service = SuspiciousAccountService(repository, engineer, detector)

    ranked = service.rank_accounts()
    top_10 = ranked[:10]
    print("Top 10 cuentas con mayor puntuación de anomalía:")
    for feature, score in top_10:
        ranking = SuspiciousRanking(account_id=feature.account_id, anomaly_score=score)
        print(ranking.as_dict())


if __name__ == "__main__":
    main()
