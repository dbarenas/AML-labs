from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, List


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "aml_data.csv"


@dataclass
class TransactionRow:
    account_id: str
    transaction_date: date
    amount: float
    is_suspicious: bool

    def as_dict(self) -> dict:
        return {
            "AccountID": self.account_id,
            "TransactionDate": self.transaction_date.isoformat(),
            "Amount": f"{self.amount:.2f}",
            "IsSuspicious": str(self.is_suspicious),
        }


class AMLDataGenerator:
    """Genera registros transaccionales reproducibles.

    La clase mantiene una responsabilidad clara: construir y persistir datos de
    entrenamiento sintéticos para las demos y pruebas unitarias.
    """

    def __init__(
        self,
        seed: int = 42,
        total_rows: int = 1000,
        suspicious_accounts: int = 3,
        suspicious_transactions_per_account: int = 30,
    ) -> None:
        self.seed = seed
        self.total_rows = total_rows
        self.suspicious_accounts = suspicious_accounts
        self.suspicious_transactions_per_account = suspicious_transactions_per_account
        self._rng = random.Random(self.seed)

    def _create_account_ids(self, count: int) -> List[str]:
        return [f"A{9000 + idx}" for idx in range(1, count + 1)]

    def _generate_normal_transactions(self, account_ids: List[str], rows_needed: int) -> Iterable[TransactionRow]:
        base_date = date.today()
        for _ in range(rows_needed):
            yield TransactionRow(
                account_id=self._rng.choice(account_ids),
                transaction_date=base_date - timedelta(days=self._rng.randint(0, 120)),
                amount=self._rng.uniform(1500, 25000),
                is_suspicious=False,
            )

    def _generate_suspicious_transactions(self, account_ids: List[str]) -> List[TransactionRow]:
        base_date = date.today()
        suspicious_rows: List[TransactionRow] = []
        for account in account_ids:
            indices_marked = set(self._rng.sample(range(self.suspicious_transactions_per_account), k=2))
            for idx in range(self.suspicious_transactions_per_account):
                suspicious_rows.append(
                    TransactionRow(
                        account_id=account,
                        transaction_date=base_date - timedelta(days=self._rng.randint(0, 30)),
                        amount=self._rng.uniform(900, 1000),
                        is_suspicious=idx in indices_marked,
                    )
                )
        return suspicious_rows

    def generate(self) -> List[TransactionRow]:
        normal_account_count = 60
        suspicious_ids = self._create_account_ids(self.suspicious_accounts)
        normal_ids = self._create_account_ids(normal_account_count + self.suspicious_accounts)[self.suspicious_accounts :]

        suspicious_rows = self._generate_suspicious_transactions(suspicious_ids)
        remaining_rows = self.total_rows - len(suspicious_rows)
        normal_rows = list(self._generate_normal_transactions(normal_ids, rows_needed=remaining_rows))

        full_dataset = suspicious_rows + normal_rows
        self._rng.shuffle(full_dataset)
        return full_dataset

    def save(self, rows: Iterable[TransactionRow], path: Path = DATA_FILE) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["AccountID", "TransactionDate", "Amount", "IsSuspicious"])
            writer.writeheader()
            for row in rows:
                writer.writerow(row.as_dict())
        return path


def generate_dataset() -> Path:
    generator = AMLDataGenerator()
    dataset = generator.generate()
    return generator.save(dataset)


if __name__ == "__main__":
    output = generate_dataset()
    print(f"Dataset escrito en {output}")
