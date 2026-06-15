# setup_initial_data.py - Script to add sample products
import sqlite3
from main import Database

def setup_sample_products():
    db = Database()
    
    sample_products = [
        ("6901234567890", "Coca Cola 330ml", 1, 1.50, 0.80, 100, 20, "can"),
        ("6901234567891", "Pepsi 330ml", 1, 1.50, 0.80, 100, 20, "can"),
        ("6901234567892", "Lays Chips", 2, 2.00, 1.20, 50, 10, "bag"),
        ("6901234567893", "Pringles", 2, 3.50, 2.00, 30, 5, "can"),
        ("6901234567894", "Fresh Milk 1L", 3, 2.50, 1.80, 40, 10, "carton"),
        ("6901234567895", "Yogurt", 3, 1.20, 0.70, 60, 15, "cup"),
        ("6901234567896", "Tomatoes", 4, 2.00, 1.00, 30, 5, "kg"),
        ("6901234567897", "Potatoes", 4, 1.50, 0.80, 50, 10, "kg"),
        ("6901234567898", "Apples", 5, 3.00, 1.80, 40, 10, "kg"),
        ("6901234567899", "Bananas", 5, 2.00, 1.00, 60, 15, "bunch"),
        ("6901234567900", "Dish Soap", 6, 3.00, 1.50, 30, 5, "bottle"),
        ("6901234567901", "Laundry Detergent", 6, 8.00, 5.00, 20, 5, "box"),
        ("6901234567902", "Shampoo", 7, 5.00, 3.00, 25, 5, "bottle"),
        ("6901234567903", "Soap Bar", 7, 1.00, 0.50, 100, 20, "piece"),
        ("6901234567904", "Orange Juice 1L", 1, 2.50, 1.50, 35, 10, "carton"),
        ("6901234567905", "Doritos", 2, 2.50, 1.40, 45, 10, "bag"),
        ("6901234567906", "Cheese 200g", 3, 4.00, 2.50, 25, 5, "pack"),
        ("6901234567907", "Cucumbers", 4, 1.00, 0.50, 35, 8, "piece"),
        ("6901234567908", "Grapes 500g", 5, 3.50, 2.00, 20, 5, "pack"),
        ("6901234567909", "Toothpaste", 7, 3.50, 2.00, 40, 10, "tube"),
    ]
    
    for product in sample_products:
        try:
            db.execute_query("""
                INSERT INTO products (barcode, name, category_id, price, cost, quantity, min_stock, unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, product)
        except sqlite3.IntegrityError:
            print(f"Product {product[1]} already exists")
    
    print("Sample products added successfully!")
    db.close()

if __name__ == "__main__":
    setup_sample_products()