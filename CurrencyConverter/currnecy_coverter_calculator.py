from abc import ABC, abstractmethod
from dataclasses import dataclass
import subprocess
from currency_coverter_interface import CurrencyAmount, ICurrencyConverter
from pywinauto.application import Application
from time import sleep
import pyautogui
import time
import os


#pictures_folder = r'C:\Users\stank\Desktop\projects\CurrencyConverter\CurrencyConverter'
pictures_folder = r'C:\Users\istankovic\Desktop\me\Assignment_Project\CurrencyConverter\CurrencyConverter'

class PywinautoCurrencyConverter(ICurrencyConverter):
    def __init__(self):
        super().__init__()
        # self.app = Application(backend="uia").start("calc.exe")
        # time.sleep(2)  # Wait for the application to start
        
        # Step 1: Open the Calculator using subprocess
        subprocess.Popen('calc.exe')

        sleep(2)
        # Use Win + Up to maximize
        pyautogui.hotkey('win', 'up')
            

    def covert_rsd_to_euros(self, amount: float) -> CurrencyAmount:
        return self.__convert(amount, "EUR")

    def covert_rsd_to_usd(self, amount: float) -> CurrencyAmount:
        return self.__convert(amount, "USD")

    def __convert(self, amount: float, to_currency: str) -> CurrencyAmount:

        #  Pres the menu button
        self.__click_button_by_image(["menu-black.png", "menu-white.png"])

        # Press on the Currency
        self.__click_button_by_image(["currency.png"])

        # Press volute from
        self.__click_button_by_image(["volute-from.png"], position="bottom")

        time.sleep(2)
        pyautogui.write("SRD", interval=0.1)  # Types S, then R, then D

        # Press on the SRD
        self.__click_button_by_image(["srd.png"])

        # Press volute to
        self.__click_button_by_image(["volute-to.png"], position="bottom")

        time.sleep(2)
        pyautogui.write("euro", interval=0.1)  

        # Press on the SRD
        self.__click_button_by_image(["euro.png"])

        time.sleep(2)
        pyautogui.write(str(amount), interval=0.1)  # Types S, then R, then D

    
    def __click_button_by_image(self, images: list[str], position: str= "center", confidence: float = 0.):
        """
        Clicks a button on the screen by matching its image.
        :param images: List of image paths to search for.
        :param confidence: Confidence level for image matching (0.0 to 1.0).
        """
        for image in images:
            try:
                button_location = pyautogui.locateOnScreen(os.path.join(pictures_folder,image), confidence=confidence, region=(1920, 0, 1920, 1080))

                if button_location:

                    if position == "center":
                        x, y = pyautogui.center(button_location)
                    elif position == "bottom":
                        x, y, width, height = button_location
                        x = x + width // 2
                        y = y + height - 5  # 5 pixels above the exact bottom edge
                    else:
                        raise ValueError("Invalid position argument. Use 'center' or 'bottom'.")

                    pyautogui.click(x, y)
                    print(f"Clicked on {image} at ({x}, {y})")
                    sleep(1)  # Wait for the click to register
                    return True
            except:
                continue
        print("No button found on screen.")
        raise ValueError(f"Button not found on screen.", {str(images)})



if __name__ == "__main__":
    converter = PywinautoCurrencyConverter()
    converter.covert_rsd_to_euros(100)

