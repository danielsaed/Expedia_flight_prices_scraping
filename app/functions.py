import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re
import time
import random
import pandas as pd
from datetime import datetime
import calendar

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
def validate_flight_data(flight_data):
    """
    Validates the flight data input.

    Args:
        flight_data (dict): Dictionary with flight data. The key must be a number and the value a list with three elements: [origin place, destination place, flight URL].

    Returns:
        None: Ends the program if an invalid entry is found.
    """
    for key, value in flight_data.items():
        # Check that the key is a number
        if not isinstance(key, int):
            print(f"Invalid key: {key} (must be a number)")
            sys.exit(1)
        
        # Check that the value is a list with three elements
        if not isinstance(value, list) or len(value) != 3:
            print(f"Invalid value for key {key}: {value} (must be a list with three elements)")
            sys.exit(1)
        
        origin, destination, url = value
        
        # Check that the first and second elements are strings
        if not isinstance(origin, str) or not isinstance(destination, str):
            print(f"Invalid origin or destination for key {key}: {origin}, {destination} (must be strings)")
            sys.exit(1)
        
        # Check that the third element is a valid URL
        if not is_valid_url(url):
            print(f"Invalid URL for key {key}: {url}")
            sys.exit(1)
        
        print(f"Valid entry for key {key}: {value}")

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

# Function to generate a dynamic URL
def generate_dynamic_url(base_url, new_departure_date):
    """
    Generates a dynamic URL by updating the departure date.

    Args:
        base_url (str): The base URL.
        new_departure_date (str): The new departure date in 'yyyy-mm-dd' format.

    Returns:
        str: The updated URL.
    """
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
                if date >= today:
                    dates.append(date.strftime("%d/%m/%Y"))
    
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
    df['Flight type'] = ''
    df['Class'] = 'Economic'

    df['Departure time'] = pd.to_datetime(df['Departure time'], format='%H:%M').dt.time

    df.loc[(df['Departure time'] >= pd.to_datetime('18:00', format='%H:%M').time()) | (df['Departure time'] < pd.to_datetime('05:00', format='%H:%M').time()), 'Flight type'] = 'Night flight'
    df.loc[(df['Departure time'] >= pd.to_datetime('12:00', format='%H:%M').time()) & (df['Departure time'] < pd.to_datetime('18:00', format='%H:%M').time()), 'Flight type'] = 'Day flight'
    df.loc[(df['Departure time'] >= pd.to_datetime('5:00', format='%H:%M').time()) & (df['Departure time'] < pd.to_datetime('12:00', format='%H:%M').time()), 'Flight type'] = 'Morning flight'

    df.to_csv(r"data\\flights_data.csv", index=False)
    print('Output file generated')