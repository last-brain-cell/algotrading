from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from models.trade import (
    Trade,
    Account,
    Position,
)
from models.user import User
from utils.short_trade_eligibility import short_trade_eligibility

router = APIRouter()


@router.post("/place_trade")
async def place_trade(trade: Trade) -> Trade:
    current_user = await User.find_one(User.email == trade.email)

    if current_user:
        if trade.position == Position.long:
            if current_user.balance < trade.buy_price * trade.quantity:
                raise HTTPException(status_code=400, detail="Insufficient balance")
        elif trade.position == Position.short:
            # If the user has sufficient holdings or existing short positions
            if not short_trade_eligibility(trade):
                raise HTTPException(
                    status_code=400, detail="Insufficient holdings for short trade"
                )
    else:
        raise HTTPException(
            status_code=404, detail="User who issued this trade does not exist"
        )
    trade.timestamp = datetime.now()
    saved_trade = await trade.create()

    return saved_trade
