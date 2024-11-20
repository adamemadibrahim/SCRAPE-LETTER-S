import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get business type from the business page
def get_business_type(url):
    try:
        # Send HTTP request to the URL with a user-agent header to prevent blocking
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch {url} (Status Code: {response.status_code})")
            return None
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the business type element using the provided CSS selector
        business_type_element = soup.select_one(
            "#contact-details > div.contact-details > div.media-object.clearfix.inside-gap-medium.image-on-right > div > h2 > a"
        )
        
        # Return the business type if found, otherwise return None
        if business_type_element:
            business_type = business_type_element.get_text(strip=True)
            print(f"Extracted business type: '{business_type}' from {url}")
            return business_type
        else:
            print(f"No business type found for {url}")
            return None
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return None

# Load the CSV file containing the business links
file_path = 'S_GROUP.csv'

try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit()

# Initialize a list to store business types
business_types = []

# Loop through each row to process the 'Business Link'
for index, row in data.iterrows():
    business_link = row.get('Business Link', None)
    
    # Check if the business link exists and is a valid string
    if isinstance(business_link, str) and business_link.startswith("http"):
        print(f"Processing business link: {business_link}")
        business_type = get_business_type(business_link)
        business_types.append(business_type)
    else:
        print(f"Invalid or missing business link at index {index}")
        business_types.append(None)

# Add the business type column to the dataframe
data['Business Type'] = business_types

# Save the updated dataframe to a new CSV file
output_file_path = 'S_GROUP_with_business_type.csv'
data.to_csv(output_file_path, index=False)

print(f"Updated data saved to {output_file_path}")
