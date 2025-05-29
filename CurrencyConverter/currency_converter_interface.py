
import os
import sys
from abc import ABC, abstractmethod

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')))
from currency_converter_file_manager import CurrencyAmount

class ICurrencyConverter(ABC):
    
    @abstractmethod
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount: ...
    
    @abstractmethod
    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount: ...
