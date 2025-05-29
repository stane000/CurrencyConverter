import time

from currency_converter_calculator_base import CurrencyConverterCalculatorBase
from currency_converter_interface import CurrencyAmount

class CurrencyConverterCalculator(CurrencyConverterCalculatorBase):
    """
    A class to convert RSD to Euro or USD using the Windows Calculator app.
    Requires language settings to be set to English
    """
    
    def __init__(self) -> None:
        super().__init__()

    # Public methods
    def convert_rsd_to_euro(self, amount: float) -> CurrencyAmount:
        self._start_calculator_and_prepare()
        return self._convert_currency(amount, "EUR")

    def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        self._start_calculator_and_prepare()
        return self._convert_currency(amount, 'USD')
    
    # Private methods
    def _convert_currency(self, amount: float, target_currency: str) -> CurrencyAmount:

        # Switch to Currency mode
        self.calc.type_keys('%H')
        time.sleep(0.5)
        self.calc.type_keys('{DOWN 5}')
        time.sleep(0.5)
        self.calc.type_keys('{ENTER}')
        time.sleep(1)

        # Enter amount
        self.calc.type_keys(str(int(amount)))
        time.sleep(0.5)
        
        # Set covert from
        self.calc.type_keys('{TAB}')
        time.sleep(0.5)

        self.calc.type_keys('{ENTER}')
        time.sleep(0.5)

        self.calc.type_keys('ser')
        time.sleep(0.5)

        self.calc.type_keys('{ENTER}')
        time.sleep(1)
        #--------------------------------
        
        # Set convert to
        self.calc.type_keys('{TAB}')
        time.sleep(0.5)
        self.calc.type_keys('{TAB}')
        time.sleep(0.5)

        self.calc.type_keys('{ENTER}')
        time.sleep(0.5)
        
        if target_currency.upper() == "USD":
            result_elem = "" 
            timeout = 30
            start_time = time.time()
            while "United States Dollar" not in result_elem:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Timeout while waiting for 'United States Dollar' to appear.")
                self.calc.type_keys("united")
                time.sleep(0.5)
                self.calc.type_keys('{ENTER}')
                time.sleep(0.5)
                result_elem = self.calc.child_window(auto_id='Value2', control_type='Text').window_text()
                self.calc.type_keys('{ENTER}')
                time.sleep(0.5)
            
        else:
            self.calc.type_keys(target_currency)
            time.sleep(0.5)

        self.calc.type_keys('{ENTER}')
        time.sleep(0.5)

        # Read result from Value2
        result_elem = self.calc.child_window(auto_id='Value2', control_type='Text')
        result_text = result_elem.window_text().split(" ")[2].replace(",", "")
        return CurrencyAmount(float(result_text), target_currency.upper())
    
# Usage
if __name__ == "__main__":
    converter = CurrencyConverterCalculator()
    #print("Converted to Euro:", converter.convert_rsd_to_euro(105000))
    print("Converted to USD:", converter.convert_rsd_to_usd(105000))
