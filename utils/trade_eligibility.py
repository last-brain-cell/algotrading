from models.trade import Trade, Account, Position


async def trade_eligbility(trade: Trade, user: Account):
    if trade.position == Position.short:
        if 0 != 0:  # false condition for a short trade
            return False
        return True
    else:
        if user.balance < trade.buy_price * trade.quantity:
            return False
        return True
