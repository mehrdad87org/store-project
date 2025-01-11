import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape eBay
def scrape_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for item in soup.find_all('div', class_='s-item__info'):
        try:
            # Extract title
            title_element = item.find('h3', class_='s-item__title')
            title = title_element.text if title_element else "No Title"

            # Extract price
            price_element = item.find('span', class_='s-item__price')
            price = price_element.text if price_element else "No Price"

            # Extract image URL
            image_element = item.find('img')
            image_url = image_element['src'] if image_element and 'src' in image_element.attrs else None

            # Extract product URL
            product_url_element = item.find('a', class_='s-item__link')
            product_url = product_url_element['href'] if product_url_element else "No URL"

            # Add product to the list only if it has a valid image URL
            if image_url:
                products.append({
                    'title': title,
                    'price': price,
                    'image_url': image_url,
                    'product_url': product_url
                })
        except Exception as e:
            st.warning(f"Error parsing an item: {e}")
            continue

    return products

# Streamlit App
st.title("Online Shop - Search Products on eBay")

# Search bar
query = st.text_input("Enter a product to search on eBay (e.g., iPhone):")

if query:
    st.write(f"Searching for '{query}' on eBay...")

    # Scrape eBay
    results = scrape_ebay(query)

    if results:
        st.write(f"Found {len(results)} results:")
        for product in results:
            # Display image only if the URL is valid
            if product['image_url']:
                st.image(product['image_url'], width=200)
            st.write(f"**Title:** {product['title']}")
            st.write(f"**Price:** {product['price']}")
            st.write(f"**Product URL:** [Link]({product['product_url']})")
            st.write("---")
    else:
        st.write("No results found.")
else:
    st.write("Please enter a search term to begin.")