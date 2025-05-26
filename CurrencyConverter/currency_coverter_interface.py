from abc import ABC
from dataclasses import dataclass
import re

@dataclass
class CurrencyAmount:
    amount: float
    currency: str

    @classmethod
    def create(cls, text: str) -> "CurrencyAmount":
        """
        Parse a string like '0.85298964 Euros' into amount and currency.
        """
        # Use regex to separate number and currency text
        match = re.match(r"([\d\.]+)\s*(\w+)", text.strip())
        if not match:
            raise ValueError(f"Cannot parse currency amount from '{text}'")
        amount_str, currency = match.groups()
        amount = float(amount_str)
        return cls(amount=amount, currency=currency)

class ICurrencyConverter(ABC):

    def covert_rsd_to_euros(self, amount: float) -> CurrencyAmount: ...
    
    def covert_rsd_to_usd(self, amount: float) -> CurrencyAmount: ...
