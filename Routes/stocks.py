from utils.scrape_stock import Scrapy
from fastapi import APIRouter, Depends, HTTPException, Body
from models.stock import Stock, GetStock, PostStock


router = APIRouter()


async def get_stock_price(stock: str):
    stock_data = await Scrapy(stock).getPrice()
    if stock_data:
        return stock_data
    else:
        return None


@router.get("/stock")
async def get_stock(stock: GetStock = Body(...)) -> PostStock:
    fetch_stock = await get_stock_price(str(stock.stock))
    if fetch_stock is not None:
        new_stock = PostStock()
        new_stock.stock = get_stock.stock
        new_stock.email = get_stock.email
        new_stock.price = new_stock.price
        new_stock.change_point = new_stock.change_point
        new_stock.change_percentage = new_stock.change_percentage
        new_stock.total_vol = new_stock.total_vol
        return new_stock
