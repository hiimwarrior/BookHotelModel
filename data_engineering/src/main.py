import argparse
from utils.db import save_to_db
from utils.file import is_csv_empty, save_to_csv
from transformations.process_bookings_data_v1 import process_bookings_data_v1
import os

def main():
    parser = argparse.ArgumentParser(
        description="Process and clean hotel bookings data."
    )
    parser.add_argument(
        "--destination",
        choices=["csv", "db"],
        default="csv",
        help='Specify the destination for the processed data. Options are "csv" or "db". Default is "csv".',
    )
    parser.add_argument(
        "--version",
        default="1",
        help='Specify the version of the transformation. Default is "1".',
    )
    args = parser.parse_args()

    # Process the data
    transformed_df = process_bookings_data_v1()

    # Save the data based on the destination parameter
    if args.destination == "csv":
        dataset_filename="clean_hotel_bookings_v1.csv"
        base_dir = os.path.dirname(__file__)
        data_path = os.path.abspath(os.path.join(base_dir, '../../data/processed', dataset_filename))
        if is_csv_empty(data_path):
            save_to_csv(transformed_df, data_path)
        else:
            print("CSV file already contains data. No new data saved.")
    elif args.destination == "db":
        save_to_db(transformed_df, version=args.version)


if __name__ == "__main__":
    main()
