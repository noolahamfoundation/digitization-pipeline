import os
import pandas as pd

def concatenate_csv_files(directory, output_file):
    """
    Concatenates all CSV files in the specified directory into one output file.

    Args:
        directory (str): The path to the directory containing CSV files.
        output_file (str): The path to the output CSV file.
    """
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_csv(output_file, index=False)

    print(f"All CSV files have been concatenated into {output_file}")

# Usage
directory = '/home/parathan/Desktop/scripts/scripts/first_list'  # Replace with the path to your directory
output_file = 'combined.csv'  # Replace with the desired output CSV file name

concatenate_csv_files(directory, output_file)
