from fastapi import FastAPI

from schemes import (
    TransactionResponseScheme,
    TransactionRequestScheme,
    CheckIntegrityResponseScheme
)
from blockchain import write_block, check_integrity

app = FastAPI(
    title="Simple API with blockchain",
    docs_url="/"
)


@app.post("/api/transaction", response_model=TransactionResponseScheme)
async def transaction(
    data: TransactionRequestScheme
):
    """Add transaction to blocks of blockchain"""

    write_block(
        from_=data.from_,
        to=data.to,
        amount=data.amount,
        comment=data.comment
    )
    return {"status": "OK"}


@app.get("/api/transactions/check", response_model=CheckIntegrityResponseScheme)
async def check_integrity_transactions():
    """Check integrity blocks of blockchain"""

    total_check = check_integrity()
    return {"blocks": total_check}
