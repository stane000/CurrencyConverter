from abc import ABC
from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')))
from currency_converter_file_manager import CurrencyAmount

class ICurrencyConverter(ABC):

    def convert_rsd_to_euros(self, amount: float) -> CurrencyAmount: ...
    
    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount: ...
