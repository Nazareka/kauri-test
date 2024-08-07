from decimal import Decimal


class PricesRepo:
    _prices: dict[str, Decimal]

    def __init__(self):
        self._prices = {}

    def set_price(self, price_pair: str, new_price: Decimal) -> None:
        self._prices[price_pair] = new_price

    def get_prices(self) -> dict[str, Decimal]:
        return self._prices

prices_repo = PricesRepo()

__all__ = ['prices_repo']