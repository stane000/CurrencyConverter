
import pytest
from converter_app_test import ConverterAppTest

# Parameters for testing
converters_list = [["web_xe", 'web_gb']]
amounts = [1000, 2000, 3000]
currencies = ["euro", "usd"]

@pytest.mark.web
@pytest.mark.parametrize("converters", converters_list)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_web_gb_and_web_xe(converters: str, amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter web_xe: uses 'https://www.xe.com/'  for real-time conversion.
    Converter web_gb: uses'https://wise.com/gb/currency-converter/ for real-time conversion.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# Parameters for testing
converters_list = [["calc", "calc2"]]

@pytest.mark.calc
@pytest.mark.parametrize("converters", converters_list)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_calc_and_calc2(converters: str, amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter calculator app 1: uses Windows Calculator built in currency conversion app for conversion.
    Converter calculator app 2: uses Windows Calculator to calculate currency conversion based on exchange rate.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# Parameters for testing
converters_list = [["web_xe", "calc"]]

@pytest.mark.xe_calc
@pytest.mark.parametrize("converters", converters_list)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_xe_and_calc(converters: str, amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter web_xe: uses 'https://www.xe.com/'  for real-time conversion.
    Converter calculator app: uses Windows Calculator built in currency conversion app for conversion.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

# Parameters for testing
converters_list = [["web_xe", "calc2"]]

@pytest.mark.xe_calc2
@pytest.mark.parametrize("converters", converters_list)
@pytest.mark.parametrize("amount", amounts)
@pytest.mark.parametrize("currency", currencies)
def test_compere_currency_amounts_xe_and_calc2(converters: str, amount: str, currency: str) -> None:
    """
    Test to compare currency conversion results from different converters.

    Converter web_xe: uses 'https://www.xe.com/'  for real-time conversion.
    Converter calculator app 2: uses Windows Calculator to calculate currency conversion based on exchange rate.
    
    Parameters:
    - converters: List of converter names to test.
    - amount: Amount in RSD to convert.
    - currency: Target currency for conversion (euro or usd).
    """
    print(f"Testing converters: {converters} for amount: {amount} and currency: {currency}")
    compare_convertors_currency_conversion(converters, amount, currency)

def compare_convertors_currency_conversion(converters: str, amount: str, currency: str) -> None:

    currency_amount_and_converter = []
    for converter in converters:

        print(f"Starting converter: {converter} for amount: {amount} and currency: {currency}")
        converter_app_test = ConverterAppTest()
        output_file = converter_app_test.run_currency_converter_app(converter, amount, currency)
        converter_app_test.check_output_file_exists(output_file)
        output_file = converter_app_test.get_currency_amount_from_file(output_file)
        currency_amount_and_converter.append((converter, output_file))
    
    if len(converters) > 1:
        converter_app_test.assert_all_file_outputs(currency_amount_and_converter)


# Add main method for standalone execution
def main():
    import sys
    sys.exit(pytest.main(["-s", "-v", __file__]))

if __name__ == "__main__":
    main()