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
import pandas as pd
import re

def use_xpath(xpath,time):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))

def random_delay(start=1, end=3):
    time.sleep(random.uniform(start, end))

def nayarit_mexico_generate_url(departure_date):
    base_url = 'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:{departure_date}TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate={departure_date}&d1={departure_date}&passengers=adults:1,infantinlap:N'
    return base_url.format(departure_date=departure_date)


dates = ["16/01/2025","17/01/2025","18/01/2025","19/01/2025"]
dates = list(set(dates))

links = []

for i in range(len(dates)):
    links.append(nayarit_mexico_generate_url(dates[i]))

#display = Display(visible=0, size=(800, 800))  
#display.start()

dict_ = {}

df = pd.DataFrame(columns=["price", "tiempo", "aerolinea", "horario","date"])


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
    "--no-sandbox",
    "--disable-popup-blocking"  # Disable popup blocking
    ]  # Bypass OS security model

for option in options:
    chrome_options.add_argument(option)

chromedriver_path = r"C:/Users/saedi/Documentos/Github/flight_prices_check/chromedriver.exe"
#driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)'''


#driver = uc.Chrome(executable_path=chromedriver_path,options=chrome_options)
try:
    driver = uc.Chrome(options=chrome_options)
    driver.get(r'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:14/01/2025TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate=14/01/2025&d1=2025-1-14&passengers=adults:1,infantinlap:N')

    date_count=-1
    for current_link in links:
        
        quantity_flights=0
        date_count+=1
        
        driver.execute_script("window.open('');")
        time.sleep(2)  # Wait for the new tab to open
        print("New tab opened")

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched to new tab")

        # Open the new URL in the new tab
        driver.get(current_link)
        print(f"Opened URL: {current_link}")

        # Close the old tab
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        print("Closed old tab")

        driver.switch_to.window(driver.window_handles[-1])
        print("Switched back to new tab")

        use_xpath("//li[@data-test-id='offer-listing']",180)
        elements = driver.find_elements(By.XPATH, "//div[@data-test-id='price-column']")

        # Get the count of elements
        count = len(elements)


        try:
            for i in range(count):

                dict_[str(quantity_flights + 1)] = {
                    "price": "",
                    "tiempo": "",
                    "aerolinea": "",
                    "horario": "",
                    "date":dates[date_count]
                }

                try:
                    price = use_xpath(f"(//div[@data-test-id='price-column'])[{quantity_flights+1}]/div/section/span[2]", 15)
                    dict_[str(quantity_flights + 1)]["price"] = re.sub(r'\D', '', price.text)
                    
                except:
                    #price = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[3]/div/section/span[2]", 15)
                    print("No se encontro el precio")
                    dict_[str(quantity_flights + 1)]["price"] = "no se encontro el precio"

                try:
                    tiempo = use_xpath(f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div/span[1]", 5)
                    dict_[str(quantity_flights + 1)]["tiempo"] = tiempo.text
                except:
                    print("No se encontro el tiempo")
                    dict_[str(quantity_flights + 1)]["tiempo"] = "no se encontro el tiempo"
                    #tiempo = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[2]/div/span[1]", 5)
                    
                try:
                    aerolinea = use_xpath(f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[3]/div", 5)
                    dict_[str(quantity_flights + 1)]["aerolinea"] = aerolinea.text
                except:
                    print("No se encontro aerolinea")
                    dict_[str(quantity_flights + 1)]["aerolinea"] = "no se encontro el aerolinea"
                    #aerolinea = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[1]/div/div/div[3]/div", 5)

                try:
                    horario = use_xpath(f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[1]/div/div/div[1]/div[1]/div", 120)
                    dict_[str(quantity_flights + 1)]["horario"] = horario.text
                except:
                    print("No se encontro horario")
                    dict_[str(quantity_flights + 1)]["horario"] = "no se encontro el horario"

                
                quantity_flights += 1

        except Exception as e:
            print(f"Se encontraron {quantity_flights} vuelos")
            print("An error occurred:")
            traceback.print_exc()
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error occurred in line: {tb[-1].lineno}")


        print(f"Se encontraron {quantity_flights} vuelos")

        #print(dict_)

        time.sleep(5)


        
        for ii in dict_:
            print(list(dict_[ii].values()))
            print(df.columns.tolist())
            temp_df = pd.DataFrame(dict_[ii], index=[0])
        # Ajusta las columnas al DataFrame principal si difieren
            temp_df = temp_df.reindex(columns=df.columns)
            df = pd.concat([df, temp_df], ignore_index=True)

    print(df)

    #xpath listings //li[@data-test-id='offer-listing']
    #path text of the listing //li[@data-test-id='offer-listing'][1]//div/button/span

    with open('./GitHub_Action_Results.txt', 'w') as f:
        f.write(f"This was written with a GitHub action {driver.title}")
    print('DONE')
finally:
    driver.quit()

# .//div[@data-test-id='price-column'][1]