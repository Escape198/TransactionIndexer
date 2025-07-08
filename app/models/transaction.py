from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, index=True, nullable=False)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    value = Column(String)
    data = Column(String)
    block_number = Column(Integer)
    timestamp = Column(DateTime)
    logs = Column(JSON)
