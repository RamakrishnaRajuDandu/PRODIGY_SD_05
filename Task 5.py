import requests
from bs4 import BeautifulSoup
import csv

def extract_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    
    
    for item in soup.select('.s-result-item'):
        name = item.select_one('.a-text-normal')
        price = item.select_one('.a-price-whole')
        rating = item.select_one('.a-icon-alt')

        if name and price and rating:
            product_info = {
                'name': name.get_text(strip=True),
                'price': price.get_text(strip=True),
                'rating': rating.get_text(strip=True)
            }
            products.append(product_info)

    return products

def save_to_csv(products, filename):
    keys = products[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)

def main():
    url = 'https://www.amazon.com/s?k=your+search+term'
    products = extract_product_info(url)
    if products:
        save_to_csv(products, 'products.csv')
        print(f"Extracted {len(products)} products and saved to products.csv")
    else:
        print("No products found or unable to extract data.")

if __name__ == "__main__":
    main()
