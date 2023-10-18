import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from time import sleep

# Initialize VAR
seconds = 0
products_data = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

# Loop through 20 pages of product listing
for page_number in tqdm(range(1, 21)):
    try:
        # Delay the Request for more Accuracy
        sleep(seconds)
        url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_number}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract product information
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        for product in products:
            product_link = product.find('a', {'class': 'a-link-normal s-no-outline'})
            if product_link:
                product_url = "https://www.amazon.in" + product_link['href']
                product_name = product.find('span', {'class': 'a-text-normal'}).text.strip()
                product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
                rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
                num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()
                # Update product informatuon
                products_data.append([product_url, product_name, product_price, rating, num_reviews])
            else:
                print("Product link not found for a product. Skipping...")
                continue
    except Exception as error:
        print(f"Error: {e}")
# Save the scraped data to a CSV file
with open('products_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
    csv_writer.writerows(products_data)
print("File saved as 'products_data.csv'.")
