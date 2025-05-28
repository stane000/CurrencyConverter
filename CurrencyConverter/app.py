import argparse
import os
import sys

from currency_converter_interface import ICurrencyConverter
from currency_converter_calculator import CurrencyConverterCalculator
from currency_converter_calculator_v2 import CurrencyConverterCalculatorV2
from currency_converter_gb import CurrencyConverterGB
from currency_converter_xe import CurrencyConverterXE

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools')))
from currency_converter_file_manager import CurrencyConverterFileManager

def positive_float(value):
    f = float(value)
    if f <= 0:
        raise argparse.ArgumentTypeError(f"Amount must be a positive number, got {value}")
    return f

def main():
    parser = argparse.ArgumentParser(description="Currency Converter CLI")
    parser.add_argument('converter', type=str, choices=['web_xe', 'web_gb', 'calc', 'calc2'], help='Converter to use')
    parser.add_argument('currency', type=str, choices=['euro', 'usd'], help='Target currency')
    parser.add_argument('amount', type=positive_float, help='Amount in RSD to convert')
    parser.add_argument('file_name', type=str, help='File output name to save the result')

    try:
        args = parser.parse_args()

        output_file =  args.file_name + '.txt' if not args.file_name.lower().endswith('.txt') else args.file_name

        converter: ICurrencyConverter = None

        if args.converter == "web_xe":
            converter = CurrencyConverterXE()
        elif args.converter == "web_gb":
            converter = CurrencyConverterGB()  
        elif args.converter == "calc":
            converter = CurrencyConverterCalculator()
        elif args.converter == "calc2":
            converter = CurrencyConverterCalculatorV2()       

        if args.currency == 'euro':
            currency_amount = converter.covert_rsd_to_euros(args.amount)
        else:
            currency_amount = converter.convert_rsd_to_usd(args.amount)

    except Exception as ex:
        print(f"Error: {ex}")
    else:
        print(f"Conversion result: {currency_amount}")
        CurrencyConverterFileManager().save_to_file(os.path.join(os.getcwd() , "results"), currency_amount, output_file)

if __name__ == "__main__":
    main()
