import subprocess
import sys
import pytest
import os

# Define paths based on known structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_PATH = os.path.join(BASE_DIR, "CurrencyConverter", "app.py")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Parameters for testing
converters = ["calc", "web_xe", "calc2"]
amounts = [1000, 2000, 3000]
currencies = ["euro", "usd"]

@pytest.mark.parametrize("converter", converters)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_converter_app_functionality(converter, amount, currency):

    file_name = f"test_output_{converter}_{amount}_rsd_to_{currency}"
    output_file = os.path.join(RESULTS_DIR, file_name + ".txt")

    result = subprocess.run(
    [sys.executable, APP_PATH, converter, currency, str(amount), output_file],
    capture_output=True,
    text=True
    )   

    # Check for successful exit
    assert result.returncode == 0, f"Process failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Check for expected output in stdout
    assert "Conversion result:" in result.stdout, f"Missing output: {result.stdout}"

    # Check the output file was created
    assert os.path.exists(output_file), f"Missing result file: {output_file}"

    # # Optional: Clean up generated file after test
    os.remove(output_file)


# Add main method for standalone execution
def main():
    import sys
    sys.exit(pytest.main([__file__]))

if __name__ == "__main__":
    main()