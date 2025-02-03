from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import traceback
import pandas as pd
import re
from functions import *

def get_xpath_data_to_dic(name,time):
    if dic_xpats[name][0] != "":
        for xpath in dic_xpats[name]:
            try:
                current_xpath = use_xpath(driver,xpath.format(quantity_flights=quantity_flights), time)
                dic_flight_data[quantity_flights][name] = current_xpath.text
                if dic_flight_data[quantity_flights][name] == "":
                    print('1')
                    try:
                        dic_flight_data[quantity_flights][name] = current_xpath.getAttribute("aria-label")
                    
                    except:
                        dic_flight_data[quantity_flights][name] = dic_flight_data[1][name]

                return True
            
                
            except:
                dic_flight_data[quantity_flights][name] = f"{name} not found"
        print(f"No se encontro {name} - {xpath.format(quantity_flights=quantity_flights)}")

def get_xpath_data_to_text(xpath,name,time):
    try:
        return use_xpath(driver,xpath, time).text
        
    except:
        print(f"No se encontro {name} - {xpath}")
        return f"{name} not found"
    
        

#-----------------INPUT------------------#
'''
Input the flight data with the links of the flight with the next format:
    -key: the number of the flight
    -value: a list with the next format: [origin place, destination place, link of the flight]
'''

dic_input_flight_links = {
    #1:'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tokio%20(y%20alrededores),%20Tokio%20(prefectura),%20Jap%C3%B3n,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:13/02/2025TANYT,fromType:MULTICITY,toType:AIRPORT&options=cabinclass:economy&fromDate=13/02/2025&d1=2025-2-13&passengers=adults:1,infantinlap:N',
    #2:'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Recinto%20Arena%20Ciudad%20de%20M%C3%A9xico,%20Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico,to:Tepic,%20Nayarit,%20M%C3%A9xico,departure:29/01/2025TANYT,fromType:POI,toType:CITY&options=cabinclass:economy&fromDate=29/01/2025&d1=2025-1-29&passengers=adults:1,infantinlap:N',
    #3:'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),to:Tokio,%20Jap%C3%B3n%20(TYO-Todos%20los%20aeropuertos),departure:12/02/2025TANYT,fromType:AIRPORT,toType:METROCODE&options=cabinclass:economy&fromDate=12/02/2025&d1=2025-2-12&passengers=adults:1,infantinlap:N',
    #4:'https://www.skyscanner.com.mx/transport/flights/mexa/tyoa/250307/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&rtn=0'
    5:'https://www.kayak.com.mx/flights/MEX-NRT/2025-02-14?ucs=1vhvkp2&sort=price_a'
}

#input the months that you want to search, can be in any format, numbers, short name or long name
input_dates = ["feb"]
#input_dates = ["jan"]

#----------------------------------------#

#display = Display(visible=0, size=(800, 800))  
#display.start()

#-----------------CONFIGURATION------------------#

#validating the input
validate_flight_data(dic_input_flight_links)
validate_dates(input_dates)

#init variables
links = []
dic_flight_data = {}
quantity_flights=1

dic_xpats_expedia = {
    'Class':["//button[@data-test-id='flights-cabin-class-options-toggle']//div[@class='uitk-layout-flex']/span"],
    'Origin place': ["//div[@data-test-id='typeahead-originInput']//button"],
    'Destination place': ["//div[@data-test-id='typeahead-destinationInput']//button"],
    'Parentesis place 1': ["(//div[@data-stid='secondary-section'])[{quantity_flights}]/div[2]/div"],
    'Parentesis place 2': [""],
    'Price': ["(//div[@data-test-id='price-column'])[{quantity_flights}]/div/section/span[2]", "(//div[@data-stid='price-column'])[{quantity_flights}]/div/section/span[2]"],
    'Flight time': ["(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div/span[1]"],
    'Stop over': ["(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div/span[3]"],
    'Stop over place': ["(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div[2]/div", "(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div[2]/span[1]", "(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div[2]/span[3]"],
    'Airline': ["(//div[@data-stid='secondary-section'])[{quantity_flights}]/div[3]/div"],
    'Departure time': ["(//div[@data-stid='secondary-section'])[{quantity_flights}]/div[1]/div/div/div[1]/div[1]/div"],
    'Airline 1': ["//div[@class='uitk-spacing']/div[1]/div[2]/span[2]"],
    'Airline 2': ["//div[@class='uitk-spacing']/div[2]/div[2]/span[2]"],
    'Airline 3': ["//div[@class='uitk-spacing']/div[3]/div[2]/span[2]"]
    }

