import logging

from fastapi import FastAPI

from schemes import (
    TransactionResponseScheme,
    TransactionRequestScheme,
    CheckIntegrityResponseScheme
)
from blockchain import write_block, check_integrity
from db import db

app = FastAPI(
    title="Simple API with blockchain",
    docs_url="/"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

@app.on_event("startup")
async def on_startup():
    """If genesis block is not exists then need create it"""

    genesis_block = await db.blocks.find_one({"_id": 1})
    if not genesis_block:
        logger.info("Genesis block is not exists, creating...")
        await db.blocks.insert_one(
            {
                "_id": 1,
                "from": 0,
                "to": 0,
                "amount": 0,
                "comment": "",
                "prev_hash": ""
            }
        )


@app.post("/api/transaction", response_model=TransactionResponseScheme)
async def transaction(
    data: TransactionRequestScheme
):
    """Add transaction to blocks of blockchain"""

    await write_block(
        from_=data.from_,
        to=data.to,
        amount=data.amount,
        comment=data.comment
    )
    return {"status": "OK"}


@app.get("/api/transactions/check", response_model=CheckIntegrityResponseScheme)
async def check_integrity_transactions():
    """Check integrity blocks of blockchain"""

    total_check = await check_integrity()
    return {"blocks": total_check}
