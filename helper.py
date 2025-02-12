import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re
import time
import random
import pandas as pd
from datetime import datetime
import calendar

def get_page_visited(url):
    """
    Extracts the domain name from a URL to determine the page visited.

    Args:
        url (str): The URL to extract the domain name from.

    Returns:
        str: The domain name of the page visited.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Extract the main domain (e.g., 'expedia' from 'www.expedia.mx')
    main_domain = domain.split('.')[1] if 'www.' in domain else domain.split('.')[0]
    return main_domain

# Function to validate URLs
def is_valid_url(url):
    """
    Checks if a URL is valid.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Validate flight data input
def validate_links(flight_data):
    """
    Validates the flight data input.

    Args:
        flight_data (dict): Dictionary with flight data. The key must be a number and the value a list with three elements: [origin place, destination place, flight URL].

    Returns:
        None: Ends the program if an invalid entry is found.
    """
    for value in flight_data:
        
        # Check that the third element is a valid URL
        if not is_valid_url(value):
            print(f"Invalid URL for key {value}")
            sys.exit(1)
        
        print(f"Valid entry for key {value}")

# Function to validate and convert input dates
def validate_dates(dates):
    """
    Validates and converts input dates to month numbers.

    Args:
        dates (list): List of dates in different formats (names, abbreviations, numbers).

    Returns:
        list: List of validated month numbers.
    """
    # Dictionary to map month names to numbers
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

    validated_dates = []
    for date in dates:
        date_str = str(date).strip().lower()
        if date_str in month_map:
            validated_dates.append(month_map[date_str])
        else:
            print(f"Invalid date: {date}")
            sys.exit(1)
    
# Function to generate a random delay
def random_delay(start=1, end=3):
    """
    Generates a random delay.

    Args:
        start (int): Minimum delay time in seconds.
        end (int): Maximum delay time in seconds.

    Returns:
        None
    """
    time.sleep(random.uniform(start, end))


def generate_dynamic_url(base_url, new_departure_date):
    """
    Generates a dynamic URL by updating the departure date.
    Handles both expedia.com and expedia.mx URLs differently.

    Args:
        base_url (str): The base URL.
        new_departure_date (str): The new departure date in 'dd/mm/yyyy' format.

    Returns:
        tuple: (str, str) The updated URL and the page type.
    """
    # Parse the URL
    url_parts = urlparse(base_url)
    query_params = parse_qs(url_parts.query)
    domain = url_parts.netloc

    # Convert the string to a datetime object
    date_obj = datetime.strptime(new_departure_date, "%d/%m/%Y")
    
    page = ""
    if 'expedia' in domain:
        page = "Expedia"
        
        if 'expedia.mx' in domain:
            # Format dates for expedia.mx (original format)
            date_slash = date_obj.strftime("%d/%m/%Y")  # Format: dd/mm/yyyy
            date_dash = date_obj.strftime("%Y-%m-%d")   # Format: yyyy-mm-dd
            
            # Update dates in query parameters for Expedia MX
            for key in query_params:
                # Handle dates with slashes (d/m/Y format)
                query_params[key] = [re.sub(r'\d{1,2}/\d{1,2}/\d{4}', date_slash, param) for param in query_params[key]]
                # Handle dates with dashes (Y-m-d format)
                query_params[key] = [re.sub(r'\d{4}-\d{1,2}-\d{1,2}', date_dash, param) for param in query_params[key]]
        
        else:  # expedia.com

            date_obj = datetime.strptime(new_departure_date, "%d/%m/%Y")
    
            # Format dates for different URL patterns
            date_slash = date_obj.strftime("%m/%d/%Y")  # US format for URLs (m/d/Y)
            date_dash = date_obj.strftime("%Y-%m-%d")   # ISO format (Y-m-d)
            # Update dates in query parameters for Expedia
            for key in query_params:
                # Handle dates with slashes (both d/m/Y and m/d/Y formats)
                query_params[key] = [re.sub(r'\d{1,2}/\d{1,2}/\d{4}', date_slash, param) for param in query_params[key]]
                # Handle dates with dashes (Y-m-d format)
                query_params[key] = [re.sub(r'\d{4}-\d{1,2}-\d{1,2}', date_dash, param) for param in query_params[key]]
        
            
    elif 'kayak' in domain:
        page = "Kayak"
        # Update the path for Kayak
        path_parts = url_parts.path.split('/')
        for i, part in enumerate(path_parts):
            if re.match(r'\d{4}-\d{2}-\d{2}', part):
                path_parts[i] = date_dash
        url_parts = url_parts._replace(path='/'.join(path_parts))

    # Reconstruct the URL with updated query parameters
    updated_query = urlencode(query_params, doseq=True)
    updated_url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path, 
                             url_parts.params, updated_query, url_parts.fragment))

    return updated_url, page

