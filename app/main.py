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



#-----------------INPUT------------------#
'''
Input the flight data with the links of the flight with the next format:
    -key: the number of the flight
    -value: a list with the next format: [origin place, destination place, link of the flight]
'''
dic_input_flight_links = {
    #1:['Tepic','Ciudad de México','https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tepic,%20Nayarit,%20M%C3%A9xico,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:14/01/2025TANYT,fromType:CITY,toType:AIRPORT&options=cabinclass:economy&fromDate=14/01/2025&d1=2025-1-14&passengers=adults:1,infantinlap:N'],
    #2:['Ciudad de México','Tepic','https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Recinto%20Arena%20Ciudad%20de%20M%C3%A9xico,%20Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico,to:Tepic,%20Nayarit,%20M%C3%A9xico,departure:29/01/2025TANYT,fromType:POI,toType:CITY&options=cabinclass:economy&fromDate=29/01/2025&d1=2025-1-29&passengers=adults:1,infantinlap:N'],
    3:'https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),to:Tokio,%20Jap%C3%B3n%20(TYO-Todos%20los%20aeropuertos),departure:12/02/2025TANYT,fromType:AIRPORT,toType:METROCODE&options=cabinclass:economy&fromDate=12/02/2025&d1=2025-2-12&passengers=adults:1,infantinlap:N'
}

#input the months that you want to search, can be in any format, numbers, short name or long name
#input_dates = ["jan","feb",'03']
input_dates = ["jan"]

#----------------------------------------#

#display = Display(visible=0, size=(800, 800))  
#display.start()


#-----------------CONFIGURATION------------------#

#validating the input
validate_flight_data(dic_input_flight_links)
validate_dates(input_dates)


#init variables
links = []
dict_ = {}

#generate dates
dates = generate_dates(input_dates)

#init dataframe
df = pd.DataFrame(columns=["Price", "Flight time","Stop over","Stop over place","Airline", "Departure time","Date of flight","Destination place","Origin place","Airline 1","Airline 2","Airline 3"])

#options for the browser
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
    ]

for option in options:
    chrome_options.add_argument(option)

#generate the links, dates, the origin and arrival places
for i in range(len(dates)):
    for key in dic_input_flight_links:
        links.append([generate_dynamic_url(dic_input_flight_links[key][2],dates[i]),dates[i]])
#----------------------------------------#




