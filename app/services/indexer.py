from web3 import Web3
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.models.transaction import Transaction



w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))


def convert_hexbytes(obj):
    if isinstance(obj, list):
        return [convert_hexbytes(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_hexbytes(v) for k, v in obj.items()}
    elif hasattr(obj, 'hex'):
        return obj.hex()
    else:
        return obj


class TransactionIndexerService:
    def __init__(self, db: Session):
        self.db = db

    def bulk_upsert_transactions(self, transactions: list[dict]):
        stmt = insert(Transaction).values(transactions)
        stmt = stmt.on_conflict_do_nothing(index_elements=["hash"])
        self.db.execute(stmt)
        self.db.commit()

    def index_address(
        self,
        address: str,
        start_block: int,
        end_block: int,
    ) -> list:

        batch = []
        for block_num in range(start_block, end_block + 1):
            block = w3.eth.get_block(block_num, full_transactions=True)
            for tx in block["transactions"]:
                if tx["from"].lower() == address.lower() or (tx["to"] and tx["to"].lower() == address.lower()):
                    receipt = w3.eth.get_transaction_receipt(tx["hash"])
                    batch.append({
                        "hash": tx["hash"].hex(),
                        "from_address": tx["from"],
                        "to_address": tx["to"],
                        "value": str(tx["value"]),
                        "data": tx["input"].hex() if hasattr(tx["input"], "hex") else tx["input"],
                        "block_number": tx["blockNumber"],
                        "timestamp": datetime.fromtimestamp(block.timestamp),
                        "logs": convert_hexbytes([dict(log) for log in receipt.logs])
                    })

        self.bulk_upsert_transactions(batch)
        return batch
