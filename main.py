from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import traceback
import pandas as pd
from helper import *
import json
from pyvirtualdisplay import Display


    
#-----------------FUNCTIONS------------------#
#function to get the text of the xpath and add it to the dictionary
def get_xpath_data_to_dic(name,time):
    #validate if the xpath is not empty, if it is not empty get the text of the xpath and add it to the dictionary
    if dic_xpats[name][0] != "":
        #iterate over the xpaths
        for xpath in dic_xpats[name]:
            #
            try:
                #get the text of the xpath
                current_xpath = use_xpath(driver,xpath.format(quantity_flights=quantity_flights), time)
                #add the text to the dictionary
                dic_flight_data[quantity_flights][name] = current_xpath.text
                
                #if the text is empty, try to get the aria-label
                if dic_flight_data[quantity_flights][name] == "":
                    try:
                        #add the aria-label to the dictionary
                        dic_flight_data[quantity_flights][name] = current_xpath.getAttribute("aria-label")
                    
                    except:
                        #if the aria-label is empty, add the name of the element to the dictionary
                        dic_flight_data[quantity_flights][name] = dic_flight_data[1][name]
                return True
            
                
            except:
                dic_flight_data[quantity_flights][name] = f"{name} not found"
        #print(f"No se encontro {name} - {xpath.format(quantity_flights=quantity_flights)}")

#function to get the text of the xpath
def get_xpath_data_to_text(xpath,name,time):
    #use the xpath to get the text of the element
    try:
        return use_xpath(driver,xpath, time).text
        
    except:
        #print(f"No se encontro {name} - {xpath}")
        return f"{name} not found"




#-----------------INPUT------------------#
#read the input data from input_data.json

with open("input_data.json") as f:
    config = json.load(f)

#list of urls and months
urls = config["flight_urls"]
months = [str(item) for item in config["scrape_months"]]

#validating the input
validate_links(urls)
validate_dates(months)

#generate dates base on the months
dates = generate_dates(months)

#init variables
links = []
dic_flight_data = {}
quantity_flights=1

#init dataframe
df = pd.DataFrame(columns=["Price", "Flight time","Stop over","Stop over place","Airline", "Departure time","Date of flight","Destination place","Origin place","Airline 1","Airline 2","Airline 3","Class","Page"])


#pass links, dates and page to a matrix links
for i in range(len(dates)):
    for key in urls:
        url,page = generate_dynamic_url(key,dates[i])
        links.append([url,page,dates[i]])

#----------------------------------------#






#-----------------Comment 2 lines if execution is local------------------#
display = Display(visible=0, size=(800, 800))  
display.start()






#-----------------CONFIGURATION------------------#

#dictionary with the xpaths
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

#options for the browser
try:
    chromedriver_autoinstaller.install()# Check if the current version of chromedriver exists and if it doesn't exist, download it automatically,
except:
    print("Error al instalar chromedriver")

ua = UserAgent()
user_agent = ua.random
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")

options = [
    #"--headless=new",  # Hides the browser window
    #"--window-size=1200,1200",
    "--ignore-certificate-errors",
    "--lang=es",
    "--disable-dev-shm-usage",  # Overcome limited resource problems
    "--no-sandbox",
    "--enable-javascript",
    "--allow-running-insecure-content",
    "--disable-popup-blocking",  # Disable popup blocking
    "--disable-web-security",
    "--disable-site-isolation-trials",
    "--disable-extensions",
    "--disable-infobars",
    "--disable-notifications",
    "--disable-automation",
    "--disable-blink-features=AutomationControlled",
    "--disable-blink-features=BlockCredentialedSubresources"
    ]

for option in options:
    chrome_options.add_argument(option)

#----------------------------------------#







