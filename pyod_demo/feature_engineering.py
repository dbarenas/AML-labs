from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List

from pyod_demo.models import AccountFeatures, Transaction


class TransactionRepository:
    """Carga transacciones desde CSV y las valida."""

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path

    def load(self) -> List[Transaction]:
        transactions: List[Transaction] = []
        with self.csv_path.open() as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                transactions.append(
                    Transaction(
                        AccountID=row["AccountID"],
                        TransactionDate=row["TransactionDate"],
                        Amount=float(row["Amount"]),
                        IsSuspicious=row["IsSuspicious"].lower() == "true",
                    )
                )
        return transactions


class FeatureEngineer:
    """Calcula métricas agregadas por cuenta."""

    def __init__(self, days_window: int = 30) -> None:
        self.days_window = days_window

    def build_features(self, transactions: Iterable[Transaction]) -> List[AccountFeatures]:
        tx_by_account: Dict[str, List[Transaction]] = {}
        for tx in transactions:
            tx_by_account.setdefault(tx.AccountID, []).append(tx)

        if not tx_by_account:
            return []

        max_date = max(datetime.fromisoformat(tx.TransactionDate).date() for tx_list in tx_by_account.values() for tx in tx_list)
        cutoff = max_date - timedelta(days=self.days_window)

        features: List[AccountFeatures] = []
        for account_id, tx_list in tx_by_account.items():
            recent = [tx for tx in tx_list if datetime.fromisoformat(tx.TransactionDate).date() >= cutoff]
            tx_count = len(recent)
            avg_amount = sum(tx.Amount for tx in recent) / tx_count if tx_count else 0.0
            features.append(
                AccountFeatures(
                    account_id=account_id,
                    tx_count_30d=tx_count,
                    avg_amount_30d=avg_amount,
                )
            )
        return features


class SuspiciousAccountService:
    """Orquestador para procesar y detectar anomalías."""

    def __init__(self, repository: TransactionRepository, feature_engineer: FeatureEngineer, detector) -> None:
        self.repository = repository
        self.feature_engineer = feature_engineer
        self.detector = detector

    def detect(self) -> List[AccountFeatures]:
        transactions = self.repository.load()
        features = self.feature_engineer.build_features(transactions)
        feature_vectors = [feature.as_tuple() for feature in features]
        self.detector.fit(feature_vectors)
        return features

    def rank_accounts(self) -> List[tuple[AccountFeatures, float]]:
        features = self.detect()
        scores = self.detector.decision_scores_
        ranked = sorted(zip(features, scores), key=lambda item: item[1], reverse=True)
        return ranked
