from typing import Optional, Dict

from pydantic import BaseModel


class TransactionResponseScheme(BaseModel):
    status: str


class TransactionRequestScheme(BaseModel):
    from_: int
    to: int
    amount: int
    comment: Optional[str] = None


class CheckIntegrityResponseScheme(BaseModel):
    blocks: list[Dict[str, str]]
