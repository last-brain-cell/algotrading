from enum import Enum
from pydantic import BaseModel, EmailStr


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


class GetStock(BaseModel):
    email: EmailStr
    stock: Stock


class PostStock(BaseModel):
    email: EmailStr
    stock: Stock
    price: float
    change_point: float
    change_percentage: float
    total_vol: str
