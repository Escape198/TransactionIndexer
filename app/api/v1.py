from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.core.db import get_db
from app.services.indexer import TransactionIndexerService
from app.services.transaction_service import TransactionQueryService
from app.schemas.transaction import TransactionSchema


router = APIRouter()


@router.post("/index/{address}")
def index_address(
    address: str,
    start_block: int,
    end_block: int,
    db: Session = Depends(get_db),
):
    service = TransactionIndexerService(db)
    count = service.index_address(address, start_block, end_block)
    return {"indexed": count}


@router.get("/transactions/{address}", response_model=List[TransactionSchema])
def list_transactions(
    address: str,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    min_value: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    service = TransactionQueryService(db)
    return service.get_transactions(address, start_date, end_date, min_value)


@router.delete("/transactions/{address}")
def delete_transactions(
    address: str,
    start_block: Optional[int] = Query(None),
    end_block: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    service = TransactionQueryService(db)
    deleted = service.delete_transactions(address, start_block, end_block)
    return {"deleted": deleted}


@router.get("/stats/{address}")
def get_stats(
    address: str,
    db: Session = Depends(get_db),
):
    service = TransactionQueryService(db)
    return service.get_stats(address)
