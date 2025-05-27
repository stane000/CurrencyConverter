import time
import subprocess
from pywinauto import Application
import psutil
import requests

API_key = "4827627fdea1d2cf73151028ee3d6e2c"

# Step 1: Kill existing Calculator processes
for proc in psutil.process_iter(['pid', 'name']):
    if "calculator" in  str(proc.info['name']).lower():
        proc.kill()

# === 2. Get live exchange rate (RSD to EUR) ===
url = f"http://data.fixer.io/api/latest?access_key={API_key}&base=RSD&symbols=EUR"
response = requests.get(url)
response.raise_for_status()

rate = response.json().get("result")
if not rate:
    raise Exception("Could not retrieve exchange rate.")
rate = round(rate, 6)  # Precision for calculator

print(f"Live RSD → EUR rate: {rate}")

# Step 2: Launch Calculator
app = Application(backend="uia").start("calc.exe")
time.sleep(2)

# Step 3: Connect and wait
app.connect(title_re="Calculator")
calc = app.window(title_re="Calculator")
calc.wait('visible', timeout=10)

# === 4. Enter 100 * [rate] ===
expression = f"100*{rate}"
calc.type_keys(expression + "=", with_spaces=True)
time.sleep(1)


# Step 5: Read result
result_element = calc.child_window(auto_id="CalculatorResults", control_type="Text")
raw_result = result_element.window_text()

# Step 6: Clean result
clean_result = raw_result.replace("Display is", "").strip()
print(f"Result: {clean_result}")