dic_xpats_skyscanner = {
    'Class':["//div[contains(@class, 'SearchDetails_travellerContainer')]"],
    'Origin place': ["//div[contains(@class, 'SearchDetails_location')]/span[1]"],
    'Destination place': ["//div[contains(@class, 'SearchDetails_location')]/span[3]"],
    'Parentesis place 1': ["//div[contains(@class,'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegInfo_routePartialDepart')]/span[2]//span"],
    'Parentesis place 2': ["//div[contains(@class, 'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegInfo_routePartialArrive')]/span[2]//span"],
    'Price': ["//div[contains(@class, 'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class, 'Price_mainPriceContainer')]"],
    'Flight time': ["//div[contains(@class, 'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegInfo_stopsContainer')]/span"],
    'Stop over': ["//div[contains(@class, 'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegInfo_stopsContainer')]/div[2]/span"],
    'Stop over place': ["//div[contains(@class, 'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegInfo_stopsContainer')]/div[2]/div/span//span", "(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div[2]/span[1]", "(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div[2]/span[3]"],

    'Airline': ["//div[contains(@class,'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegLogo_legImage__NjU4O')]//img","//div[contains(@class,'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegDetails_container')]//div[contains(@class,'LogoImage_container')]/span[1]"],
    
    'Departure time': ["//div[contains(@class, 'FlightsResults_dayViewItems')]/div[{quantity_flights}]//div[contains(@class,'LegInfo_routePartialDepart')]/span[1]//span"],

    'Airline 1': ["//div[@class='uitk-spacing']/div[1]/div[2]/span[2]"],'ResultsSummary_buttonContainer__MzA5Z'
    'Airline 2': ["//div[@class='uitk-spacing']/div[2]/div[2]/span[2]"],
    'Airline 3': ["//div[@class='uitk-spacing']/div[3]/div[2]/span[2]"]
    }

dic_xpats_kayak = {
    'Class':["//div[@class='NITa NITa-cabin NITa-hide-below-m NITa-hasValue']"],
    'Origin place': ["//div[@class='NITa NITa-location-inline NITa-hide-below-s NITa-hasValue NITa-mod-multi-values']//div[@role='list']/div[1]"],
    'Destination place': ["//div[@class='NITa NITa-location-inline NITa-hasValue NITa-mod-multi-values']/div/div"],

    'Parentesis place 1': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'mod-variant-large')]//following-sibling::div/div/div[1]/span/span[2]"],
    'Parentesis place 2': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'mod-variant-large')]//following-sibling::div/div/div[2]/span/span[2]"],
    
    'Price': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'large-display')]//div[contains(@class,'price-text-container')]/div"],
    'Flight time': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'mod-full-airport')]/div[1]"],
    'Stop over': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'mod-variant-default')]/span[1]"],
    'Stop over place': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'inner')]//div[contains(@class,'mod-variant-default')]/following-sibling::div/span[1]/span"],
    'Airline': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'operator-text')]"],
    'Departure time': ["//div[contains(@class, 'result-item-container')][{quantity_flights}]//div[contains(@class,'mod-variant-large')]/span[1]"],

    'Airline 1': ["//div[@class='uitk-spacing']/div[1]/div[2]/span[2]"],'ResultsSummary_buttonContainer__MzA5Z'
    'Airline 2': ["//div[@class='uitk-spacing']/div[2]/div[2]/span[2]"],
    'Airline 3': ["//div[@class='uitk-spacing']/div[3]/div[2]/span[2]"]
    }


#generate dates
dates = generate_dates(input_dates)

#init dataframe
df = pd.DataFrame(columns=["Price", "Flight time","Stop over","Stop over place","Airline", "Departure time","Date of flight","Destination place","Origin place","Airline 1","Airline 2","Airline 3","Class","Page"])

