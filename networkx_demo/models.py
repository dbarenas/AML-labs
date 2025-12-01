from __future__ import annotations

from pydantic import BaseModel


class TransactionEdge(BaseModel):
    source: str
    target: str
    amount: float
