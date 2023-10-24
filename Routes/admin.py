# get stock data without verification
# get all the user accounts data
# send P&L of all the participants for the leaderboard
# calculate the total P&L when the leaderboard data is requested and not anyway to ensure optimization
# toggle the kill-switch

from fastapi import APIRouter, Body, HTTPException, Depends
from utils.auth.auth_bearer import JWTBearer, JWTBearerAdmin

router = APIRouter()
kill_switch_enabled = False


@router.get("/admin", dependencies=[Depends(JWTBearerAdmin())])
async def admin():
    return {"admin endpoints": "work in progress"}