# Function to generate a list of dates in "dd/mm/yyyy" format
def generate_dates(months):
    """
    Generates a list of dates in "dd/mm/yyyy" format for the specified months.

    Args:
        months (list): List of months in different formats (names, abbreviations, numbers).

    Returns:
        list: List of dates in "dd/mm/yyyy" format.
    """
    # Current date
    today = datetime.today()
    
    # Dictionary to map month names and abbreviations to numbers
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
    qty = 0
    # List to store generated dates
    dates = []

    # Iterate over the input months list
    for month in months:

        month_str = str(month).strip().lower()
        if month_str in month_map:
            month_num = month_map[month_str]
            year = today.year
            
            # Generate dates for each day of the specified month
            for day in range(1, calendar.monthrange(year, month_num)[1] + 1):
                date = datetime(year, month_num, day)
                qty += 1

                if date >= today:
                    print(date)
                    print(today)
                    dates.append(date.strftime("%d/%m/%Y"))
                '''if qty > 12:
                    break'''
    
    return dates

# Function to add a dictionary to a DataFrame
def add_dict_to_df(dict_, df):
    """
    Adds data from a dictionary to a DataFrame.

    Args:
        dict_ (dict): Dictionary with data to add.
        df (pd.DataFrame): DataFrame to which the data will be added.

    Returns:
        pd.DataFrame: Updated DataFrame with added data.
    """
    for i in dict_:
        temp_df = pd.DataFrame(dict_[i], index=[0])
        temp_df = temp_df.reindex(columns=df.columns)
        df = pd.concat([df, temp_df], ignore_index=True)
    return df

# Function to generate a CSV file with flight data
def generate_file(df):
    """
    Generates a CSV file with flight data.

    Args:
        df (pd.DataFrame): DataFrame with flight data.

    Returns:
        None
    """

    df = df[df['Price'] != 'Price not found']
    
    df['Flight type'] = ''
    #df['Class'] = 'Economic'
    df['Days to date'] = ''
    df['Day of week'] = ''
    df['Date of flight'] = pd.to_datetime(df['Date of flight'], format='%d/%m/%Y', dayfirst=True)
    df['Days to date'] = count_days_to_date(df['Date of flight'])

    # Extract the day of the week
    df['Day of week'] = df['Date of flight'].dt.day_name()

    try:

        df['Departure time'] = pd.to_datetime(df['Departure time'], format='%H:%M').dt.time

        df.loc[(df['Departure time'] >= pd.to_datetime('18:00', format='%H:%M').time()) | (df['Departure time'] < pd.to_datetime('05:00', format='%H:%M').time()), 'Flight type'] = 'Night flight'
        df.loc[(df['Departure time'] >= pd.to_datetime('12:00', format='%H:%M').time()) & (df['Departure time'] < pd.to_datetime('18:00', format='%H:%M').time()), 'Flight type'] = 'Day flight'
        df.loc[(df['Departure time'] >= pd.to_datetime('5:00', format='%H:%M').time()) & (df['Departure time'] < pd.to_datetime('12:00', format='%H:%M').time()), 'Flight type'] = 'Morning flight'

    except:
        df['Departure time'] = pd.to_datetime(df['Departure time'], format='mixed').dt.time

        # Define flight types based on departure time
        df.loc[(df['Departure time'] >= pd.to_datetime('18:00').time()) | 
            (df['Departure time'] < pd.to_datetime('05:00').time()), 'Flight type'] = 'Night flight'
        df.loc[(df['Departure time'] >= pd.to_datetime('12:00').time()) & 
            (df['Departure time'] < pd.to_datetime('18:00').time()), 'Flight type'] = 'Day flight'
        df.loc[(df['Departure time'] >= pd.to_datetime('05:00').time()) & 
            (df['Departure time'] < pd.to_datetime('12:00').time()), 'Flight type'] = 'Morning flight'

    df['Scrapped date'] = datetime.now().strftime('%Y-%m-%d')
    
    try:
        df_excel = pd.read_csv(r'data/flights_data.csv')
        df = pd.concat([df_excel, df], ignore_index=True)
    except:
        print('No file found')

    df.drop_duplicates()
    df.to_csv(r"data/flights_data.csv", index=False)
    print('Output file generated')

# Function to count the number of days from today to a target date
def count_days_to_date(date_series):
    """
    Counts the number of days from today to the target date.

    Args:
        target_date (str): The target date in 'yyyy-mm-dd' format.

    Returns:
        int: The number of days from today to the target date.
    """
    today = datetime.today()
    days_to_date = date_series.apply(lambda x: (x - today).days)
    return days_to_date

# Function to get the content inside the second pair of parentheses
def get_second_parentheses_content(text):
    """
    Gets the content inside the second pair of parentheses from a string.

    Args:
        text (str): The input string.

    Returns:
        str: The content inside the second pair of parentheses, or an empty string if not found.
    """
    # Use regular expression to find all content inside parentheses
    matches = re.findall(r'\(.*?\)', text)
    # Return the content inside the second pair of parentheses if it exists
    first_content = matches[0] if len(matches) >= 1 else ""
    second_content = matches[1] if len(matches) >= 2 else ""
    return first_content, second_content

# 
def use_xpath(driver,xpath,time):
    '''
    Function to use the xpath of an element and wait for it to appear
    args:   
        xpath: the xpath of the element
        time: the time to wait for the element
    '''
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))