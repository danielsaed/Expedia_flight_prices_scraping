# Expedia Flight Prices Scraping

The project implements an ETL (Extract, Transform, Load) process to gather and analyze flight data from Expedia. Using Selenium for web scraping, the data is systematically extracted, organized, and stored in a structured CSV file format. The collected data is then transformed and loaded into an interactive Power BI dashboard, where it is visualized to uncover insightful trends and patterns in flight pricing.

The primary objective of this project is to provide actionable insights into flight prices by automating data collection and presenting it in an intuitive and interactive dashboard. This end-to-end solution highlights the complete workflow, from data extraction and transformation to visualization, demonstrating the integration of web scraping, data organization, and business intelligence tools.

## Features
- **Web Scraping**: Collects flight data (e.g., origin, destination, airline, price, stopovers) from Expedia.
- **Data Storage**: Saves scraped data into a structured CSV file.
- **Data Visualization**: Utilizes Power BI to create an interactive dashboard for analyzing flight prices.

## Web Page Preview

![Dashboard Screenshot](https://github.com/danielsaed/Expedia_flight_prices_scraping/blob/Development-using-undetected_chromedriver/.github/img/Expedia_web.png?raw=true)

# Flight Prices Table

Example of flight data, generated on csv file.


| **Price (MXN)** | **Flight Time** | **Stopover** | **Stopover Place**       | **Airline**                                                   | **Departure Time** | **Date**      | **Destination**      | **Origin**          | **Flight Type** | **Class**   |
| :------------------: |-----------------|--------------|--------------------------|-------------------------------------------------------------|--------------------|---------------|-----------------------|---------------------|-----------------|-------------|
| 3378             | 1 h 47 min     | Direct       | -                        | Aeromexico (operated by Aerolitoral)                        | 16:33             | 18/01/2025   | Ciudad de México     | Tepic               | Day flight      | Economic    |
| 9592             | 10 h 41 min    | 1 stop       | 4 h 48 min in TIJ        | Volaris                                                     | 20:36             | 18/01/2025   | Ciudad de México     | Tepic               | Night flight    | Economic    |
| 9592             | 9 h 34 min     | 1 stop       | 3 h 28 min in TIJ        | Volaris                                                     | 20:36             | 18/01/2025   | Ciudad de México     | Tepic               | Night flight    | Economic    |
| 3255             | 1 h 40 min     | Direct       | -                        | Aeromexico (operated by Aerolitoral)                        | 15:00             | 18/01/2025   | Tepic               | Ciudad de México    | Day flight      | Economic    |
| 9592             | 10 h 41 min    | 1 stop       | 4 h 48 min in TIJ        | Volaris                                                     | 20:36             | 18/01/2025   | Ciudad de México     | Tepic               | Night flight    | Economic    |
| 9592             | 9 h 34 min     | 1 stop       | 3 h 28 min in TIJ        | Volaris                                                     | 20:36             | 18/01/2025   | Ciudad de México     | Tepic               | Night flight    | Economic    |
| 3494             | 1 h 47 min     | Direct       | -                        | Aeromexico (operated by Aerolitoral)                        | 16:23             | 19/01/2025   | Ciudad de México     | Tepic               | Day flight      | Economic    |
| 11042            | 9 h 34 min     | 1 stop       | 3 h 28 min in TIJ        | Volaris                                                     | 20:36             | 19/01/2025   | Ciudad de México     | Tepic               | Night flight    | Economic    |
| 11042            | 10 h 41 min    | 1 stop       | 4 h 48 min in TIJ        | Volaris                                                     | 20:36             | 19/01/2025   | Ciudad de México     | Tepic               | Night flight    | Economic    |
| 3255             | 1 h 40 min     | Direct       | -                        | Aeromexico (operated by Aerolitoral)                        | 14:50             | 19/01/2025   | Tepic               | Ciudad de México    | Day flight      | Economic    |

## Dashboard
The dashboard presents the following insights:
- Lowest flight prices by day.
- Daily average lowest price by airline.
- Price trends for different destinations and airlines.
- Interactive filters for origin, destination, airline, and month.

### Dashboard Preview
![Dashboard Screenshot](https://github.com/danielsaed/Expedia_flight_prices_scraping/blob/Development-using-undetected_chromedriver/.github/img/Expedia_flight_dasboard.png?raw=true)

[View Interactive Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYjI4ZjI4MjEtNDcwNC00N2RiLWFjNjMtZGY2YTc1YmI3NGUyIiwidCI6IjZjMGMxMTZhLWJmOGItNDc4My04NjI3LTNjZTVmMDE0MjhlNCIsImMiOjR9)

## Setup
### Prerequisites
- Python 3.7+
- Required Python libraries: `pandas`, `selenium`, `undetected-chromedriver`
- Power BI Desktop for creating and modifying dashboards

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/danielsaed/Expedia_flight_prices_scraping.git
   cd Expedia_flight_prices_scraping
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scraper script:
   ```bash
   python main.py
   ```
4. The scraped data will be saved in a `flights_data.csv` file.

## Usage
1. Scrape flight data using the provided script.
2. Open the Power BI file and load the updated CSV data.
3. Interact with the dashboard to analyze flight prices.

## Project Workflow
1. **Data Collection**: Scrape flight data using Python scripts.
2. **Data Storage**: Save the collected data into a CSV file.
3. **Visualization**: Use Power BI to create a dashboard for insights.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
Special thanks to Expedia for the data and Power BI for enabling data visualization.


