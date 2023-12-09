import os
import requests
from dotenv import load_dotenv
import argparse
import json


def upload_csv_to_tollguru(csv_path, api_key, map_provider, vehicle_type):
    # Construct the URL for TollGuru API
    url = f'{os.getenv("TOLLGURU_API_URL")}/gps-tracks-csv-upload?mapProvider={map_provider}&vehicleType={vehicle_type}'
    headers = {'x-api-key': api_key, 'Content-Type': 'text/csv'}

    # Open the CSV file and send a POST request to TollGuru API
    with open(csv_path, 'rb') as file:
        response = requests.post(url, data=file, headers=headers)

    # Return the JSON response received from the API
    return response.json()


def process_csv_files(input_folder, output_folder, api_key, map_provider, vehicle_type):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each CSV file in the input folder
    for csv_file in os.listdir(input_folder):
        # Check if the CSV file starts with '2000' (example condition)
        if csv_file.startswith('2000'):
            csv_path = os.path.join(input_folder, csv_file)

            # Upload CSV to TollGuru API and get the JSON response
            json_response = upload_csv_to_tollguru(csv_path, api_key, map_provider, vehicle_type)

            # Save the JSON response in the output folder with the same file name
            json_file_path = os.path.join(output_folder, f"{os.path.splitext(csv_file)[0]}.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(json_response, json_file)  # Convert dictionary to JSON string


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Upload CSV files to TollGuru API and store JSON responses.")
    parser.add_argument("--to_process", required=True, help="Path to the CSV folder.")
    parser.add_argument("--output_dir", required=True, help="Folder where the resulting JSON files will be stored.")
    args = parser.parse_args()

    # Get API key, map provider, and vehicle type from environment variables
    api_key = os.getenv("TOLLGURU_API_KEY")
    map_provider = "osrm"  # You can modify this if needed
    vehicle_type = "5AxlesTruck"  # You can modify this if needed

    # Process CSV files and upload to TollGuru API
    process_csv_files(args.to_process, args.output_dir, api_key, map_provider, vehicle_type)


if __name__ == "__main__":
    main()
