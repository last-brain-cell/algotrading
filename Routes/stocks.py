from pydantic import EmailStr
from utils.scrape_stock import StockScraper
from fastapi import APIRouter, Depends, HTTPException, Query
from models.stock import PostStock
from models.user import User
from utils.auth.auth_bearer import JWTBearer


router = APIRouter()


@router.get("/fetch_stock_basic", dependencies=[Depends(JWTBearer())])
# @router.get("/fetch_stock_basic")
async def fetch_stock(
    email: EmailStr = Query(..., description="Email"),
    stock: str = Query(..., description="Stock"),
) -> PostStock:
    existing_user = await User.find_one(User.email == email)

    if existing_user:
        stock_data = StockScraper(stock).getPrice()
        if stock_data:
            new_stock = PostStock(
                stock=stock,
                email=email,
                price=stock_data["price"],
                change_point=stock_data["change_point"],
                change_percentage=stock_data["change_percentage"],
                total_vol=stock_data["total_vol"],
            )

            return new_stock
        raise HTTPException(
            status_code=500, detail="There was some problem with this request"
        )
    raise HTTPException(status_code=404, detail="User not found")


# implement the logic for this endpoint for getting detailed stock information
@router.get("/fetch_stock_detailed", dependencies=[Depends(JWTBearer())])
# @router.get("/fetch_stock_detailed")
async def fetch_stock(
    email: EmailStr = Query(..., description="Email"),
    stock: str = Query(..., description="Stock"),
) -> PostStock:
    existing_user = await User.find_one(User.email == email)

    if existing_user:
        stock_data = StockScraper(stock).getPrice()
        if stock_data:
            new_stock = PostStock(
                stock=stock,
                email=email,
                price=stock_data["price"],
                change_point=stock_data["change_point"],
                change_percentage=stock_data["change_percentage"],
                total_vol=stock_data["total_vol"],
            )

            return new_stock
        raise HTTPException(
            status_code=500, detail="There was some problem with this request"
        )
    raise HTTPException(status_code=404, detail="User not found")
