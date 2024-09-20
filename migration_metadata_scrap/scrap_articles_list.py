# 1st script to execute to scrap the list of Noolaham List
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL to scrape
base_url = "https://noolaham.org/wiki/index.php?title=நூலகம்:"

# Function to scrape a single page
def scrape_page(page_number):
    url = base_url + str(page_number).zfill(2)
    print("Scraping page:", url)
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_number}: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    
    if not table:
        print(f"No table found on page {page_number}")
        return None

    # Extract table headers (first two columns only)
    headers = []
    for th in table.find_all('th')[:2]:
        headers.append(th.text.strip())

    # Extract table rows (first two columns only)
    rows = []
    for tr in table.find_all('tr')[1:]:  # skip the header row
        cells = tr.find_all('td')[:2]  # only take the first two columns
        row = [cell.text.strip() for cell in cells]
        # Check if the number of columns matches the number of headers
        if len(row) == len(headers):
            rows.append(row)
        else:
            print(f"Warning: Mismatch in number of columns at page {page_number}. Skipping row.")
            print(f"Headers: {len(headers)}, Row: {len(row)}")

    if rows:
        return pd.DataFrame(rows, columns=headers)
    else:
        return None

# Loop through the pages and save data to CSV files
all_data = []
for page_number in range(1, 11):  # Adjust the range as needed
    df = scrape_page(page_number)
    if df is not None:
        all_data.append(df)
    if page_number % 10 == 0:
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df.to_csv(f'books_and_authors_{page_number // 10}.csv', index=False)
            print(f'Created CSV: books_and_authors_{page_number // 10}.csv')
            all_data = []

# Save any remaining data
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_csv(f'books_and_authors_{(page_number // 10) + 1}.csv', index=False)
    print(f'Created CSV: books_and_authors_{(page_number // 10) + 1}.csv')

print("CSV files have been created successfully.")
