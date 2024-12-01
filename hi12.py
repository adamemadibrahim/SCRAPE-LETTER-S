import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to get business type from the business page
def get_business_type(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)  # 10 seconds timeout
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        business_type_element = soup.select_one(
            "#contact-details > div.contact-details > div.media-object.clearfix.inside-gap-medium.image-on-right > div > h2 > a"
        )
        return business_type_element.get_text(strip=True) if business_type_element else None
    except Exception as e:
        return None

# File paths
input_file = 'S_GROUP.csv'
output_file = 'S_GROUP_with_business_type.csv'

# Load the data
data = pd.read_csv(input_file)
if os.path.exists(output_file):
    processed_data = pd.read_csv(output_file)
    start_index = len(processed_data)
    print(f"Resuming from index {start_index}")
    data = data.iloc[start_index:]
else:
    start_index = 0
    processed_data = data.copy()
    processed_data['Business Type'] = None

# Process rows in batches
batch_size = 100
for batch_start in range(0, len(data), batch_size):
    batch_end = batch_start + batch_size
    batch = data.iloc[batch_start:batch_end]
    for index, row in batch.iterrows():
        business_link = row.get('Business Link', None)
        if isinstance(business_link, str) and business_link.startswith("http"):
            print(f"Processing: {business_link}")
            business_type = get_business_type(business_link)
            processed_data.at[start_index + index, 'Business Type'] = business_type
        else:
            print(f"Skipping invalid link at index {index}")
    processed_data.to_csv(output_file, index=False)
    print(f"Saved batch {batch_start} to {batch_end} to {output_file}")
