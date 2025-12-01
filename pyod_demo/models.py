from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List

from pydantic import BaseModel


class Transaction(BaseModel):
    AccountID: str
    TransactionDate: str
    Amount: float
    IsSuspicious: bool


@dataclass
class AccountFeatures:
    account_id: str
    tx_count_30d: int
    avg_amount_30d: float

    def as_tuple(self) -> tuple[float, float]:
        return float(self.tx_count_30d), float(self.avg_amount_30d)


@dataclass
class SuspiciousRanking:
    account_id: str
    anomaly_score: float

    def as_dict(self) -> Dict[str, str]:
        return {
            "account_id": self.account_id,
            "anomaly_score": f"{self.anomaly_score:.4f}",
        }
