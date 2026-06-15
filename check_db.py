import sqlite3
import os

print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir("."))

try:
    db = sqlite3.connect("mypos.db")
    cursor = db.cursor()

    print("\n--- CATEGORIES ---")
    cursor.execute("SELECT * FROM categories")
    for row in cursor.fetchall():
        print(row)

    print("\n--- PRODUCTS ---")
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print(f"Total products: {len(products)}")
    for row in products:
        print(row)

    db.close()
except Exception as e:
    print("Error:", e)
