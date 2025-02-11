# Expedia Flight Prices Scraping

Web scrapping from Expedia fligth section, using `selenium` with `undetected-chromedriver`, works locally or with github actions, check [Setup](#setup) for detailed info.

- Important to get the link from the expedia [page](#page), does not matter the date since the link will be dynamic, just get the link when the data is already filtered


- Only tested with expedia.mx and expedia.com links, check generate_dynamic_url on helper.py if you face any porblem related with links

## Page

Scrapped page preview


[Example link](https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),to:Tokio,%20Jap%C3%B3n%20(TYO-Todos%20los%20aeropuertos),departure:12/02/2025TANYT,fromType:AIRPORT,toType:METROCODE&options=cabinclass:economy&fromDate=12/02/2025&d1=2025-2-12&passengers=adults:1,infantinlap:N) 

![Dashboard Screenshot](https://github.com/danielsaed/Expedia_flight_prices_scraping/blob/Development-using-undetected_chromedriver/.github/img/Expedia_web.png?raw=true)




## Data scrapped

- Price
- Stop over
- Stop over time
- Airline
- Class
- Flight time
- Stop over time and place
- Origin place
- Destination place

<br/>
Example of flight data, generated on csv file on "data/flight_data.csv"

<br/>


| **Price (MXN)** | **Flight Time** | **Stopover** | **Stopover Place** | **Airline** | **Departure Time** | **Date** | **Destination** | **Origin** | **Flight Type** | **Class** |
| :-------------: | :-------------: | :----------: | :----------------: | :---------: | :----------------: | :------: | :-------------: | :--------: | :-------------: | :-------: |
| 3378 | 1 h 47 min | Direct | - | Aeromexico (operated by Aerolitoral) | 16:33 | 18/01/2025 | Ciudad de México | Tepic | Day flight | Economic |
| 9592 | 10 h 41 min | 1 stop | 4 h 48 min in TIJ | Volaris | 20:36 | 18/01/2025 | Ciudad de México | Tepic | Night flight | Economic |
| 9592 | 9 h 34 min | 1 stop | 3 h 28 min in TIJ | Volaris | 20:36 | 18/01/2025 | Ciudad de México | Tepic | Night flight | Economic |


<br/>


## Technology Stack

- **Web Scraping**: 
  - Selenium with undetected-chromedriver
- **Data Processing**: 
  - Python 3.9+
  - pandas

<br/>

## Project Structure

```
Expedia_flight_prices_scraping

├── main.py                # Main scraping app
├── helper.py              # Help functions used on main.py
├── .github/               # Github files and config
├── input_data.json        # Input data loaded in main.py to execute the links and date of flights
├── data/                  # Data collected from data scrapped
```


<br/>



## Setup
### Prerequisites
- Python 3.9
- Required Python libraries: `pandas`, `selenium`, `undetected-chromedriver`
- Power BI Desktop for creating and modifying dashboards

### Installation Local
1. Clone the repository:
   ```bash
   git clone https://github.com/danielsaed/Expedia_flight_prices_scraping.git
   cd Expedia_flight_prices_scraping
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add links you want to scrape with dates as month to input_data.json file:
   ```json
    {
      "flight_urls": [
         "https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),to:Tokio,%20Jap%C3%B3n%20(TYO-Todos%20los%20aeropuertos),departure:12/02/2025TANYT,fromType:AIRPORT,toType:METROCODE&options=cabinclass:economy&fromDate=12/02/2025&d1=2025-2-12&passengers=adults:1,infantinlap:N",
         "https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tokio%20(y%20alrededores),%20Tokio%20(prefectura),%20Jap%C3%B3n,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:13/02/2025TANYT,fromType:MULTICITY,toType:AIRPORT&options=cabinclass:economy&fromDate=13/02/2025&d1=2025-2-13&passengers=adults:1,infantinlap:N"
      ],
      "scrape_months": [2,3,4]
    }
    ```
  

4. Run the scraper script:
   ```bash
   python main.py
   ```
5. The scraped data will be saved in a `data/flights_data.csv` file.

### Installation with GitHub Actions
1. Fork the repository:
   - Visit [Expedia Flight Prices Scraping](https://github.com/danielsaed/Expedia_flight_prices_scraping)
   - Click the "Fork" button in the top-right corner
   - Wait for the repository to be forked to your account



3. Modify input_data.json:
   - Navigate to input_data.json in your forked repository
   - Click the edit button (pencil icon)
   - Update the flight URLs and months you want to scrape:
   ```json
   {
     "flight_urls": [
         "https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),to:Tokio,%20Jap%C3%B3n%20(TYO-Todos%20los%20aeropuertos),departure:12/02/2025TANYT,fromType:AIRPORT,toType:METROCODE&options=cabinclass:economy&fromDate=12/02/2025&d1=2025-2-12&passengers=adults:1,infantinlap:N",
         "https://www.expedia.mx/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:Tokio%20(y%20alrededores),%20Tokio%20(prefectura),%20Jap%C3%B3n,to:Ciudad%20de%20M%C3%A9xico,%20M%C3%A9xico%20(MEX-Aeropuerto%20Internacional%20de%20la%20Ciudad%20de%20M%C3%A9xico),departure:13/02/2025TANYT,fromType:MULTICITY,toType:AIRPORT&options=cabinclass:economy&fromDate=13/02/2025&d1=2025-2-13&passengers=adults:1,infantinlap:N"
     ],
     "scrape_months": [2,3,4]
   }
   ```
   - Commit the changes

4. Run GitHub Action:
   - Go to the "Actions" tab
   - Select "Web Scraping Workflow"
   - Click "Run workflow"
   - Choose the branch (usually 'main')
   - Click "Run workflow"

The action will:
- Set up Python environment
- Install dependencies
- Run the scraper
- Commit the scraped data to the `data/` directory
- Create a pull request if changes are detected

You can find the scraped data in the `data/flights_data.csv` file after the action completes.


## License
This project is licensed under the MIT License. See the LICENSE file for more details.



