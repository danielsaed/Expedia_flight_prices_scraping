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

dict_ = {}
quantity_flights= 0



chromedriver_autoinstaller.install()# Check if the current version of chromedriver exists and if it doesn't exist, download it automatically,
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

for option in options:
    chrome_options.add_argument(option)

chromedriver_path = r"C:/Users/saedi/Documentos/Github/flight_prices_check/chromedriver.exe"
#driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)'''


#driver = uc.Chrome(executable_path=chromedriver_path,options=chrome_options)
driver = uc.Chrome(options=chrome_options)
driver.get(r'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:14/01/2025TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate=14/01/2025&d1=2025-1-14&passengers=adults:1,infantinlap:N')

use_xpath("//li[@data-test-id='offer-listing']",180)
elements = driver.find_elements(By.XPATH, "//div[@data-test-id='price-column']")

# Get the count of elements
count = len(elements)
print(count)

try:
    for i in range(count):

        try:
            price = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[3]/div/section/span[2]", 15)
        except:
            price = use_xpath(f"(//div[@data-test-id='price-column'])[{quantity_flights+1}]/div/section/span[2]", 15)

        try:
            tiempo = use_xpath(f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div/span[1]", 5)
        except:
            tiempo = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[2]/div/span[1]", 5)
            

        try:
            aerolinea = use_xpath(f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[3]/div", 5)
        except:
            aerolinea = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[1]/div/div/div[3]/div", 5)

        horario = use_xpath(f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[1]/div/div/div[1]/div[1]/div", 120)

        dict_[str(quantity_flights + 1)] = {
            "price": price.text,
            "tiempo": tiempo.text,
            "aerolinea": aerolinea.text,
            "horario": horario.text
        }

        quantity_flights += 1

except Exception as e:
    print(f"Se encontraron {quantity_flights} vuelos")
    print("An error occurred:")
    traceback.print_exc()
    tb = traceback.extract_tb(e.__traceback__)
    print(f"Error occurred in line: {tb[-1].lineno}")

print(f"Se encontraron {quantity_flights} vuelos")

print(dict_)

time.sleep(5)

#xpath listings //li[@data-test-id='offer-listing']
#path text of the listing //li[@data-test-id='offer-listing'][1]//div/button/span

with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {driver.title}")
print('DONE')

driver.close()

# .//div[@data-test-id='price-column'][1]