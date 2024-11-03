import streamlit as st
import uuid
import pandas as pd

# Sample data (replace with database integration later)
products = {}

# User authentication (replace with a secure authentication method)
users = {
    "admin": {"password": "admin", "role": "admin"},
    "user": {"password": "user", "role": "user"},
}

def login():
    st.title("Inventory Management System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]
            st.success("Login successful! Please refresh the page.")
        else:
            st.error("Invalid username or password")

def add_product():
    st.subheader("Add Product")
    with st.form(key='add_product_form'):
        product_id = str(uuid.uuid4())  # Generate a unique product ID
        name = st.text_input('Product Name', max_chars=50)
        category = st.text_input('Category', max_chars=30)
        price = st.number_input('Price', min_value=0.0, format="%.2f")
        stock_quantity = st.number_input('Stock Quantity', min_value=0, step=1)
        submit_button = st.form_submit_button('Add Product')

        if submit_button:
            products[product_id] = {
                'name': name,
                'category': category,
                'price': price,
                'stock_quantity': stock_quantity
            }
            st.success(f'Product "{name}" added successfully!')

def view_products():
    st.subheader("View Products")
    if products:
        product_list = pd.DataFrame.from_dict(products, orient='index')
        st.dataframe(product_list)  # Display products in a table
    else:
        st.write("No products available.")

def search_products():
    st.subheader("Search Products")
    search_term = st.text_input("Enter product name or category to search:")
    filtered_products = {pid: details for pid, details in products.items() if 
                         search_term.lower() in details['name'].lower() or 
                         search_term.lower() in details['category'].lower()}
    
    if filtered_products:
        st.write("Search Results:")
        product_list = pd.DataFrame.from_dict(filtered_products, orient='index')
        st.dataframe(product_list)
    else:
        st.write("No matching products found.")

def main():
    if "logged_in" not in st.session_state:
        login()
        return  # Stop further execution until logged in

    st.title("Inventory Management System")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode", ["Add Product", "View Products", "Search Products"])

    st.write(f"Welcome, {st.session_state['username']} ({st.session_state['role']})")

    if app_mode == "Add Product":
        if st.session_state["role"] == "admin":
            add_product()
        else:
            st.warning("You do not have permission to add products.")
    elif app_mode == "View Products":
        view_products()
    elif app_mode == "Search Products":
        search_products()

if __name__ == "__main__":
    main()
