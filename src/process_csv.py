import pandas as pd

def process_weather_data(input_file_path, output_file_path):
    """
    Process the weather data by loading, filtering, and saving it.
    
    Parameters:
    - input_file_path (str): Path to the input CSV file containing the raw weather data.
    - output_file_path (str): Path to the output CSV file where the processed data will be saved.
    
    This function performs the following steps:
    1. Loads the weather data from the input CSV file.
    2. Filters the columns to keep only the relevant weather data.
    3. Renames certain columns for consistency and readability.
    4. Saves the processed data to a new CSV file.
    
    The columns filtered include:
    - date (renamed from 'datetime')
    - temperature (renamed from 'temp')
    - humidity
    - precipprob
    - snow
    - wind_speed (renamed from 'windspeed')
    - visibility
    - conditions
    - description
    """
    df = pd.read_csv(input_file_path)
    filtered_df = df[['datetime', 'temp', 'humidity', 'precipprob', 'snow', 'windspeed', 'visibility', 'conditions', 'description']]  # Filter the columns
    filtered_df = filtered_df.rename(columns = {'datetime': 'date', 'temp':'temperature', 'windspeed':'wind_speed'})  # Rename columns
    filtered_df.to_csv(output_file_path, index=False)
