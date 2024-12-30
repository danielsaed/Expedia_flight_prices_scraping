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

#display = Display(visible=0, size=(800, 800))  
#display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
chrome_options = webdriver.ChromeOptions()  

options = [
  # Define window size here
    #"--headless",
   "--window-size=1200,1200",
   "--ignore-certificate-errors",
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)

driver.get('https://www.expedia.mx/')
print('done')
vuelos = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="multi-product-search-form-1"]/div/div/div/div/div[1]/ul/li[2]/a/span'))).click()
time.sleep(10)

#xpath viaje sencillo //span[normalize-space()='Viaje sencillo']
#xpath boton origen //button[@aria-label='Origen']
#xpath input origen //input[@id='origin_select']
#xpath tepic //button[@aria-label='Tepic (TPQ - A. Nacional Amado Nervo) Nayarit, México']
#xpath boton destino //button[@aria-label='Destino']
#xpath input destino //input[@id='destination_select']
#xpath cdmx //button[@aria-label='Ciudad de México (MEX - Aeropuerto Internacional de la Ciudad de México) México']
#xpath date //button[@data-testid="uitk-date-selector-input1-default"]/following-sibling::input
#xpath date input //button[@data-testid="uitk-date-selector-input1-default"]/preceding::input[1]
#xpath search //button[@id='search_button']
#xpath wait to //select[@id='sort-filter-dropdown-SORT']

#xpath listings //li[@data-test-id='offer-listing']

#path text of the listing //li[@data-test-id='offer-listing'][1]//div/button/span
with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {driver.title}")