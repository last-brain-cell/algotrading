from fastapi import APIRouter, Depends, HTTPException
from models.trade import (
    Trade,
    Account,
    Position,
)
from models.user import User

router = APIRouter()


def has_sufficient_holdings_for_short_trade(current_user, trade):
    return True


@router.post("/trades")
async def create_trade(trade: Trade) -> Trade:
    current_user = await User.find_one(User.email == trade.email)

    if current_user:
        if trade.position == Position.long:
            if current_user.balance < trade.buy_price * trade.quantity:
                raise HTTPException(status_code=400, detail="Insufficient balance")
        elif trade.position == Position.short:
            # If the user has sufficient holdings or existing short positions
            if not has_sufficient_holdings_for_short_trade(current_user, trade):
                raise HTTPException(
                    status_code=400, detail="Insufficient holdings for short trade"
                )
    else:
        raise HTTPException(
            status_code=404, detail="User who issued this trade does not exist"
        )
    saved_trade = await trade.create()

    return saved_trade
