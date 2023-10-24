from typing import List
from beanie import Document
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class Position(Enum):
    long = "Long"
    short = "Short"


class Stock(Enum):
    AAPL = "AAPL"  # Apple Inc.
    MSFT = "MSFT"  # Microsoft Corporation
    GOOGL = "GOOGL"  # Alphabet Inc. (Google)
    AMZN = "AMZN"  # Amazon.com Inc.
    FB = "FB"  # Facebook Inc.
    TSLA = "TSLA"  # Tesla Inc.
    NFLX = "NFLX"  # Netflix Inc.
    NVDA = "NVDA"  # NVIDIA Corporation
    IBM = "IBM"  # International Business Machines Corporation


class Status(Enum):
    open = "open"
    closed = "closed"


class Trade(BaseModel):
    trade_id: str
    email: EmailStr
    stock: Stock
    position: Position
    buy_price: float
    sell_price: float
    timestamp: datetime
    quantity: int
    status: Status


class StopTrade(BaseModel):
    email: EmailStr
    trade_id: str


class Account(Document):
    email: EmailStr
    balance: float
    holdings: dict
    trade_history: List[Trade]
    profit_loss: float