#-----------------START AUTOMATION------------------#
try:
    #initialize the driver
    driver = uc.Chrome(use_subprocess=True,options=chrome_options,version_main=132)
    
    #access the page
    driver.get(links[0][0])

    #iterate over the links
    for current_link,page,date in links:

        #validate the page
        if page == "Expedia":
            dic_xpats= dic_xpats_expedia
        else:
            continue
        
        quantity_flights=1
        
        #open a new tab
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

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched back to new tab")

        #wait for the page to load
        use_xpath(driver,"//li[@data-test-id='offer-listing']",180)
        time.sleep(5)

        #get the elements of the page quantity, to know how many flights are in the page
        elements = driver.find_elements(By.XPATH, "//li[@data-test-id='offer-listing']")
        elements = len(elements)

        

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
                get_xpath_data_to_dic("Origin place", 1)

                #-- get Destination place
                get_xpath_data_to_dic(f"Destination place", 1)

                #-- get the content of the second parentheses usually the city
                get_xpath_data_to_dic("Parentesis place 1", 1)

                #-- get Price
                get_xpath_data_to_dic("Price", 1)

                #-- get Flight time
                get_xpath_data_to_dic("Flight time", 1)

                #-- get Stop over
                get_xpath_data_to_dic("Stop over", 1)

                #-- get Airline
                get_xpath_data_to_dic("Airline", 1)

                #-- get Departure time
                get_xpath_data_to_dic("Departure time", 1)



                #----------------------DATA PREPROCESSING----------------------#
                #-- get the content of the second parentheses usually the city and add it to the origin and destination place
                first,second = get_second_parentheses_content(dic_flight_data[quantity_flights]["Parentesis place 1"])
                dic_flight_data[quantity_flights]["Origin place"] = dic_flight_data[quantity_flights]["Origin place"] + " " + first
                dic_flight_data[quantity_flights]["Destination place"] = dic_flight_data[quantity_flights]["Destination place"] + " " + second

                #-- get Stop over place, the try except is to get the stop over place if the flight has 1 or 2 stops if not it means that the flight is direct no need to get the stop over place
                try:
                    dic_flight_data[quantity_flights]["Stop over place"] = get_xpath_data_to_text(dic_xpats['Stop over place'][1].format(quantity_flights=quantity_flights),"Stop over place",.5) + " and " + get_xpath_data_to_text(dic_xpats['Stop over place'][2].format(quantity_flights=quantity_flights),"Stop over place",.5)
                except:    
                    try:
                        dic_flight_data[quantity_flights]["Stop over place"] = get_xpath_data_to_text(dic_xpats['Stop over place'][0].format(quantity_flights=quantity_flights),"Stop over place", .5)
                    except:
                        print("vuelo sin escalas")

                #if the airline is multiple get the get airline 1, airline 2, airline 3
                if "ltiple" in dic_flight_data[quantity_flights]["Airline"]:
                    try:
                        #click on the flight to get the airlines
                        use_xpath(driver,f"//li[@data-test-id='offer-listing'][{quantity_flights}]", 10).click()
                        time.sleep(1)
                        #click on the expand button
                        use_xpath(driver,f"//span[@class='uitk-expando-title']", 10).click()
                        time.sleep(1)

                        #get the airlines
                        try:
                            get_xpath_data_to_dic("Airline 1", 1)
                        except:
                            print("No Airline 1")
                        try:
                            get_xpath_data_to_dic("Airline 2", 1)
                        except:
                            print("No Airline 2")
                        try:
                            get_xpath_data_to_dic("Airline 3", 1)
                        except:
                            print("No Airline 3")

                        #close the flight
                        try:
                            use_xpath(driver,f"(//*[name()='svg'][@aria-label='Cerrar y volver'])[1]", .5).click()
                        except:
                            use_xpath(driver,f"//span[@class='uitk-toolbar-button-content uitk-toolbar-button-content-icon-only']//*[name()='svg']", 1).click()

                    except:
                        print("Error al obtener las aerolineas multiples")
            
                #-----------------END SCRAPPING DATA------------------#

                #sum 1 to the quantity of flights

                print(f"Vuelo {quantity_flights} completado")
                quantity_flights += 1

        #if an error occurs, print the error
        except Exception as e:
            # Print the error
            print("An error occurred:")
            traceback.print_exc()
            tb = traceback.extract_tb(e.__traceback__)
            print(f"Error occurred in line: {tb[-1].lineno}")

        #print the quantity of flights found
        print(f"Se encontraron {quantity_flights-1} vuelos, dia: {date}")

        #add the data to the dataframe
        df = add_dict_to_df(dic_flight_data,df)
    #-----------------END AUTOMATION------------------#



    #-----------------OUTPUT------------------#
except Exception as e:
    # Print the error
    print("An error occurred:")
    traceback.print_exc()
    tb = traceback.extract_tb(e.__traceback__)
    print(f"Error occurred in line: {tb[-1].lineno}")

finally:
    #close the driver
    generate_file(df)
    try:
        driver.quit()
    except:
        print("Error al cerrar el driver")

