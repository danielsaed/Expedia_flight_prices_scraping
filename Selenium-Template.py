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
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from datetime import datetime, timedelta
import calendar

def use_xpath(xpath,time):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))

def random_delay(start=1, end=3):
    time.sleep(random.uniform(start, end))

def nayarit_mexico_generate_url(departure_date):
    base_url = 'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:{departure_date}TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate={departure_date}&d1={departure_date}&passengers=adults:1,infantinlap:N'
    
    return base_url.format(departure_date=departure_date)


def generate_dynamic_url(base_url, new_departure_date):
    # Parse the URL
    url_parts = urlparse(base_url)
    query_params = parse_qs(url_parts.query)
    
    # Convert new_departure_date to different formats
    new_departure_date_slash = new_departure_date.replace('-', '/')
    new_departure_date_dash = new_departure_date
    
    # Update the departure date in the query parameters
    for key in query_params:
        query_params[key] = [re.sub(r'\d{2}/\d{2}/\d{4}', new_departure_date_slash, param) for param in query_params[key]]
        query_params[key] = [re.sub(r'\d{4}-\d{2}-\d{2}', new_departure_date_dash, param) for param in query_params[key]]
    
    # Reconstruct the URL with updated query parameters
    updated_query = urlencode(query_params, doseq=True)
    updated_url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path, url_parts.params, updated_query, url_parts.fragment))
    
    return updated_url
#llllllll = 'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Recinto%20Arena%20Ciudad%20de%20M%C3%A9xico,%20Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico,to:Tepic,%20Nayarit,%20M%C3%A9xico,departure:29/01/2025TANYT,fromType:POI,toType:CITY&options=cabinclass:economy&fromDate=29/01/2025&d1=2025-1-29&passengers=adults:1,infantinlap:N'
def generate_dates(months):
    # Fecha actual
    today = datetime.today()
    
    # Diccionario para mapear nombres y abreviaturas de meses a números
    month_map = {
        'january': 1, 'jan': 1, '01': 1, '1': 1,
        'february': 2, 'feb': 2, '02': 2, '2': 2,
        'march': 3, 'mar': 3, '03': 3, '3': 3,
        'april': 4, 'apr': 4, '04': 4, '4': 4,
        'may': 5, '05': 5, '5': 5,
        'june': 6, 'jun': 6, '06': 6, '6': 6,
        'july': 7, 'jul': 7, '07': 7, '7': 7,
        'august': 8, 'aug': 8, '08': 8, '8': 8,
        'september': 9, 'sep': 9, '09': 9, '9': 9,
        'october': 10, 'oct': 10, '10': 10,
        'november': 11, 'nov': 11, '11': 11,
        'december': 12, 'dec': 12, '12': 12
    }
    
    # Lista para almacenar las fechas generadas
    dates = []
    
    # Iterar sobre la lista de meses de entrada
    for month in months:
        month_str = str(month).strip().lower()
        if month_str in month_map:
            month_num = month_map[month_str]
            year = today.year
            
            # Generar fechas para cada día del mes especificado
            for day in range(1, calendar.monthrange(year, month_num)[1] + 1):
                date = datetime(year, month_num, day)
                if date >= today:
                    dates.append(date.strftime("%d/%m/%Y"))
    
    return dates

dates = generate_dates([1])

raw_links = {
    'cdmx':'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:14/01/2025TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate=14/01/2025&d1=2025-1-14&passengers=adults:1,infantinlap:N',
    'tepic':'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Recinto%20Arena%20Ciudad%20de%20M%C3%A9xico,%20Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico,to:Tepic,%20Nayarit,%20M%C3%A9xico,departure:29/01/2025TANYT,fromType:POI,toType:CITY&options=cabinclass:economy&fromDate=29/01/2025&d1=2025-1-29&passengers=adults:1,infantinlap:N'
}
links = []

for i in range(len(dates)):
    for key in raw_links:
        links.append([generate_dynamic_url(raw_links[key],dates[i]),dates[i],key])

#display = Display(visible=0, size=(800, 800))  
#display.start()

dict_ = {}

df = pd.DataFrame(columns=["price", "tiempo", "aerolinea", "horario","date","place"])


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

    for current_link,date,place in links:
        
        quantity_flights=0
        
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
                    "date":date,
                    "place":place
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
    df.to_csv("Output_data.csv", index=False)

    print('DONE')
finally:
    driver.quit()

# .//div[@data-test-id='price-column'][1]