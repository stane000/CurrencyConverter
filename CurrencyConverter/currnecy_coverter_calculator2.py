import time
from typing import Optional

import psutil
from pywinauto import Application

class CurrencyConverter:
    """
    A class to convert RSD to Euro or USD using the Windows Calculator app.
    Requires language settings to be set to English
    """

    calc: Optional[Application.window]

    def __init__(self):
        self.calc = None

    def _kill_existing_calculator(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if "calculator" in str(proc.info['name']).lower():
                proc.kill()

    def _start_calculator_and_prepare(self):
        self._kill_existing_calculator()
        time.sleep(1)
        app = Application(backend="uia").start("calc.exe")
        time.sleep(2)
        app.connect(best_match='Calculator')
        self.calc = app.window(best_match='Calculator')
        self.calc.wait('visible', timeout=10)
        time.sleep(0.5)

        # Switch to Currency mode
        self.calc.type_keys('%H')
        time.sleep(0.5)
        self.calc.type_keys('{DOWN 5}')
        time.sleep(0.5)
        self.calc.type_keys('{ENTER}')
        time.sleep(1)

    def _convert(self, amount: float, target_currency: str) -> str:

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
        
        if target_currency == "usd":
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
         #--------------------------------

        # Read result from Value2
        result_elem = self.calc.child_window(auto_id='Value2', control_type='Text')
        return result_elem.window_text()

    def convert_rsd_to_euro(self, amount: float) -> str:
        self._start_calculator_and_prepare()
        return self._convert(amount, 'euro')

    def convert_rsd_to_usd(self, amount: float) -> str:
        self._start_calculator_and_prepare()
        return self._convert(amount, 'usd')


# Usage
if __name__ == "__main__":
    converter = CurrencyConverter()
    print("Converted to Euro:", converter.convert_rsd_to_euro(105000))
    print("Converted to USD:", converter.convert_rsd_to_usd(105000))
