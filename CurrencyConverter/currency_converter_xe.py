
from time import sleep
from playwright.sync_api import sync_playwright
from currency_coverter_interface import CurrencyAmount, ICurrencyConverter

class CurrencyConverterXE(ICurrencyConverter):

    def __init__(self):
        super().__init__()

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto("https://www.xe.com/")

        # Accept cookies if shown
        try:
            self.page.click("text=Accept", timeout=3000)
        except:
            pass
    
    # Public methods
    def covert_rsd_to_euros(self, amount: str = "100") -> CurrencyAmount:
        return self.__convert(amount, "EUR")

    def covert_rsd_to_usd(self, amount: str = "100") -> CurrencyAmount:
        return self.__convert(amount, "USD")
    
    # Private methods
    def __convert(self, amount: str, to_currency: str) -> CurrencyAmount:

        # open page
        self.page.goto("https://www.xe.com/")
        
        # Fill amount to convert
        self.page.press("#amount", "Control+A")
        self.page.press("#amount", "Backspace")
        self.page.fill("#amount", amount)

        # Select "From" currency
        input_selector = 'input[placeholder="Type to search..."]'
        self.page.click(input_selector)
        self.page.type(input_selector, "rsd")
        sleep(0.5)
        self.page.press(input_selector, "Enter")
    
        # Select "To" currency
        to_input = 'input[aria-describedby="midmarketToCurrency-current-selection"]'
        self.page.click(to_input)
        self.page.type(to_input, to_currency.lower())
        sleep(0.5)
        self.page.press(to_input, "Enter")
        
        # Convert
        sleep(0.5)
        self.page.click('button:has-text("Convert")')
        
        # Wait for results
        sleep(0.5)
        output = self.page.text_content('p.sc-708e65be-1.chuBHG')
        return CurrencyAmount.create(output)
    
    def close(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()

# Example usage
if __name__ == "__main__":
    converter = CurrencyConverterXE()
    eur_result = converter.covert_rsd_to_euros("100")
    print("RSD to EUR:", eur_result)

    usd_result = converter.covert_rsd_to_usd("100")
    print("RSD to USD:", usd_result)

    converter.close()
    a  =4