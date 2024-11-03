# test_inventory_app.py

import pytest
import inventory_app  # Import the main app code

def test_add_product():
    """Test adding a product to the inventory."""
    # Test data
    product_id = "test_id"
    name = "Test Product"
    category = "Test Category"
    price = 10.0
    stock_quantity = 50
    
    # Add product
    result = inventory_app.add_product(product_id, name, category, price, stock_quantity)
    
    # Assertions
    assert result == "Product added!"
    assert product_id in inventory_app.products
    assert inventory_app.products[product_id]["name"] == name
    assert inventory_app.products[product_id]["category"] == category
    assert inventory_app.products[product_id]["price"] == price
    assert inventory_app.products[product_id]["stock_quantity"] == stock_quantity

def test_delete_product():
    """Test deleting a product from the inventory."""
    # Add product to delete
    product_id = "test_id"
    inventory_app.add_product(product_id, "Test Product", "Test Category", 10.0, 50)
    
    # Delete product
    result = inventory_app.delete_product(product_id)
    
    # Assertions
    assert result == "Product deleted!"
    assert product_id not in inventory_app.products