#options for the browser
chromedriver_autoinstaller.install()# Check if the current version of chromedriver exists and if it doesn't exist, download it automatically,
ua = UserAgent()
user_agent = ua.random
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")
#chrome_options.add_argument('--user-agent="Android 4.2.1')
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.cookies": 1,
    "profile.default_content_settings.cookies": 1,
    "profile.cookie_controls_mode": 0
})
options = [
    #"--headless",  # Hides the browser window
    
    #"--window-size=1200,1200",
    "--ignore-certificate-errors",
    "--lang=es",
    "--disable-dev-shm-usage",  # Overcome limited resource problems
    "--no-sandbox",
    "--enable-javascript",
    "--allow-running-insecure-content",
    #"--disable-blink-features=AutomationControlled",
    "--disable-popup-blocking",  # Disable popup blocking
    "--disable-web-security",
    "--disable-site-isolation-trials",
    "--disable-extensions",
    #"--profile-directory=Default",
    #"--disable-plugins-discovery",
    #"--incognito",
    "--disable-infobars",
    #"--disable-notifications",
    "--disable-automation",
    "--disable-blink-features=AutomationControlled",
    "--disable-blink-features=BlockCredentialedSubresources"
    ]

for option in options:
    chrome_options.add_argument(option)

#generate the links, dates, the origin and arrival places
for i in range(len(dates)):
    for key in dic_input_flight_links:
        url,page = generate_dynamic_url(dic_input_flight_links[key],dates[i])
        links.append([url,page,dates[i]])
#----------------------------------------#


