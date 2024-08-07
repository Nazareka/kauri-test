from contextlib import asynccontextmanager
from decimal import Decimal

from fastapi import FastAPI, Query
import asyncio

from app.exchanges.binance_client import BinanceClient
from app.exchanges.kraken_client import KrakenClient
from app.exchanges.prices_repo import prices_repo
from app.settings import settings
from app.exchanges.enums import Exchange


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(
        BinanceClient(
            api_key=settings.BINANCE_API_KEY,
            api_secret=settings.BINANCE_API_SECRET
        ).start()
    )
    asyncio.create_task(KrakenClient().start())
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/prices", response_model=dict[str, Decimal])
async def get_prices(pair: str = Query(None), exchange: Exchange = Query(None)):
    prices = prices_repo.get_prices()
    results = {}
    if pair and exchange:
        key = f"{exchange}:{pair}"
        if key in prices:
            results[key] = prices[key]
    elif exchange:
        results = {k: v for k, v in prices.items() if k.startswith(exchange)}
    elif pair:
        results = {k: v for k, v in prices.items() if k.endswith(f":{pair}")}
    else:
        results = prices
    return results
