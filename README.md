# Expedia Flight Prices Scraping

This project is a solution designed to gather and analyze flight data from Expedia. By web scraping with selenium, the data is systematically extracted, organized, and stored in a structured CSV file format. The stored data is subsequently utilized to generate insightful visualizations in an interactive Power BI dashboard, enabling users to explore and analyze flight pricing trends effectively.

## Overview
The main goal of this project is to provide insights into flight prices by scraping data from Expedia and presenting it in an interactive dashboard. It showcases the complete process, from data collection to data visualization.

## Features
- **Web Scraping**: Collects flight data (e.g., origin, destination, airline, price, stopovers) from Expedia.
- **Data Storage**: Saves scraped data into a structured CSV file.
- **Data Visualization**: Utilizes Power BI to create an interactive dashboard for analyzing flight prices.

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


