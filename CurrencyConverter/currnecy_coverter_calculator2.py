import time
import subprocess
from pywinauto import Application
import psutil
import requests

# API_key = "4827627fdea1d2cf73151028ee3d6e2c"

# # Step 1: Kill existing Calculator processes
# for proc in psutil.process_iter(['pid', 'name']):
#     if "calculator" in  str(proc.info['name']).lower():
#         proc.kill()

# # Step 2: Launch Calculator
# app = Application(backend="uia").start("calc.exe")
# time.sleep(2)

# # Step 3: Connect and wait
# app.connect(title_re="Calculator")
# calc = app.window(title_re="Calculator")
# calc.wait('visible', timeout=10)

# #--------------------------------------
# # Optional: Ensure it's in Currency mode (Alt+H > Down 5 > Enter)
# calc.type_keys('%H')      # Open menu (Alt+H)
# time.sleep(0.5)
# calc.type_keys('{DOWN 5}')  # Go to 'Currency'
# time.sleep(0.5)
# calc.type_keys('{ENTER}')   # Enter Currency mode
# time.sleep(1)

# # Enter 100
# calc.type_keys('105000')
# time.sleep(0.5)


# calc.type_keys('{TAB}')
# time.sleep(0.5)

# calc.type_keys('{ENTER}')   # Enter Currency mode
# time.sleep(0.5)

# calc.type_keys('ser')
# time.sleep(0.5)


# calc.type_keys('{ENTER}')   # Enter Currency mode
# time.sleep(1)

# calc.type_keys('{TAB}')
# time.sleep(0.5)
# calc.type_keys('{TAB}')
# time.sleep(0.5)

# calc.type_keys('{ENTER}')   # Enter Currency mode
# time.sleep(0.5)

# calc.type_keys('euro')
# time.sleep(0.5)


# calc.type_keys('{ENTER}')   # Enter Currency mode
# time.sleep(0.5)



# # Access the element with automation_id 'Value2'
# result_elem = calc.child_window(auto_id='Value2', control_type='Text')

# # Get the displayed converted currency value
# result_text = result_elem.window_text()
# print("Converted currency value:", result_text)

import time
import psutil
from pywinauto import Application

class CurrencyConverter:
    def __init__(self):
        self.app = None
        self.calc = None
       # self._start_calculator_and_prepare()

    def _kill_existing_calculator(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if "calculator" in str(proc.info['name']).lower():
                proc.kill()

    def _start_calculator_and_prepare(self):
        self._kill_existing_calculator()
        time.sleep(1)
        self.app = Application(backend="uia").start("calc.exe")
        time.sleep(2)
        self.app.connect(title_re="Calculator")
        self.calc = self.app.window(title_re="Calculator")
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
            while "United States Dolla3r" not in result_elem or time.time() - start_time < timeout:
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
   # print("Converted to Euro:", converter.convert_rsd_to_euro(105000))
    print("Converted to USD:", converter.convert_rsd_to_usd(105000))
