import asyncio
from decimal import Decimal

from binance import AsyncClient, BinanceSocketManager

from app.exchanges.enums import Exchange
from app.exchanges.prices_repo import prices_repo


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    async def fetch_all_symbols(self, client: AsyncClient) -> list[str]:
        exchange_info = await client.get_exchange_info()
        return [s['symbol'].lower() for s in exchange_info['symbols'] if s['status'] == 'TRADING']

    async def handle_stream(self, symbols: list[str], client: AsyncClient) -> None:
        bm = BinanceSocketManager(client)
        streams = [f'{symbol}@ticker' for symbol in symbols]

        async with bm.multiplex_socket(streams) as stream:
            while True:
                res = await stream.recv()
                data = res['data']
                symbol = data['s'].lower()
                bid = Decimal(data['b'])
                ask = Decimal(data['a'])
                price = (bid + ask) / Decimal(2)
                prices_repo.set_price(f"{Exchange.BINANCE.value}:{symbol}", price)

    async def start(self) -> None:
        client = await AsyncClient.create(api_key=self.api_key, api_secret=self.api_secret)

        symbols = await self.fetch_all_symbols(client)

        # Split symbols dynamically based on stream limit(1024)
        batches = [symbols[i:i + 1024] for i in range(0, len(symbols), 1024)]

        tasks = [self.handle_stream(batch, client) for batch in batches]

        await asyncio.gather(*tasks)

        await client.close_connection()
