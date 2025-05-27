
from typing import Optional
import psutil
import requests
from pywinauto import Application
import time

from currency_coverter_interface import CurrencyAmount

class CurrencyConverterCalculator:
    """
    A currency converter that uses the Windows Calculator to perform currency conversions
    from Serbian Dinar (RSD) to Euro (EUR) and US Dollar (USD).

    This class fetches the latest exchange rates from a reliable API and utilizes the
    Windows Calculator application to compute the converted amounts. It ensures that
    the Calculator is properly managed by opening it for each calculation and closing
    it afterward to prevent resource leaks.
    """

    app: Optional[Application]

    def __init__(self): 
        self.app = None
    
    # Public methods
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount:
        return self._convert(amount, 'EUR')

    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        return self._convert(amount, 'USD')

    # Private methods
    def _get_exchange_rate(self, currency: str = 'EUR') -> float:
        """
        Fetches the latest RSD to EUR exchange rate from a reliable API.
        """
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/RSD")
            data = response.json()
            rate = data['rates'][currency]
            return rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def _convert(self, amount_rsd, currency: str):
        """
        Opens the Windows Calculator in Standard mode, inputs the multiplication expression,
        and retrieves the result.
        """
        rate = self._get_exchange_rate(currency)
        try:
 
            self._kill_existing_calculator()
            time.sleep(1)
            self.app = Application(backend="uia").start("calc.exe")
            time.sleep(2)
            self.app.connect(best_match='Calculator')
            calc = self.app.window(best_match='Calculator')
            calc.wait('visible', timeout=10)
            time.sleep(0.5)

            # Switch to Standard mode using Alt+1
            calc.type_keys('%1')
            time.sleep(0.5)

            # Clear any previous input
            calc.type_keys('{ESC}')
            time.sleep(0.5)

            calc.type_keys(f"{amount_rsd}")

            # Press multiplication operator
            calc.type_keys('*')
            time.sleep(0.1)

            calc.type_keys(f"{str(rate).replace('.', ',')}")  # Replace dot with comma for correct decimal format

            # Press Enter to get the result
            calc.type_keys('{ENTER}')
            time.sleep(1)  # Wait for the result to appear

            # Retrieve the result from the Calculator's display
            result_element = calc.child_window(auto_id='CalculatorResults', control_type='Text')
            result_text = result_element.window_text()
            return CurrencyAmount(amount=float(result_text.replace(",", ".").split(" ")[-1]), currency=currency)
        except Exception as e:
            print(f"Error interacting with Calculator: {e}")
            return None
        finally:
            self._close_calculator()
        
    def _kill_existing_calculator(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if "calculator" in str(proc.info['name']).lower():
                proc.kill()

    def _close_calculator(self):
        if self.app:
            try:
                self.app.kill()
                self.app = None
            except Exception as e:
                print(f"Error closing Calculator: {e}")

    
if __name__ == "__main__":
    converter = CurrencyConverterCalculator()
    
    # Example usage
    amount_rsd = 1000  # Amount in RSD
    euro_result = converter.convert_rsd_to_euro(amount_rsd)
    usd_result = converter.convert_rsd_to_usd(amount_rsd)
    
    print(f"{amount_rsd} RSD is equivalent to {euro_result} EUR")
    print(f"{amount_rsd} RSD is equivalent to {usd_result} USD")