#-----------------START AUTOMATION------------------#
try:
    #initialize the driver
    driver = uc.Chrome(options=chrome_options)
    
    driver.get(links[0][0])

    for current_link,page,date in links:

        if page == "Expedia":
            dic_xpats= dic_xpats_expedia
        else:
            dic_xpats = dic_xpats_kayak
        
        quantity_flights=1
        
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

        if page == "Expedia":
            use_xpath(driver,"//li[@data-test-id='offer-listing']",180)
            time.sleep(5)
            elements = driver.find_elements(By.XPATH, "//li[@data-test-id='offer-listing']")
            elements = len(elements)
        else:
            btn = use_xpath(driver,"//div[@aria-label='El mejor']",180)
            time.sleep(5)
            btn.click()
            time.sleep(2)
            try:
                while True:
                    use_xpath(driver,"//div[contains(text(),'Ver más resultados')]",2).click()
            except:
                print("No hay mas resultados")
            elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'result-item-container')]")
            elements = len(elements) - 1
            elements = 25 if elements <=25 else elements
        #elements = driver.find_elements(By.XPATH, "//div[@data-test-id='price-column']")
        

        try:
            for i in range(elements):

                # define the dictionary with the data of the flights
                dic_flight_data[quantity_flights] = {
                    "Price": "",
                    "Flight time": "",
                    "Stop over": "",
                    'Stop over place':"",
                    "Airline": "",
                    "Departure time": "",
                    "Date of flight":date,
                    "Destination place":"",
                    "Origin place":"",
                    "Class":"",
                    "Airline 1":"",
                    "Airline 2":"",
                    "Airline 3":"",
                    "Page": page
                }

                #-----------------SCRAPPING DATA------------------#
                #-- get Origin place
                get_xpath_data_to_dic("Class", 3)

                #-- get Origin place
                get_xpath_data_to_dic("Origin place", 3)

                #-- get Destination place
                get_xpath_data_to_dic(f"Destination place", 3)

                #-- get the content of the second parentheses
                get_xpath_data_to_dic("Parentesis place 1", 3)
                get_xpath_data_to_dic("Parentesis place 2", 3)

                #-- get Price
                get_xpath_data_to_dic("Price", 1)

                #-- get Flight time
                get_xpath_data_to_dic("Flight time", 3)

                #-- get Stop over
                get_xpath_data_to_dic("Stop over", 3)

                #-- get Airline
                get_xpath_data_to_dic("Airline", 3)

                #-- get Departure time
                get_xpath_data_to_dic("Departure time", 3)



                #----------------------DATA PREPROCESSING----------------------#
                '''dic_flight_data[quantity_flights]["Origin place"] = re.sub(r'\(.*?\)', '',dic_flight_data[quantity_flights]["Origin place"]).strip()

                dic_flight_data[quantity_flights]["Destination place"] = re.sub(r'\(.*?\)', '',dic_flight_data[quantity_flights]["Destination place"]).strip()

                first,second = get_second_parentheses_content(dic_flight_data[quantity_flights]["Parentesis place 1"])
                dic_flight_data[quantity_flights]["Origin place"] = dic_flight_data[quantity_flights]["Origin place"] + " " + first
                dic_flight_data[quantity_flights]["Destination place"] = dic_flight_data[quantity_flights]["Destination place"] + " " + second

                dic_flight_data[quantity_flights]["Price"] = re.sub(r'\D', '', dic_flight_data[quantity_flights]["Price"])

                if dic_flight_data[quantity_flights]["Stop over"] == "1 escala":
                    dic_flight_data[quantity_flights]["Stop over"] = 1
                    dic_flight_data[quantity_flights]["Stop over place"] = get_xpath_data_to_text(dic_xpats['Stop over place'][0].format(quantity_flights=quantity_flights),"Stop over place", 3)

                elif dic_flight_data[quantity_flights]["Stop over"] == "2 escalas":
                    dic_flight_data[quantity_flights]["Stop over"] = 2
                    dic_flight_data[quantity_flights]["Stop over place"] = get_xpath_data_to_text(dic_xpats['Stop over place'][1].format(quantity_flights=quantity_flights),"Stop over place",3) + " and " + get_xpath_data_to_text(dic_xpats['Stop over place'][2].format(quantity_flights=quantity_flights),"Stop over place",3)

                elif dic_flight_data[quantity_flights]["Stop over"] == 'Vuelo sin escalas':
                    dic_flight_data[quantity_flights]["Stop over"] = 0
                    dic_flight_data[quantity_flights]["Stop over place"] = get_xpath_data_to_text(f"(//div[@data-stid='tertiary-section'])[{quantity_flights}]/div[2]/div","Stop over place",3)

                
                #-- get Airline 1, Airline 2, Airline 3
                #if the airline is multiple
                if "ltiples" in dic_flight_data[quantity_flights]["Airline"]:
                    
                    print("Aerolineas multiples")
                    try:
                        use_xpath(driver,f"//li[@data-test-id='offer-listing'][{quantity_flights}]", 10).click()
                        time.sleep(1)
                        use_xpath(driver,f"//span[@class='uitk-expando-title']", 10).click()
                        time.sleep(1)

                        if dic_flight_data[quantity_flights]["Stop over"] == 1:
                            get_xpath_data_to_dic("Airline 1", 3)
                            get_xpath_data_to_dic("Airline 2", 3)
                        
                        if dic_flight_data[quantity_flights]["Stop over"] == 2:
                            get_xpath_data_to_dic("Airline 1", 3)
                            get_xpath_data_to_dic("Airline 2", 3)
                            get_xpath_data_to_dic("Airline 3", 3)

                        use_xpath(driver,f"(//*[name()='svg'][@aria-label='Cerrar y volver'])[1]", 10).click()

                    except Exception as e:
                        traceback.print_exc()
                        tb = traceback.extract_tb(e.__traceback__)
                        print(f"Error occurred in line: {tb[-1].lineno}")'''
            
                #-----------------END SCRAPPING DATA------------------#
                
                quantity_flights += 1

        except Exception as e:
            # Print the error
            print("An error occurred:")
            traceback.print_exc()
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error occurred in line: {tb[-1].lineno}")

        print(f"Se encontraron {quantity_flights-1} vuelos")

        #add the data to the dataframe
        df = add_dict_to_df(dic_flight_data,df)
        #df = add_dict_to_df(dic_flight_data,df)
    #-----------------END AUTOMATION------------------#


    #-----------------OUTPUT------------------#
except Exception as e:
    # Print the error
    print("An error occurred:")
    traceback.print_exc()
    tb = traceback.extract_tb(e.__traceback__)
    print(f"Error occurred in line: {tb[-1].lineno}")

finally:
    #try:
    df = df[df['Price'] != 'Price not found']
    print(df['Departure time'])
    generate_file(df)
    '''except:
        print("Error al generar el archivo")
    print('Ending program')'''
    try:
        driver.quit()
    except:
        print("Error al cerrar el driver")