#-----------------START AUTOMATION------------------#
try:
    #initialize the driver
    driver = uc.Chrome(options=chrome_options)
    driver.get(links[0][0])

    for current_link,date in links:
        
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

        use_xpath(driver,"//li[@data-test-id='offer-listing']",180)
        time.sleep(5)
        #elements = driver.find_elements(By.XPATH, "//div[@data-test-id='price-column']")
        elements = driver.find_elements(By.XPATH, "//li[@data-test-id='offer-listing']")

        # Get the count of elements
        count = len(elements)


        try:
            for i in range(count):

                # define the dictionary with the data of the flights
                dict_[str(quantity_flights + 1)] = {
                    "Price": "",
                    "Flight time": "",
                    "Stop over": "",
                    'Stop over place':"",
                    "Airline": "",
                    "Departure time": "",
                    "Date of flight":date,
                    "Destination place":"",
                    "Origin place":"",
                    "Airline 1":"",
                    "Airline 2":"",
                    "Airline 3":""
                }
                # airline //div[@class='uitk-spacing']/div[-]/div[2]/span[2]
                # expand details //span[@class='uitk-expando-title']
                # click //li[@data-test-id='offer-listing'][-]
                # (//*[name()='svg'][@aria-label='Cerrar y volver'])[1]

                # button origin //div[@data-test-id='typeahead-originInput']//button
                # button destination //div[@data-test-id='typeahead-destinationInput']//button

                #-----------------SCRAPPING DATA------------------#
                try:
                    origin = use_xpath(driver,f"//div[@data-test-id='typeahead-originInput']//button", 60)
                    dict_[str(quantity_flights + 1)]["Origin place"] = re.sub(r'\(.*?\)', '', origin.text).strip()
                except:
                    print("No se encontro el tiempo")
                    dict_[str(quantity_flights + 1)]["Origin place"] ="Origin place not found"
                
                try:
                    arrival = use_xpath(driver,f"//div[@data-test-id='typeahead-destinationInput']//button", 60)
                    dict_[str(quantity_flights + 1)]["Destination place"] = re.sub(r'\(.*?\)', '', arrival.text).strip()
                except:
                    print("No se encontro el tiempo")
                    dict_[str(quantity_flights + 1)]["Destination place"] = "Destination place not found"

                try:
                    places = use_xpath(driver,f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[2]/div", 5)
                    first,second = get_second_parentheses_content(places.text)
                    dict_[str(quantity_flights + 1)]["Origin place"] = dict_[str(quantity_flights + 1)]["Origin place"] + " " + first
                    dict_[str(quantity_flights + 1)]["Destination place"] = dict_[str(quantity_flights + 1)]["Destination place"] + " " + second
                except:
                    print("No se encontro parentesis")

                try:
                    price = use_xpath(driver,f"(//div[@data-test-id='price-column'])[{quantity_flights+1}]/div/section/span[2]", 3)#data-stid
                    dict_[str(quantity_flights + 1)]["Price"] = re.sub(r'\D', '', price.text)
                    
                except:
                    try:
                        price = use_xpath(driver,f"(//div[@data-stid='price-column'])[{quantity_flights+1}]/div/section/span[2]", 5)#data-stid
                        dict_[str(quantity_flights + 1)]["Price"] = re.sub(r'\D', '', price.text)
                    except:
                        print("No se encontro el Price")
                        print("No se encontro el Price")
                        dict_[str(quantity_flights + 1)]["Price"] = "Price not found"

                try:
                    flight_time = use_xpath(driver,f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div/span[1]", 5)
                    dict_[str(quantity_flights + 1)]["Flight time"] = flight_time.text
                except:
                    print("No se encontro el tiempo")
                    dict_[str(quantity_flights + 1)]["Flight time"] = "Flight time not found"
                try:
                    stop_over = use_xpath(driver,f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div/span[3]", 5)
                    if stop_over.text == "1 escala":
                        dict_[str(quantity_flights + 1)]["Stop over"] = 1
                    elif stop_over.text == "2 escalas":
                        dict_[str(quantity_flights + 1)]["Stop over"] = 2
                    elif stop_over.text == 'Vuelo sin escalas':
                        dict_[str(quantity_flights + 1)]["Stop over"] = 0
                except:
                    print("Stop over not found")
                    dict_[str(quantity_flights + 1)]["Stop over"] = "no se encontro escala"
                try:

                    if dict_[str(quantity_flights + 1)]["Stop over"] == "2 escalas":
                        stop_over_place = use_xpath(driver,f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div[2]/span[1]", 1)
                        dict_[str(quantity_flights + 1)]["Stop over place"] = stop_over_place.text
                        stop_over_place = use_xpath(driver,f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div[2]/span[3]", 1)
                        dict_[str(quantity_flights + 1)]["Stop over place"] = dict_[str(quantity_flights + 1)]["Stop over place"] +" and "+ stop_over_place.text
                    else:

                        stop_over_place = use_xpath(driver,f"(//div[@data-stid='tertiary-section'])[{quantity_flights+1}]/div[2]/div", 1)
                        dict_[str(quantity_flights + 1)]["Stop over place"] = stop_over_place.text
                except:
                    print("Stop over place not found")
                    dict_[str(quantity_flights + 1)]["Stop over place"] = "Stop over place not found"
                    
                try:
                    airline = use_xpath(driver,f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[3]/div", 5)
                    dict_[str(quantity_flights + 1)]["Airline"] = airline.text
                except:
                    print("No se encontro Airline")
                    dict_[str(quantity_flights + 1)]["Airline"] = "no se encontro el aerolinea"
                    #aerolinea = use_xpath(f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]/div/div/div/div/div[1]/div[1]/div/div/div[3]/div", 5)

                try:
                    departure_time = use_xpath(driver,f"(//div[@data-stid='secondary-section'])[{quantity_flights+1}]/div[1]/div/div/div[1]/div[1]/div", 120)
                    dict_[str(quantity_flights + 1)]["Departure time"] = departure_time.text
                except:
                    print("No se encontro horario")
                    dict_[str(quantity_flights + 1)]["horario"] = "Departure time not found"

                try:
                    if "ltiples" in dict_[str(quantity_flights + 1)]["Airline"]:
                        print("Aerolineas multiples")
                        use_xpath(driver,f"//li[@data-test-id='offer-listing'][{quantity_flights+1}]", 60).click()
                        time.sleep(1)
                        use_xpath(driver,f"//span[@class='uitk-expando-title']", 60).click()
                        time.sleep(1)

                        if stop_over.text == "1 escala":
                            airline_1 = use_xpath(driver,f"//div[@class='uitk-spacing']/div[1]/div[2]/span[2]", 1)
                            dict_[str(quantity_flights + 1)]["Airline 1"] = airline_1.text
                            airline_2 = use_xpath(driver,f"//div[@class='uitk-spacing']/div[2]/div[2]/span[2]", 1)
                            dict_[str(quantity_flights + 1)]["Airline 2"] = airline_2.text
                        
                        if stop_over.text == "2 escalas":
                            airline_1 = use_xpath(driver,f"//div[@class='uitk-spacing']/div[1]/div[2]/span[2]", 1)
                            dict_[str(quantity_flights + 1)]["Airline 1"] = airline_1.text
                            airline_2 = use_xpath(driver,f"//div[@class='uitk-spacing']/div[2]/div[2]/span[2]", 1)
                            dict_[str(quantity_flights + 1)]["Airline 2"] = airline_2.text
                            airline_3 = use_xpath(driver,f"//div[@class='uitk-spacing']/div[3]/div[2]/span[2]", 1)
                            dict_[str(quantity_flights + 1)]["Airline 3"] = airline_3.text
                        use_xpath(driver,f"(//*[name()='svg'][@aria-label='Cerrar y volver'])[1]", 60).click()

            
                except Exception as e:
                    print("Error al buscar aerolineas")
                    traceback.print_exc()
                    tb = traceback.extract_tb(e.__traceback__)
                    print(f"Error occurred in line: {tb[-1].lineno}")
                #-----------------END SCRAPPING DATA------------------#

                quantity_flights += 1
                print(quantity_flights)

        except Exception as e:
            # Print the error
            print("An error occurred:")
            traceback.print_exc()
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error occurred in line: {tb[-1].lineno}")

        print(f"Se encontraron {quantity_flights} vuelos")

        #add the data to the dataframe
        df = add_dict_to_df(dict_,df)
    #-----------------END AUTOMATION------------------#


    #-----------------OUTPUT------------------#
    generate_file(df)
    print('Ending program')

finally:
    driver.quit()

# .//div[@data-test-id='price-column'][1]