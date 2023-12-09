# import necessary libraries
import os
import json
import csv
import argparse


# function to process JSON files and create CSV
def process_json_files(input_folder, output_folder):
    # List to store processed data for CSV
    csv_data = []

    # Process each JSON file in the input folder
    for json_file in os.listdir(input_folder):

        # Check if the file has a .json extension
        if json_file.endswith('.json'):
            # Extract trip_id from the file name
            trip_id = json_file.split('.')[0]

            # Create the full path to the JSON file
            json_path = os.path.join(input_folder, json_file)

            # Read JSON file
            with open(json_path, 'r') as json_file:
                # Load JSON data
                json_data = json.load(json_file)

                # Check if there are tolls in the route
                if 'tolls' in json_data['route']:

                    # Iterate over tolls in the route
                    for toll in json_data['route']['tolls']:
                        print(toll)

                        # Extract relevant data
                        unit = trip_id.split('_')[0]
                        toll_loc_id_start = toll['start']['id']
                        toll_loc_id_end = toll['end']['id']
                        toll_loc_name_start = toll['start']['name']
                        toll_loc_name_end = toll['end']['name']
                        toll_system_type = toll['type']
                        entry_time = toll['start']['arrival']['time']
                        exit_time = toll['end']['arrival']['time']
                        tag_cost = toll.get('tagCost', '')
                        cash_cost = toll.get('cashCost', '')
                        license_plate_cost = toll.get('licensePlateCost', '')

                        # Append data to CSV list
                        csv_data.append([unit, trip_id, toll_loc_id_start, toll_loc_id_end, toll_loc_name_start,
                                         toll_loc_name_end, toll_system_type, entry_time, exit_time,
                                         tag_cost, cash_cost, license_plate_cost])

    # Write CSV file with consolidated data
    csv_file_path = os.path.join(output_folder, 'transformed_data.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(['unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end', 'toll_loc_name_start',
                             'toll_loc_name_end', 'toll_system_type', 'entry_time', 'exit_time',
                             'tag_cost', 'cash_cost', 'license_plate_cost'])
        # Write data
        csv_writer.writerows(csv_data)

    print(f"CSV file saved at: {csv_file_path}")


# main function to handle command-line arguments
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process toll information from JSON files and transform to CSV.")
    parser.add_argument("--to_process", required=True, help="Path to the JSON responses folder.")
    parser.add_argument("--output_dir", required=True,
                        help="Folder where the final transformed_data.csv will be stored.")
    args = parser.parse_args()

    # Process JSON files and create CSV
    process_json_files(args.to_process, args.output_dir)


# entry point of the script
if __name__ == "__main__":
    main()
