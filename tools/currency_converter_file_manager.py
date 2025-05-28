from dataclasses import dataclass
import os

@dataclass
class CurrencyAmount:
    amount: float
    currency: str

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

class CurrencyConverterFileManager:

    def save_to_file(self, filepath: str, currency_amount: CurrencyAmount, file_name: str = "output.txt") -> None:

        # Create 'results' folder if it doesn't exist
        os.makedirs(filepath, exist_ok=True)

        # Full path for the file inside 'results' folder
        output_path = os.path.join(filepath, file_name)

        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(f"{currency_amount}")
        except Exception as e:
            print(f"Error saving to file: {e}")

    def read_from_file(self, filepath: str) -> CurrencyAmount:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                amount_str, currency = content.split(',')
                return CurrencyAmount(float(amount_str), currency)
        except Exception as e:
            print(f"Error reading from file: {e}")
            raise
