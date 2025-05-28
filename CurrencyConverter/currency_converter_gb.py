
# from time import sleep
# from playwright.sync_api import sync_playwright
# from currency_coverter_interface import CurrencyAmount, ICurrencyConverter

# class CurrencyConverterGB(ICurrencyConverter):

#     def __init__(self):
#         super().__init__()

#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False)
#         self.page = self.browser.new_page()


    
#     # Public methods
#     def covert_rsd_to_euros(self, amount: str = "100") -> CurrencyAmount:
#         return self.__convert(amount, "EUR")

#     def covert_rsd_to_usd(self, amount: str = "100") -> CurrencyAmount:
#         return self.__convert(amount, "USD")
    
#     # Private methods
#     def __convert(self, amount: str, to_currency: str) -> CurrencyAmount:

#         # open page
#         self.page.goto("https://wise.com/gb/currency-converter/")
#         sleep(2)

#         # Accept cookies if shown
#         try:
#             self.page.click("text=Accept", timeout=3000)
#         except:
#             pass
        
#         # Fill amount to convert
#         self.page.press("#amount", "Control+A")
#         self.page.press("#amount", "Backspace")
#         self.page.fill("#amount", amount)

#         # Select "From" currency
#         input_selector = 'input[placeholder="Type to search..."]'
#         self.page.click(input_selector)
#         self.page.type(input_selector, "rsd")
#         sleep(0.5)
#         self.page.press(input_selector, "Enter")
    
#         # Select "To" currency
#         to_input = 'input[aria-describedby="midmarketToCurrency-current-selection"]'
#         self.page.click(to_input)
#         self.page.type(to_input, to_currency.lower())
#         sleep(0.5)
#         self.page.press(to_input, "Enter")
        
#         # Convert
#         sleep(0.5)
#         self.page.click('button:has-text("Convert")')
        
#         # Wait for results
#         sleep(0.5)
#         output = self.page.text_content('p.sc-708e65be-1.chuBHG')
#         return CurrencyAmount.create(output)
    
#     def close(self):
#         self.page.close()
#         self.browser.close()
#         self.playwright.stop()

# # Example usage
# if __name__ == "__main__":
#     converter = CurrencyConverterGB()
#     eur_result = converter.covert_rsd_to_euros("10000")
#     print("RSD to EUR:", eur_result)

#     usd_result = converter.covert_rsd_to_usd("10000")
#     print("RSD to USD:", usd_result)

#     converter.close()


import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from playwright.async_api import async_playwright

from currency_coverter_interface import CurrencyAmount, ICurrencyConverter


class WiseCurrencyConverter(ICurrencyConverter):
    async def _convert_currency(self, amount: float, to_currency: str) -> CurrencyAmount:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://wise.com/gb/currency-converter/")

            # Accept cookies
            try:
                await page.wait_for_selector('#twcc__accept-button', timeout=5000)
                await page.click('#twcc__accept-button')
            except:
                pass

            # Input amount
            await page.wait_for_selector('#source-input')
            await page.fill('#source-input', str(amount))

            # Select RSD
            await page.click('#source-inputSelectedCurrency')
            await page.wait_for_selector('#source-inputSelectedCurrencySearch')
            await page.fill('#source-inputSelectedCurrencySearch', 'RSD')
            await page.keyboard.press('Enter')

            # Select target currency (EUR or USD)
            await page.click('#target-inputSelectedCurrency')
            await page.wait_for_selector('#target-inputSelectedCurrencySearch')
            await page.fill('#target-inputSelectedCurrencySearch', to_currency)
            await page.keyboard.press('Enter')

            # Wait for result
            await page.wait_for_timeout(2000)

            # Extract result
            result_value = await page.get_attribute('#target-input', 'value')

            await browser.close()

            return CurrencyAmount(
                amount=float(result_value.replace(",","")),
                currency=to_currency)

    async def convert_rsd_to_euros(self, amount: float) -> CurrencyAmount:
        return await self._convert_currency(amount, "EUR")

    async def convert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        return await self._convert_currency(amount, "USD")


# Example usage
async def main():
    converter = WiseCurrencyConverter()
    result_eur = await converter.convert_rsd_to_euros(1000)
    result_usd = await converter.convert_rsd_to_usd(1000)
    print(result_eur)
    print(result_usd)

asyncio.run(main())
