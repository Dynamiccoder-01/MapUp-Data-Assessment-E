import argparse

import pandas as pd
from datetime import timedelta
import os


def process_trips(parquet_file, output_dir):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(parquet_file)
    time = df['timestamp']
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Initialize lists to store trip information
    latitude = []
    longitude = []
    timestamp = []
    trip_number = 0

    # Iterate through the DataFrame to identify and process trips
    for i in range(1, len(df['timestamp'])):
        # Check if the time difference is greater than 7 hours
        if (df['timestamp'][i] - df['timestamp'][i - 1]) > timedelta(hours=7):
            latitude.append(df['latitude'][i - 1])
            longitude.append(df['longitude'][i - 1])
            timestamp.append(str(time[i - 1]))
            # Save the current trip
            save_trip(df['unit'][i - 1], trip_number, latitude, longitude, timestamp, output_dir)

            # Reset lists for the next trip
            latitude = []
            longitude = []
            timestamp = []
            trip_number += 1

        # Add data to the current trip
        latitude.append(df['latitude'][i - 1])
        longitude.append(df['longitude'][i - 1])
        timestamp.append(str(time[i - 1]))

    # Save the last trip if there's any remaining data
    if len(latitude) > 0:
        save_trip(df['unit'].iloc[-1], trip_number, latitude, longitude, timestamp, output_dir)


def save_trip(unit, trip_number, latitude, longitude, timestamp, output_dir):
    # Create the file path for the CSV file in the output directory
    trip_filename = os.path.join(output_dir, f"{unit}_{trip_number}.csv")

    # Create a DataFrame for the trip data and save it to a CSV file
    trip_df = pd.DataFrame({'latitude': latitude, 'longitude': longitude, 'timestamp': timestamp})
    trip_df.to_csv(trip_filename, index=False)


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Process toll information from JSON files and transform to CSV.")
    parser.add_argument("--to_process", required=True, help="Path to the JSON responses folder.")
    parser.add_argument("--output_dir", required=True,help="Folder where the final transformed_data.csv will be stored.")
    args = parser.parse_args()
    # Process GPS data and save trips to CSV files
    process_trips(args.to_process, args.output_dir)


if __name__ == "__main__":
    main()
