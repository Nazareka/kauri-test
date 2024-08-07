import json
from decimal import Decimal

import httpx
import websockets

from app.exchanges.enums import Exchange
from app.exchanges.prices_repo import prices_repo


class KrakenClient:
    WEB_SOCKET_URL: str = "wss://ws.kraken.com/v2"
    REST_URL: str = "https://api.kraken.com/0/public"
    kraken_pairs: list[str] = []

    async def fetch_pairs(self) -> None:
        response = httpx.get(f"{self.REST_URL}/AssetPairs")
        self.kraken_pairs = [pair['wsname'] for pair in response.json()['result'].values()]

    async def start(self) -> None:
        await self.fetch_pairs()

        async with websockets.connect(self.WEB_SOCKET_URL) as websocket:
            subscribe_msg = json.dumps({
                "method": "subscribe",
                "params": {
                    "channel": "ticker",
                    "symbol": self.kraken_pairs[:700] # there is error if we subscribe to all pairs at once(more than 701), probably some limitation
                }
            })
            await websocket.send(subscribe_msg)
            subscribe_msg = json.dumps({
                "method": "subscribe",
                "params": {
                    "channel": "ticker",
                    "symbol": self.kraken_pairs[700:729]
                }
            })
            await websocket.send(subscribe_msg)

            while True:
                response = await websocket.recv()
                data = json.loads(response)
                if isinstance(data, dict) and data.get('channel') == 'ticker':
                    for pair in data['data']:
                        symbol = pair['symbol'].replace('/', '').lower()
                        bid = Decimal(pair['bid'])
                        ask = Decimal(pair['ask'])
                        prices_repo.set_price(f"{Exchange.KRAKEN.value}:{symbol}", (bid + ask) / Decimal(2))