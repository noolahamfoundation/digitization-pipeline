import pandas as pd
import os

def split_csv(input_file, output_folder, chunk_size=20000):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Read the large CSV file in chunks
    chunk_iter = pd.read_csv(input_file, chunksize=chunk_size)
    
    # Iterate over each chunk and write to separate CSV files
    for i, chunk in enumerate(chunk_iter):
        output_file = os.path.join(output_folder, f'towns_part_{i+1}.csv')
        chunk.to_csv(output_file, index=False)
        print(f'Wrote {len(chunk)} rows to {output_file}')

# Usage
input_file = 'combined.csv'  # Path to the large input CSV file
output_folder = 'chunked_csv_files'  # Folder to save the smaller CSV files
split_csv(input_file, output_folder)
