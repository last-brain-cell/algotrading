from typing import List
from beanie import Document
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class Position(Enum):
    long = "Long"
    short = "Short"


class Trade(BaseModel):
    email: EmailStr
    stock: str
    position: Position
    buy_price: float
    sell_price: float
    timestamp: datetime.timestamp()
    strategy_id: str
    quantity: int


class Account(Document):
    email: EmailStr
    balance: float
    holdings: dict
    order_history: List[Order]
    profit_loss: float
