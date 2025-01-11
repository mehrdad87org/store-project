import requests
from bs4 import BeautifulSoup
import sqlite3

def fetch_html(url):
    headers = {
        "User-Agent": "Your User Agent",
        "Accept-Language": "en-US, en;q=0.5"
    }
    response = requests.get(url, headers=headers)
    return response.content

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all("div", class_="s-item__info")
    images = soup.find_all("div", class_="s-item__image-wrapper image-treatment")
    
    items = []
    for product, img in zip(products, images):
        title = product.select_one('.s-item__title').text if product.select_one('.s-item__title') else "N/A"
        link = product.select_one('.s-item__link')['href'] if product.select_one('.s-item__link') else "N/A"
        price = product.select_one('.s-item__price').text if product.select_one('.s-item__price') else "N/A"
        img_tag = img.find("img")
        img_url = img_tag['src'] if img_tag else "N/A"
        properties = " ".join([prop.text for prop in product.select('.s-item__subtitle')])
        items.append((link, title, price, properties, img_url))
    return items

def store_data(database, data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      link TEXT, 
                      title TEXT, 
                      price TEXT, 
                      properties TEXT,
                      img TEXT)''')

    # Remove the first two items and shift others
    if len(data) > 2:
        data = data[2:]
        if len(data) > 0:
            data.insert(0, data.pop(0)) 
            data.insert(0, data.pop(0))
            

    cursor.executemany('INSERT INTO products (link, title, price, properties, img) VALUES (?,?,?,?,?)', data)
    conn.commit()
    conn.close()

def main():
    base_url = "https://www.ebay.com/sch/i.html?_nkw="
    search_query = "iphone"
    url = f"{base_url}{search_query}"
    html = fetch_html(url)
    products = parse_html(html)
    store_data('products.db', products)
    print("Data stored successfully!")

if __name__ == "__main__":
    main()
