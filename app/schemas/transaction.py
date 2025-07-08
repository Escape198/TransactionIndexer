from pydantic import BaseModel
from datetime import datetime
from typing import Any


class TransactionSchema(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: str
    block_number: int
    timestamp: datetime
    logs: Any

    class Config:
        orm_mode = True
