from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from models.trade import Trade, StopTrade, Account, Position, Status
from utils.auth.auth_bearer import JWTBearer
from utils.trade_eligibility import trade_eligbility

router = APIRouter()


@router.post("/place_trade", dependencies=[Depends(JWTBearer())])
# @router.post("/place_trade")
async def place_trade(trade: Trade = Body(...)) -> Trade:
    current_user = await Account.find_one(Account.email == trade.email)

    # Yet to implement logic for authorized trading in terms of buy or sell price
    #     -> may involve removing the buy_price and sell_price parameters from the trade model and/or taking the
    #        liberty of choosing buy or sell price at the time of the trade from the users. The trade's buy or sell price
    #        will be determined by making an api call to the marketwatch api itself to get the current price of the stock
    # Verify the Trading Flow
    if current_user:
        if not trade_eligbility(trade, current_user):
            raise HTTPException(status_code=400, detail="Trade not possible")

    else:
        raise HTTPException(
            status_code=404, detail="User who issued this trade does not exist"
        )
    trade.status = "active"
    trade.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trade.trade_id = trade.email + "/" + str(trade.stock) + "/" + str(trade.timestamp)

    if current_user.holdings[trade.stock]:
        current_user.holdings[trade.stock]["shares"] += trade.quantity
        if trade.position == Position.long:
            current_user.holdings[trade.stock]["amount"] += (
                trade.buy_price * trade.quantity
            )
        else:
            current_user.holdings[trade.stock]["amount"] -= (
                trade.buy_price * trade.quantity
            )  # make sure this is how the logic for shorting a stock works...
            # create a utils module for this

    current_user.trade_history.append(trade)
    return trade


@router.post("/stop_trade", dependencies=[Depends(JWTBearer())])
# @router.post("/stop_trade")
async def stop_trade(trade_to_stop: StopTrade):
    current_user = await Account.find_one(Account.email == trade_to_stop.email)

    for trade in current_user.trade_history:
        if trade.trade_id == trade_to_stop.trade_id:
            trade.status = Status.closed
            return trade
    raise HTTPException(
        status_code=404, detail="Trade doesn't exist, check trade_id once again"
    )


# write logic for stopping trade anyway at the sell price for long position and buy price for short position
# add dependencies after testing out the endpoints
