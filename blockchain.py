import hashlib
import os
import json
from typing import Optional

BLOCKCHAIN_DIR = os.curdir + "/blocks/"


def main():
    check_integrity()


def write_block(
    from_: int,
    to: int,
    amount: int,
    comment: Optional[str] = None,
):
    files = _get_files()  # unsorted
    sorted_files = _sort_files(files)
    last_block = sorted_files[-1]
    prev_block_hash = _hash_block(str(last_block))
    data = {
        "from": from_,
        "to": to,
        "amount": amount,
        "comment": comment,
        "prev_hash": prev_block_hash
    }
    _save_block(str(last_block + 1), data)


def check_integrity():
    files = _get_files()  # unsorted
    sorted_files = _sort_files(files)

    total = []
    for filename in sorted_files[1::]:
        contents = _get_block(str(filename))
        hash_ = contents["prev_hash"]
        actual_hash = _hash_block(str(filename - 1))
        if hash_ == actual_hash:
            total.append(
                {
                    "block": filename - 1,
                    "status": "OK"
                }
            )
        else:
            total.append(
                {
                    "block": filename - 1,
                    "status": "Corrupted"
                }
            )
    return total


def _get_block(filename: str) -> dict:
    with open(BLOCKCHAIN_DIR + filename, "r") as file:
        contents = json.loads(file.read())
    return contents


def _save_block(filename: str, data: dict):
    """Save block to file"""
    
    with open(BLOCKCHAIN_DIR + filename, "w") as file:
        file.write(
            json.dumps(data, indent=4, ensure_ascii=False)
        )


def _hash_block(filename: str) -> str:
    """Hashing block to MD5"""

    with open(BLOCKCHAIN_DIR + filename, "rb") as file:
        hashed_block = hashlib.md5(file.read()).hexdigest()
    return hashed_block


def _get_files() -> list[str]:
    """Returns list of blocks name"""

    files = os.listdir(BLOCKCHAIN_DIR)
    return files


def _sort_files(files: list[str]) -> list[int]:
    """Sort files name"""

    files = map(lambda filename: int(filename), files)
    return sorted(files)


if __name__ == "__main__":
    main()
