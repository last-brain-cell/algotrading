from fastapi import APIRouter, Depends, HTTPException
from models.trade import (
    Trade,
    Strategy,
    Order,
    OrderRequest,
    Account,
    PerformanceMetrics,
)

router = APIRouter()


@router.post("/trades")
async def create_trade(trade: Trade) -> Trade:
    saved_trade = await trade.create()
    return saved_trade


@router.post("/strategies", response_model=Strategy)
async def create_strategy(strategy: Strategy):
    saved_strategy = await strategy.create()
    return saved_strategy


@router.post("/orders/", response_model=Order)
async def create_order(order: Order):
    saved_order = await order.create()
    return saved_order


@router.post("/order-requests", response_model=OrderRequest)
async def create_order_request(order_request: OrderRequest):
    saved_order_request = await order_request.create()
    return saved_order_request


@router.post("/performance-metrics", response_model=PerformanceMetrics)
async def create_performance_metrics(metrics: PerformanceMetrics):
    saved_metrics = await metrics.create()
    return saved_metrics
