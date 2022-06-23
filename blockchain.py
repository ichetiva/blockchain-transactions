import hashlib
import os
from typing import Optional

from db import db

BLOCKCHAIN_DIR = os.curdir + "/blocks/"


async def write_block(
    from_: int,
    to: int,
    amount: int,
    comment: Optional[str] = None,
):
    last_block = await _get_last_block()
    prev_block_hash = _hash_block(str(last_block))
    data = {
        "_id": last_block["_id"] + 1,
        "from": from_,
        "to": to,
        "amount": amount,
        "comment": comment,
        "prev_hash": prev_block_hash
    }
    await _save_block(data)


async def check_integrity() -> list[dict]:
    count_blocks = await _get_count_blocks()
    all_blocks = await (_get_all_blocks()).to_list(count_blocks)
    total = []
    for block in all_blocks:
        hash_ = block["prev_hash"]
        prev_block = await _get_block(block["_id"] - 1)
        actual_hash = _hash_block(str(prev_block))
        if hash_ == actual_hash:
            total.append(
                {
                    "block": block["_id"],
                    "status": "OK"
                }
            )
        else:
            total.append(
                {
                    "block": block["_id"],
                    "status": "Corrupted"
                }
            )
    return total


async def _get_count_blocks() -> int:
    """Returns count blocks of all blocks db"""

    count = await db.blocks.count_documents({})
    return count


async def _get_block(_id: int) -> dict:
    """Returns block by id"""

    block = await db.blocks.find_one({"_id": _id})
    return block


async def _get_last_block() -> dict:
    """Returns last block from all blocks db"""

    count_blocks = await _get_count_blocks()
    last_block = await _get_block(count_blocks)
    return last_block


def _get_all_blocks():
    """Returns blocks from second"""

    blocks = db.blocks.find({"_id": {"$gt": 1}})
    return blocks


async def _save_block(data: dict) -> None:
    """Save block to db"""

    await db.blocks.insert_one(data)


def _hash_block(data: str) -> str:
    """Hashing block to MD5"""

    return hashlib.md5(data.encode()).hexdigest()
