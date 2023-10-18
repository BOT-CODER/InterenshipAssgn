import requests
import csv
from bs4 import BeautifulSoup

# Read product URLs from the previously scraped CSV file
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}
product_urls = []
with open('products_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    product_urls = [row[0] for row in reader]

# Initialize an empty list to store additional product information
product_details = []

# Loop through product URLs and scrape additional information
for product_url in product_urls:
    response = requests.get(product_url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract additional product information
    description = soup.find('meta', {'name': 'description'})['content']
    product_description = soup.find('div', {'id': 'productDescription'})
    product_description = product_description.text.strip() if product_description else 'N/A'

    # Extract ASIN and Manufacturer using different approach
    asin = 'N/A'
    manufacturer = 'N/A'
    for row in soup.find_all('tr', {'class': 'a-spacing-small'}):
        header = row.find('th', {'class': 'a-span3'})
        if header and 'ASIN' in header.text:
            asin = row.find('td', {'class': 'a-span9'}).text.strip()
        elif header and 'Brand' in header.text:
            manufacturer = row.find('td', {'class': 'a-span9'}).text.strip()

    # Add the scraped data to the product_details list
    product_details.append([description, asin, product_description, manufacturer])

# Save the additional scraped data to a new CSV file
with open('product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Description', 'ASIN', 'Product Description', 'Manufacturer'])
    csv_writer.writerows(product_details)
