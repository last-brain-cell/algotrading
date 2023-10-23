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
    timestamp: datetime
    strategy_id: str
    quantity: int


class Strategy(BaseModel):
    strategy_id: str
    description: str
    parameters: dict


class Order(Document):
    email: EmailStr
    stock: str
    position: Position
    price: float
    quantity: int


class OrderRequest(BaseModel):
    email: EmailStr
    stock: str
    position: Position
    quantity: int
    price: float


class Account(Document):
    email: EmailStr
    balance: float
    holdings: dict
    order_history: List[Order]
    profit_loss: float


class PerformanceMetrics(BaseModel):
    strategy_id: str
    returns: float
    sharpe_ratio: float
    draw_down: float
