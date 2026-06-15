# inventory_manager.py - Standalone inventory management tool
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from decimal import Decimal
import re

class InventoryManager:
    def __init__(self, db_path="mypos.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def add_product(self, name, barcode, category_id, price, cost, quantity, min_stock, unit):
        try:
            # Ensure values are stored with proper precision if needed
            price = float(Decimal(str(price)))
            cost = float(Decimal(str(cost)))
            self.cursor.execute("""
                INSERT INTO products (name, barcode, category_id, price, cost, quantity, min_stock, unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, barcode, category_id, price, cost, quantity, min_stock, unit))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product(self, product_id, **kwargs):
        if not kwargs:
            return
            
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key}=?")
            values.append(value)
        values.append(product_id)
        
        query = f"UPDATE products SET {', '.join(fields)} WHERE id=?"
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_product(self, product_id):
        # Check if product has been sold
        self.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE product_id=?", (product_id,))
        if self.cursor.fetchone()[0] > 0:
            return False
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()
        return True
    
    def get_low_stock_products(self):
        self.cursor.execute("""
            SELECT name, quantity, min_stock FROM products 
            WHERE quantity <= min_stock AND quantity > 0
        """)
        return self.cursor.fetchall()
    
    def get_out_of_stock_products(self):
        self.cursor.execute("SELECT name FROM products WHERE quantity = 0")
        return self.cursor.fetchall()
    
    def stock_adjustment(self, product_id, adjustment, reason):
        self.cursor.execute("UPDATE products SET quantity = quantity + ? WHERE id=?", (adjustment, product_id))
        self.conn.commit()
        # Log adjustment (you can add a stock_adjustments table for audit)
    
    def close(self):
        self.conn.close()