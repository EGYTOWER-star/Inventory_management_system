import streamlit as st
import sqlite3

# Database file
DB_FILE = "inventory.db"

# Set custom CSS for background and text styling
page_bg_img = '''
<style>
body {
    background-image: url("https://images.pexels.com/photos/1054218/pexels-photo-1054218.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #ffffff;
}
h1 {
    color: #FFD700;  /* Gold color */
    text-align: center;
}
.sidebar .sidebar-content {
    background-color: rgba(0, 0, 0, 0.7);
}
.stButton>button {
    color: #FFFFFF;
    background-color: #1E90FF;  /* Dodger blue */
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
}
.stTextInput>div>div>input {
    color: #000000;  /* Black input text */
    background-color: #FFFFFF;
    border-radius: 5px;
}
.stNumberInput>div>input {
    color: #000000;
    background-color: #FFFFFF;
    border-radius: 5px;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to create the database and products table
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       category TEXT,
                       quantity INTEGER,
                       price REAL,
                       low_threshold INTEGER)''')
    conn.commit()
    conn.close()

# Function to add a new product to the database
def add_product(name, category, quantity, price, low_threshold):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, category, quantity, price, low_threshold) VALUES (?, ?, ?, ?, ?)",
                   (name, category, quantity, price, low_threshold))
    conn.commit()
    conn.close()
    st.success("Product added successfully!")

# Function to remove a product from the database
def remove_product(product_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    st.success("Product removed successfully!")

# Function to get all products from the database
def view_products():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, quantity, price, low_threshold FROM products")
    products = cursor.fetchall()
    conn.close()
    
    if products:
        for product in products:
            st.write(f"**ID:** {product[0]}")  # Display product ID for removal
            st.write(f"**Name:** {product[1]}")
            st.write(f"**Category:** {product[2]}")
            st.write(f"**Quantity:** {product[3]}")
            st.write(f"**Price:** ${product[4]}")
            st.write(f"**Low Threshold:** {product[5]}")
            if product[3] <= product[5]:
                st.warning("**Low stock!** Consider restocking.")
            st.write("---")
    else:
        st.info("No products available.")

# Function to search products by name or category
def search_products(search_term):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, quantity, price, low_threshold FROM products WHERE name LIKE ? OR category LIKE ?",
                   (f'%{search_term}%', f'%{search_term}%'))
    products = cursor.fetchall()
    conn.close()
    return products

# Function to adjust stock
def adjust_stock(product_name, adjustment_amount):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = quantity + ? WHERE name = ?", (adjustment_amount, product_name))
    conn.commit()
    conn.close()
    st.success(f"Stock for '{product_name}' adjusted by {adjustment_amount}.")

# Function to create login
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        # Simple user authentication
        if username == "admin" and password == "password":  # Change this for production use!
            st.session_state['logged_in'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Streamlit UI
def main():
    st.title("Inventory Management System")
    
    # Create the database and table if they don't exist
    create_database()

    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login()
    else:
        menu = ["Add Product", "View Products", "Search Products", "Adjust Stock", "Remove Product"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Add Product":
            st.subheader("Add New Product")
            name = st.text_input("Product Name")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.01)
            low_threshold = st.number_input("Low Threshold", min_value=0, step=1)

            if st.button("Add Product"):
                add_product(name, category, quantity, price, low_threshold)

        elif choice == "View Products":
            st.subheader("Product List")
            view_products()

        elif choice == "Search Products":
            st.subheader("Search Products")
            search_term = st.text_input("Search by Name or Category")
            if st.button("Search"):
                products = search_products(search_term)
                if products:
                    for product in products:
                        st.write(f"**ID:** {product[0]}")
                        st.write(f"**Name:** {product[1]}")
                        st.write(f"**Category:** {product[2]}")
                        st.write(f"**Quantity:** {product[3]}")
                        st.write(f"**Price:** ${product[4]}")
                        st.write(f"**Low Threshold:** {product[5]}")
                        st.write("---")
                else:
                    st.info("No products found.")

        elif choice == "Adjust Stock":
            st.subheader("Adjust Stock")
            product_name = st.text_input("Product Name")
            adjustment_amount = st.number_input("Adjustment Amount", step=1)
            if st.button("Adjust Stock"):
                adjust_stock(product_name, adjustment_amount)

        elif choice == "Remove Product":
            st.subheader("Remove Product")
            product_id = st.number_input("Product ID", min_value=1, step=1)
            if st.button("Remove Product"):
                remove_product(product_id)

if __name__ == "__main__":
    main()
