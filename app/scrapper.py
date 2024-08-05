import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.constants import BCV_URL
from app.exceptions import CurrencyNotFoundException
from app.models import SingletonMeta

log = logging.getLogger(__name__)


@dataclass
class Scrapper:
    url: str

    def __post_init__(self):
        self.update_soup()

    def update_soup(self):
        response = requests.get(self.url)
        assert response.status_code == 200, "Failed to get {}".format(self.url)
        self.soup = BeautifulSoup(response.content, "html.parser")


@dataclass
class BCVScrapper(Scrapper, metaclass=SingletonMeta):
    cache: Optional[dict] = field(default_factory=dict)
    last_update: Optional[datetime] = None

    def __init__(self, *args, **kwargs):
        self.url = BCV_URL
        self.cache = defaultdict(lambda: "Not found in cache")
        self.last_update = datetime.min
        super().__init__(url=self.url)

    def __process_currency(self, currency: str):
        text_currency = currency.strip()
        text = text_currency.replace(",", ".")
        decimal_number = Decimal(text)
        return decimal_number.quantize(
            Decimal("0.001"), rounding=ROUND_HALF_EVEN
        )

    def __get_currency_by_id(self, currency):
        currency = self.soup.find(id=currency)
        if not currency:
            raise CurrencyNotFoundException(f"Currency {currency} not found")
        currency = currency.strong.get_text()  # type: ignore
        return self.__process_currency(currency)

    def get_dollar_price(self):
        now = datetime.now()
        if (
            self.last_update.date() != now.date()
            or (
                self.last_update.hour == 9
                and self.last_update.minute >= 30
                and now.hour >= 9
                and now.minute >= 30
            )
            or (
                self.last_update.hour == 13
                and self.last_update.minute >= 30
                and now.hour >= 13
                and now.minute >= 30
            )
        ):
            self.update_soup()
            log.info("Updating cache")
            self.cache["dollar"] = self.__get_currency_by_id("dolar")
            self.last_update = now
        return self.cache["dollar"]
