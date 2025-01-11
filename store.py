import streamlit as st
import sqlite3
import pandas as pd

def fetch_product_data():
    conn = sqlite3.connect('products.db')
    query = '''SELECT link, title, price, img FROM products'''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(layout="wide")
    st.title("Online Shop")
    st.header("Products")

    products = fetch_product_data()

    items_per_page = 4
    total_pages = max((len(products) + items_per_page - 1) // items_per_page, 1)
    page_number = st.session_state.get('page_number', 1)

    start_idx = (page_number - 1) * items_per_page
    end_idx = start_idx + items_per_page

    for idx in range(start_idx, min(end_idx, len(products))):
        product = products.iloc[idx]
        col1, col2 = st.columns([2, 5])
        with col1:
            st.image(product['img'], width=200)  # Increased image width
        with col2:
            st.markdown(f"### {product['title']}")  # Larger title text
            st.markdown(f"**Price:** {product['price']}")  # Larger price text
            st.markdown(
                f'<a target="_blank" href="{product["link"]}" style="text-decoration:none"><div style="display:inline-block;background-color:blue;color:black;padding:10px;border-radius:5px;">View on eBay</div></a>',
                unsafe_allow_html=True
            )
        st.write("---")  # Adds horizontal line for spacing and separation

    st.write("")
    st.write("")

    col_blank1, col_prev, col_blank2, col_next, col_blank3 = st.columns([2, 1, 4, 1, 2])

    with col_prev:
        if page_number > 1 and st.button("Previous Page", key="prev"):
            st.session_state.page_number = page_number - 1

    with col_next:
        if page_number < total_pages and st.button("Next Page", key="next"):
            st.session_state.page_number = page_number + 1

    st.write("")
    st.write("")
    page_number = st.slider("Page", 1, total_pages, page_number, key="slider")

if __name__ == "__main__":
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    main()
