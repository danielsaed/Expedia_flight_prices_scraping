from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
import os
import time
import undetected_chromedriver as uc
import random
from fake_useragent import UserAgent
import traceback

def use_xpath(xpath,time):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))

def random_delay(start=1, end=3):
    time.sleep(random.uniform(start, end))

#display = Display(visible=0, size=(800, 800))  
#display.start()

chromedriver_autoinstaller.install()# Check if the current version of chromedriver exists
                                    # and if it doesn't exist, download it automatically,
ua = UserAgent()
user_agent = ua.random

chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")

options = [
    #"--headless",  # Hides the browser window
    "--window-size=1200,1200",
    "--ignore-certificate-errors",
    "--lang=es",
    "--disable-dev-shm-usage",  # Overcome limited resource problems
    "--no-sandbox"]  # Bypass OS security model

dict_ = {}
quantity_flights= 0

dict_[str(quantity_flights + 1)] = {
        1:0
    }

print(dict_)

driver = uc.Chrome(options=chrome_options)
driver.get(r'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:14/01/2025TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate=14/01/2025&d1=2025-1-14&passengers=adults:1,infantinlap:N')

use_xpath("//li[@data-test-id='offer-listing'][1]//div/button/span",180)

try:
    while True:

        dict_[str(quantity_flights + 1)] = {
            "price": use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[2]/div/div/section/span",random_delay(1,2)),
            "tiempo":use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[1]/div/div[2]/div",random_delay(1,2)),
            "aerolinea": use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[1]/div/div[3]/div[2]",random_delay(1,2)),
            "horario":use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]",random_delay(1,2))
        }

        quantity_flights += 1

except Exception as e:
    print(f"Se encontraron {quantity_flights} vuelos")
    print("An error occurred:")
    traceback.print_exc()

print(dict_)

time.sleep(5)

#xpath listings //li[@data-test-id='offer-listing']
#path text of the listing //li[@data-test-id='offer-listing'][1]//div/button/span

with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {driver.title}")
print('DONE')

driver.close()