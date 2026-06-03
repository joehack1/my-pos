# main.py - Main application file
import sqlite3
import datetime
import hashlib
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from decimal import Decimal

# -------------------------
# Theme system (4 themes)
# -------------------------
THEMES = {
    "Dark": {
        "root_bg": "#121212",
        "frame_bg": "#1E1E1E",
        "label_bg": "#121212",
        "label_fg": "#EAEAEA",
        "entry_bg": "#2A2A2A",
        "entry_fg": "#EAEAEA",
        "card_bg": "#1E1E1E",
        "labelframe_bg": "#1E1E1E",
        "labelframe_fg": "#EAEAEA",
        "accent": "#4CAF50",
        "accent2": "#2196F3",
        "danger": "#f44336",
        "warning": "#FF9800",
        "info": "#9C27B0",
        "tree_bg": "#1E1E1E",
        "tree_fg": "#EAEAEA",
        "tree_heading_bg": "#2A2A2A",
        "tree_heading_fg": "#EAEAEA",
        "tree_select_bg": "#3949AB",
    },
    "Light": {
        "root_bg": "#F5F5F5",
        "frame_bg": "#FFFFFF",
        "label_bg": "#F5F5F5",
        "label_fg": "#111111",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#111111",
        "card_bg": "#FFFFFF",
        "labelframe_bg": "#FFFFFF",
        "labelframe_fg": "#111111",
        "accent": "#4CAF50",
        "accent2": "#2196F3",
        "danger": "#f44336",
        "warning": "#FF9800",
        "info": "#9C27B0",
        "tree_bg": "#FFFFFF",
        "tree_fg": "#111111",
        "tree_heading_bg": "#E0E0E0",
        "tree_heading_fg": "#111111",
        "tree_select_bg": "#B3D4FC",
    },
    "Blue": {
        "root_bg": "#0B1B3A",
        "frame_bg": "#12315E",
        "label_bg": "#0B1B3A",
        "label_fg": "#EAF2FF",
        "entry_bg": "#163B70",
        "entry_fg": "#EAF2FF",
        "card_bg": "#12315E",
        "labelframe_bg": "#12315E",
        "labelframe_fg": "#EAF2FF",
        "accent": "#2E7DFF",
        "accent2": "#00BCD4",
        "danger": "#FF5252",
        "warning": "#FFC107",
        "info": "#7C4DFF",
        "tree_bg": "#12315E",
        "tree_fg": "#EAF2FF",
        "tree_heading_bg": "#1B3F78",
        "tree_heading_fg": "#EAF2FF",
        "tree_select_bg": "#1E5CBF",
    },
    "Mint": {
        "root_bg": "#06221C",
        "frame_bg": "#0B3A2E",
        "label_bg": "#06221C",
        "label_fg": "#E9FFF6",
        "entry_bg": "#0F4A39",
        "entry_fg": "#E9FFF6",
        "card_bg": "#0B3A2E",
        "labelframe_bg": "#0B3A2E",
        "labelframe_fg": "#E9FFF6",
        "accent": "#2ECC71",
        "accent2": "#1ABC9C",
        "danger": "#E74C3C",
        "warning": "#F39C12",
        "info": "#3498DB",
        "tree_bg": "#0B3A2E",
        "tree_fg": "#E9FFF6",
        "tree_heading_bg": "#11624E",
        "tree_heading_fg": "#E9FFF6",
        "tree_select_bg": "#2D9CDB",
    },
}


def apply_ttk_theme(style: ttk.Style, theme_name: str):
    t = THEMES[theme_name]

    # Treeview styling
    style.configure("Custom.Treeview",
                    background=t["tree_bg"],
                    foreground=t["tree_fg"],
                    fieldbackground=t["tree_bg"],
                    rowheight=24)

    style.configure("Custom.Treeview.Heading",
                    background=t["tree_heading_bg"],
                    foreground=t["tree_heading_fg"],
                    relief="flat")

    style.map("Custom.Treeview",
              background=[("selected", t["tree_select_bg"])],
              foreground=[("selected", t["tree_fg"])])

    # Combobox styling
    style.configure("Custom.TCombobox",
                    fieldbackground=t["entry_bg"],
                    background=t["entry_bg"],
                    foreground=t["entry_fg"],
                    bordercolor=t["tree_heading_bg"])

    # Labels via ttk are limited, but Treeview/Combobox will look consistent
    return



class Database:
    def __init__(self, db_name="mypos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        ''')
        
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                name TEXT NOT NULL,
                category_id INTEGER,
                price REAL NOT NULL,
                cost REAL,
                quantity INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 0,
                unit TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Sales table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_no TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                total REAL NOT NULL,
                paid REAL,
                change REAL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Sale items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Insert default admin user if not exists
        admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
        self.cursor.execute("INSERT OR IGNORE INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                           ("admin", admin_pass, "admin", "System Administrator"))
        
        # Insert default categories
        default_categories = ["Beverages", "Snacks", "Dairy", "Vegetables", "Fruits", "Cleaning", "Personal Care"]
        for cat in default_categories:
            self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
        
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor
    
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()

class LoginWindow:
    def __init__(self, root, theme_name="Dark"):
        self.root = root
        self.theme_name = theme_name
        self.root.title("myPOS - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.db = Database()
        
        # Center the window
        self.center_window()
        
        # Login frame
        self.login_frame = Frame(self.root, padx=20, pady=20)
        self.login_frame.pack(expand=True, fill=BOTH)
        
        # Title
        title_label = Label(self.login_frame, text="myPOS System", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Username
        Label(self.login_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=5)
        self.username_entry = Entry(self.login_frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=1, column=1, pady=5)
        self.username_entry.focus()
        
        # Password
        Label(self.login_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky=W, pady=5)
        self.password_entry = Entry(self.login_frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        # Login button
        login_btn = Button(self.login_frame, text="Login", font=("Arial", 12), command=self.login, 
                          bg=THEMES[self.theme_name]["accent"], fg="white", padx=20, pady=5)

        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        self.apply_login_theme(self.theme_name)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.login())

    def apply_login_theme(self, theme_name):
        t = THEMES[theme_name]
        self.root.configure(bg=t["root_bg"])
        self.login_frame.configure(bg=t["frame_bg"])

        for widget in self.login_frame.winfo_children():
            try:
                if isinstance(widget, Label):
                    widget.configure(bg=t["frame_bg"], fg=t["label_fg"])
                elif isinstance(widget, Entry):
                    widget.configure(
                        bg=t["entry_bg"],
                        fg=t["entry_fg"],
                        insertbackground=t["entry_fg"],
                        highlightbackground=t["tree_heading_bg"],
                        highlightcolor=t["accent"],
                    )
                elif isinstance(widget, Button):
                    widget.configure(activebackground=t["accent"], activeforeground="white")
            except TclError:
                pass
    
    def center_window(self):
        self.root.update_idletasks()
        width = 400
        height = 300
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        username = self.username_entry.get()
        password = hashlib.sha256(self.password_entry.get().encode()).hexdigest()
        
        user = self.db.fetch_one("SELECT id, username, role, full_name FROM users WHERE username=? AND password=?", 
                                 (username, password))
        
        if user:
            self.db.close()
            self.root.destroy()
            main_root = Tk()
            MainApp(main_root, user, self.theme_name)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

class MainApp:
    def __init__(self, root, user, theme_name="Dark"):
        self.root = root
        self.user = user
        self.user_id, self.username, self.role, self.full_name = user

        self.root.title(f"myPOS - {self.full_name} ({self.role})")
        self.root.geometry("1200x700")

        self.db = Database()
        self.cart = []

        # Theme state
        self.theme_name = theme_name
        self.style = ttk.Style(self.root)

        # Base tk background for login/main widgets
        self.root.configure(bg=THEMES[self.theme_name]["root_bg"])


        # Setup UI
        self.setup_menu()
        self.setup_main_interface()

        # Apply initial theme (after widgets exist)
        self.apply_theme(self.theme_name)

        # Load initial data
        self.load_categories()
        self.load_products()

    
    def setup_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Theme menu
        self.theme_var = StringVar(value=self.theme_name)
        theme_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        for name in THEMES.keys():
            theme_menu.add_radiobutton(
                label=name,
                value=name,
                variable=self.theme_var,
                command=lambda n=name: self.set_theme(n)
            )

        # File menu
        file_menu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Change Password", command=self.change_password)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Reports menu
        reports_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Daily Sales Report", command=self.daily_sales_report)
        reports_menu.add_command(label="Inventory Report", command=self.inventory_report)
        reports_menu.add_command(label="Sales History", command=self.sales_history)
        
        # Management menu (admin only)
        if self.role == "admin":
            manage_menu = Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Management", menu=manage_menu)
            manage_menu.add_command(label="User Management", command=self.user_management)
            manage_menu.add_command(label="Category Management", command=self.category_management)
    
    def apply_theme(self, theme_name: str):
        if theme_name not in THEMES:
            return
        self.theme_name = theme_name
        t = THEMES[theme_name]
        if hasattr(self, "theme_var"):
            self.theme_var.set(theme_name)

        # Root background
        self.root.configure(bg=t["root_bg"])

        # ttk themes (custom styles)
        apply_ttk_theme(self.style, theme_name)

        # Fill every Tk container/label area so the selected theme covers
        # whole panels instead of leaving default-gray gaps between widgets.
        self.apply_theme_to_widget(self.root, t)

    def apply_theme_to_widget(self, widget, t):
        try:
            if isinstance(widget, (Tk, Toplevel)):
                widget.configure(bg=t["root_bg"])
            elif isinstance(widget, LabelFrame):
                widget.configure(
                    bg=t["labelframe_bg"],
                    fg=t["labelframe_fg"],
                    highlightbackground=t["tree_heading_bg"],
                    highlightcolor=t["accent"],
                )
            elif isinstance(widget, Frame):
                widget.configure(bg=t["frame_bg"])
            elif isinstance(widget, Label):
                widget.configure(bg=t["frame_bg"], fg=t["label_fg"])
            elif isinstance(widget, Entry):
                widget.configure(
                    bg=t["entry_bg"],
                    fg=t["entry_fg"],
                    insertbackground=t["entry_fg"],
                    highlightbackground=t["tree_heading_bg"],
                    highlightcolor=t["accent"],
                )
            elif isinstance(widget, Button):
                color_role = self.get_theme_color_role(widget)
                if color_role:
                    widget.configure(bg=t[color_role], fg="white")
                widget.configure(activebackground=t["accent"], activeforeground="white")
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style="Custom.Treeview")
            elif isinstance(widget, ttk.Combobox):
                widget.configure(style="Custom.TCombobox")
        except TclError:
            pass

        for child in widget.winfo_children():
            self.apply_theme_to_widget(child, t)

    def get_theme_color_role(self, widget):
        try:
            current_rgb = widget.winfo_rgb(widget.cget("bg"))
        except TclError:
            return None

        for role in ("accent", "accent2", "danger", "warning", "info"):
            for theme in THEMES.values():
                try:
                    if current_rgb == widget.winfo_rgb(theme[role]):
                        return role
                except TclError:
                    continue
        return None

    def set_theme(self, theme_name: str):
        self.apply_theme(theme_name)

    def setup_main_interface(self):
        # Main container
        main_frame = Frame(self.root)

        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Products
        left_frame = Frame(main_frame, width=600)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        # Category filter
        filter_frame = LabelFrame(left_frame, text="Categories", padx=5, pady=5)
        filter_frame.pack(fill=X, pady=(0, 10))
        
        self.category_var = StringVar(value="All")
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, state="readonly", width=30)
        self.category_combo.pack(side=LEFT, padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.load_products())
        
        # Search
        search_frame = Frame(filter_frame)
        search_frame.pack(side=RIGHT)
        Label(search_frame, text="Search:").pack(side=LEFT)
        self.search_entry = Entry(search_frame, width=20)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_products())
        
        # Products list
        products_frame = LabelFrame(left_frame, text="Products", padx=5, pady=5)
        products_frame.pack(fill=BOTH, expand=True)
        
        # Product tree
        columns = ("ID", "Barcode", "Name", "Price", "Stock", "Unit")
        self.product_tree = ttk.Treeview(products_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            width = 50 if col == "ID" else 100 if col == "Barcode" else 150 if col == "Name" else 80
            self.product_tree.column(col, width=width)
        
        self.product_tree.pack(fill=BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient=VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Add to cart button
        add_btn = Button(left_frame, text="Add to Cart", command=self.add_to_cart, 
                        bg=THEMES[self.theme_name]["accent2"], fg="white", font=("Arial", 12), padx=20, pady=5)

        add_btn.pack(pady=10)
        
        # Bind double-click to add to cart
        self.product_tree.bind('<Double-Button-1>', lambda e: self.add_to_cart())
        
        # Right panel - Cart
        right_frame = Frame(main_frame, width=500)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        # Cart title
        cart_title = Label(right_frame, text="Shopping Cart", font=("Arial", 16, "bold"))
        cart_title.pack()
        
        # Cart items
        cart_frame = Frame(right_frame)
        cart_frame.pack(fill=BOTH, expand=True, pady=10)
        
        columns = ("ID", "Name", "Qty", "Price", "Total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            width = 40 if col == "ID" else 120 if col == "Name" else 70
            self.cart_tree.column(col, width=width)
        
        self.cart_tree.pack(side=LEFT, fill=BOTH, expand=True)

        cart_scroll = ttk.Scrollbar(cart_frame, orient=VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_scroll.set)
        cart_scroll.pack(side=RIGHT, fill=Y)

        # Cart control buttons
        btn_frame = Frame(right_frame)
        btn_frame.pack(fill=X, pady=5)
        
        Button(btn_frame, text="Remove Selected", command=self.remove_from_cart, 
               bg=THEMES[self.theme_name]["danger"], fg="white").pack(side=LEFT, padx=5)
        Button(btn_frame, text="Clear Cart", command=self.clear_cart, 
               bg=THEMES[self.theme_name]["warning"], fg="white").pack(side=LEFT, padx=5)
        Button(btn_frame, text="Update Quantity", command=self.update_quantity, 
               bg=THEMES[self.theme_name]["warning"], fg="white").pack(side=LEFT, padx=5)

        
        # Total and checkout
        total_frame = LabelFrame(right_frame, text="Order Summary", padx=10, pady=10)
        total_frame.pack(fill=X, pady=10)
        
        self.total_label = Label(total_frame, text="Total: $0.00", font=("Arial", 18, "bold"))
        self.total_label.pack()
        
        checkout_btn = Button(total_frame, text="Checkout", command=self.checkout,
                             bg=THEMES[self.theme_name]["accent"], fg="white", font=("Arial", 14), padx=40, pady=10)

        checkout_btn.pack(pady=10)
        
        # Status bar
        self.status_bar = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
    
    def load_categories(self):
        categories = self.db.fetch_all("SELECT name FROM categories ORDER BY name")
        category_list = ["All"] + [cat[0] for cat in categories]
        self.category_combo['values'] = category_list
    
    def load_products(self):
        # Clear current items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        category = self.category_var.get()
        search = self.search_entry.get()
        
        if category == "All":
            if search:
                query = """SELECT p.id, p.barcode, p.name, p.price, p.quantity, p.unit 
                          FROM products p 
                          WHERE p.name LIKE ? OR p.barcode LIKE ?
                          ORDER BY p.name"""
                params = (f"%{search}%", f"%{search}%")
            else:
                query = "SELECT id, barcode, name, price, quantity, unit FROM products ORDER BY name"
                params = ()
        else:
            if search:
                query = """SELECT p.id, p.barcode, p.name, p.price, p.quantity, p.unit 
                          FROM products p 
                          JOIN categories c ON p.category_id = c.id
                          WHERE c.name = ? AND (p.name LIKE ? OR p.barcode LIKE ?)
                          ORDER BY p.name"""
                params = (category, f"%{search}%", f"%{search}%")
            else:
                query = """SELECT p.id, p.barcode, p.name, p.price, p.quantity, p.unit 
                          FROM products p 
                          JOIN categories c ON p.category_id = c.id
                          WHERE c.name = ?
                          ORDER BY p.name"""
                params = (category,)
        
        products = self.db.fetch_all(query, params)
        
        for product in products:
            self.product_tree.insert("", END, values=product)
    
    def add_to_cart(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
        item = self.product_tree.item(selected[0])
        values = item['values']
        
        # Explicitly cast types to ensure arithmetic and comparisons work
        product_id = int(values[0])
        name = str(values[2])
        price = float(values[3])
        stock = int(values[4])
        
        if stock <= 0:
            messagebox.showwarning("Warning", f"{name} is out of stock!")
            return
        
        # Check if product already in cart
        for cart_item in self.cart:
            if cart_item['id'] == product_id:
                if cart_item['quantity'] + 1 > stock:
                    messagebox.showwarning("Warning", f"Only {stock} units available!")
                    return
                cart_item['quantity'] += 1
                cart_item['total'] = cart_item['quantity'] * cart_item['price']
                self.update_cart_display()
                self.update_total()
                self.status_bar.config(text=f"Added {name} to cart")
                return
        
        # Add new item to cart
        self.cart.append({
            'id': product_id,
            'name': name,
            'price': price,
            'quantity': 1,
            'total': price,
            'stock': stock
        })
        
        self.update_cart_display()
        self.update_total()
        self.status_bar.config(text=f"Added {name} to cart")
    
    def update_cart_display(self):
        # Clear cart tree
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add items from cart
        for idx, item in enumerate(self.cart):
            self.cart_tree.insert("", END, values=(idx+1, item['name'], item['quantity'], 
                                                   f"${item['price']:.2f}", f"${item['total']:.2f}"))
    
    def update_total(self):
        total = sum(item['total'] for item in self.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")
        return total
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove!")
            return
        
        index = int(self.cart_tree.item(selected[0])['values'][0]) - 1
        removed_item = self.cart.pop(index)
        self.update_cart_display()
        self.update_total()
        self.status_bar.config(text=f"Removed {removed_item['name']} from cart")
    
    def clear_cart(self):
        if self.cart and messagebox.askyesno("Confirm", "Clear entire cart?"):
            self.cart.clear()
            self.update_cart_display()
            self.update_total()
            self.status_bar.config(text="Cart cleared")
    
    def update_quantity(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to update!")
            return
        
        index = int(self.cart_tree.item(selected[0])['values'][0]) - 1
        item = self.cart[index]
        
        new_qty = simpledialog.askinteger("Update Quantity", f"Enter new quantity for {item['name']}:",
                                          initialvalue=item['quantity'], minvalue=1, maxvalue=item['stock'])
        
        if new_qty:
            item['quantity'] = new_qty
            item['total'] = item['quantity'] * item['price']
            self.update_cart_display()
            self.update_total()
            self.status_bar.config(text=f"Updated {item['name']} quantity to {new_qty}")
    
    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        # Create checkout window
        checkout_win = Toplevel(self.root)
        checkout_win.title("Checkout")
        checkout_win.geometry("400x300")
        checkout_win.transient(self.root)
        checkout_win.grab_set()
        
        # Center the window
        checkout_win.update_idletasks()
        x = (checkout_win.winfo_screenwidth() // 2) - (400 // 2)
        y = (checkout_win.winfo_screenheight() // 2) - (300 // 2)
        checkout_win.geometry(f'400x300+{x}+{y}')
        
        total = self.update_total()
        
        Label(checkout_win, text=f"Total Amount: ${total:.2f}", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Payment method
        Label(checkout_win, text="Payment Method:", font=("Arial", 12)).pack()
        payment_var = StringVar(value="Cash")
        payment_combo = ttk.Combobox(checkout_win, textvariable=payment_var, values=["Cash", "Card", "Mobile Payment"], state="readonly")
        payment_combo.pack(pady=5)
        
        # Amount paid
        Label(checkout_win, text="Amount Paid:", font=("Arial", 12)).pack(pady=(10,0))
        paid_entry = Entry(checkout_win, font=("Arial", 14), width=20)
        paid_entry.pack(pady=5)
        paid_entry.insert(0, f"{total:.2f}")
        
        change_label = Label(checkout_win, text="Change: $0.00", font=("Arial", 12))
        change_label.pack(pady=5)
        
        def calculate_change(*args):
            try:
                val = paid_entry.get()
                if not val:
                    val = "0"
                paid = float(val)
                change = paid - total
                change_label.config(text=f"Change: ${change:.2f}" if change >= 0 else f"Short: ${-change:.2f}")
            except:
                change_label.config(text="Change: $0.00")
        
        paid_entry.bind('<KeyRelease>', calculate_change)
        
        def complete_sale():
            try:
                paid = float(paid_entry.get())
                if paid < total:
                    messagebox.showerror("Error", "Insufficient payment amount!")
                    return
                
                change = paid - total
                payment_method = payment_var.get()
                
                # Generate invoice number
                invoice_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
                
                # Save sale
                self.db.execute_query("""
                    INSERT INTO sales (invoice_no, user_id, total, paid, change, payment_method)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (invoice_no, self.user_id, total, paid, change, payment_method))
                
                sale_id = self.db.cursor.lastrowid
                
                # Save sale items and update stock
                for item in self.cart:
                    self.db.execute_query("""
                        INSERT INTO sale_items (sale_id, product_id, quantity, price, total)
                        VALUES (?, ?, ?, ?, ?)
                    """, (sale_id, item['id'], item['quantity'], item['price'], item['total']))
                    
                    # Update stock
                    self.db.execute_query("""
                        UPDATE products SET quantity = quantity - ? WHERE id = ?
                    """, (item['quantity'], item['id']))
                
                # Generate receipt
                self.generate_receipt(invoice_no, sale_id)
                
                messagebox.showinfo("Success", f"Sale completed!\nInvoice: {invoice_no}\nChange: ${change:.2f}")
                
                # Clear cart and refresh products
                self.cart.clear()
                self.update_cart_display()
                self.update_total()
                self.load_products()
                checkout_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to complete sale: {str(e)}")
        
        Button(checkout_win, text="Complete Sale", command=complete_sale, 
               bg=THEMES[self.theme_name]["accent"], fg="white", font=("Arial", 12), padx=20, pady=10).pack(pady=20)

        self.apply_theme_to_widget(checkout_win, THEMES[self.theme_name])

    
    def generate_receipt(self, invoice_no, sale_id):
        # Get sale details
        sale = self.db.fetch_one("SELECT * FROM sales WHERE id=?", (sale_id,))
        items = self.db.fetch_all("""
            SELECT p.name, si.quantity, si.price, si.total 
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id=?
        """, (sale_id,))
        
        # Create PDF receipt
        filename = f"receipt_{invoice_no}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, alignment=1, spaceAfter=30)
        header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=12, alignment=1)
        
        # Header
        story.append(Paragraph("myPOS System", title_style))
        story.append(Paragraph("Your Store Name Here", header_style))
        story.append(Paragraph("123 Business Street, City", header_style))
        story.append(Paragraph("Tel: (555) 123-4567", header_style))
        story.append(Spacer(1, 20))
        
        # Receipt info
        story.append(Paragraph(f"Invoice: {invoice_no}", styles['Normal']))
        story.append(Paragraph(f"Date: {sale[6]}", styles['Normal']))
        story.append(Paragraph(f"Cashier: {self.full_name}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Items table
        data = [["Item", "Qty", "Price", "Total"]]
        for item in items:
            data.append([item[0], str(item[1]), f"${item[2]:.2f}", f"${item[3]:.2f}"])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Totals
        story.append(Paragraph(f"Total: ${sale[3]:.2f}", styles['Normal']))
        story.append(Paragraph(f"Paid: ${sale[4]:.2f}", styles['Normal']))
        story.append(Paragraph(f"Change: ${sale[5]:.2f}", styles['Normal']))
        story.append(Paragraph(f"Payment: {sale[7]}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("Thank you for shopping with us!", styles['Normal']))
        story.append(Paragraph("Have a great day!", styles['Normal']))
        
        doc.build(story)
        self.status_bar.config(text=f"Receipt saved: {filename}")

        # Automatically open the PDF for preview and printing (merged duplicate)
        try:
            os.startfile(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open receipt: {e}")
    
    def change_password(self):
        change_win = Toplevel(self.root)
        change_win.title("Change Password")
        change_win.geometry("300x200")
        change_win.transient(self.root)
        change_win.grab_set()
        
        Label(change_win, text="Current Password:").pack(pady=(20,5))
        current_entry = Entry(change_win, show="*")
        current_entry.pack()
        
        Label(change_win, text="New Password:").pack(pady=(10,5))
        new_entry = Entry(change_win, show="*")
        new_entry.pack()
        
        Label(change_win, text="Confirm Password:").pack(pady=(10,5))
        confirm_entry = Entry(change_win, show="*")
        confirm_entry.pack()
        
        def change():
            current_hash = hashlib.sha256(current_entry.get().encode()).hexdigest()
            user_check = self.db.fetch_one("SELECT id FROM users WHERE id=? AND password=?", (self.user_id, current_hash))
            
            if not user_check:
                messagebox.showerror("Error", "Current password is incorrect!")
                return
            
            if new_entry.get() != confirm_entry.get():
                messagebox.showerror("Error", "New passwords do not match!")
                return
            
            if len(new_entry.get()) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters!")
                return
            
            new_hash = hashlib.sha256(new_entry.get().encode()).hexdigest()
            self.db.execute_query("UPDATE users SET password=? WHERE id=?", (new_hash, self.user_id))
            messagebox.showinfo("Success", "Password changed successfully!")
            change_win.destroy()
        
        Button(change_win, text="Change Password", command=change, bg=THEMES[self.theme_name]["accent"], fg="white").pack(pady=20)
        self.apply_theme_to_widget(change_win, THEMES[self.theme_name])

    
    def daily_sales_report(self):
        report_win = Toplevel(self.root)
        report_win.title("Daily Sales Report")
        report_win.geometry("600x400")
        
        # Get today's sales
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        sales = self.db.fetch_all("""
            SELECT invoice_no, total, sale_date, payment_method, full_name
            FROM sales s
            JOIN users u ON s.user_id = u.id
            WHERE DATE(sale_date) = ?
            ORDER BY sale_date DESC
        """, (today,))
        
        # Display report
        tree = ttk.Treeview(report_win, columns=("Invoice", "Total", "Time", "Payment", "Cashier"), show="headings")
        for col in ("Invoice", "Total", "Time", "Payment", "Cashier"):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=10)

        scroll = ttk.Scrollbar(report_win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y, pady=10, padx=(0, 10))

        total_sales = 0
        for sale in sales:
            tree.insert("", END, values=(sale[0], f"${sale[1]:.2f}", sale[2][11:16], sale[3], sale[4]))
            total_sales += sale[1]
        
        Label(report_win, text=f"Total Sales Today: ${total_sales:.2f}", 
              font=("Arial", 14, "bold")).pack(pady=10)
        self.apply_theme_to_widget(report_win, THEMES[self.theme_name])
    
    def inventory_report(self):
        report_win = Toplevel(self.root)
        report_win.title("Inventory Report")
        report_win.geometry("800x500")
        
        # Get inventory data
        products = self.db.fetch_all("""
            SELECT p.name, c.name, p.price, p.quantity, p.min_stock, p.unit
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY c.name, p.name
        """)
        
        tree = ttk.Treeview(report_win, columns=("Product", "Category", "Price", "Stock", "Min Stock", "Unit", "Status"), show="headings")
        for col in ("Product", "Category", "Price", "Stock", "Min Stock", "Unit", "Status"):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=10)

        scroll = ttk.Scrollbar(report_win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y, pady=10, padx=(0, 10))
        
        low_stock_items = []
        for product in products:
            status = "Low Stock" if product[3] <= product[4] else "OK"
            if product[3] <= product[4]:
                low_stock_items.append(product[0])
            tree.insert("", END, values=(product[0], product[1], f"${product[2]:.2f}", 
                                        product[3], product[4], product[5], status))
        
        if low_stock_items:
            Label(report_win, text=f"⚠ Low Stock Items: {', '.join(low_stock_items)}", 
                  fg="red", font=("Arial", 10, "bold")).pack(pady=5)
                  fg=THEMES[self.theme_name]["danger"], font=("Arial", 10, "bold")).pack(pady=5)
        self.apply_theme_to_widget(report_win, THEMES[self.theme_name])
    
    def sales_history(self):
        history_win = Toplevel(self.root)
        history_win.title("Sales History")
        history_win.geometry("800x500")
        
        # Date filter
        filter_frame = Frame(history_win)
        filter_frame.pack(pady=10)
        
        Label(filter_frame, text="From:").pack(side=LEFT)
        from_date = Entry(filter_frame, width=12)
        from_date.pack(side=LEFT, padx=5)
        from_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
        
        Label(filter_frame, text="To:").pack(side=LEFT)
        to_date = Entry(filter_frame, width=12)
        to_date.pack(side=LEFT, padx=5)
        to_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
        
        tree = ttk.Treeview(history_win, columns=("Invoice", "Date", "Total", "Cashier", "Payment"), show="headings")
        for col in ("Invoice", "Date", "Total", "Cashier", "Payment"):
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=10)

        scroll = ttk.Scrollbar(history_win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y, pady=10, padx=(0, 10))
        
        def load_history():
            for item in tree.get_children():
                tree.delete(item)
            
            sales = self.db.fetch_all("""
                SELECT s.invoice_no, s.sale_date, s.total, u.full_name, s.payment_method
                FROM sales s
                JOIN users u ON s.user_id = u.id
                WHERE DATE(s.sale_date) BETWEEN ? AND ?
                ORDER BY s.sale_date DESC
            """, (from_date.get(), to_date.get()))
            
            for sale in sales:
                tree.insert("", END, values=(sale[0], sale[1][:19], f"${sale[2]:.2f}", sale[3], sale[4]))
        
        def reprint_receipt():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a sale to reprint!")
                return
            
            invoice_no = tree.item(selected[0])['values'][0]
            sale_record = self.db.fetch_one("SELECT id FROM sales WHERE invoice_no=?", (invoice_no,))
            if sale_record:
                self.generate_receipt(invoice_no, sale_record[0])
            else:
                messagebox.showerror("Error", "Sale record not found!")

        Button(filter_frame, text="Load Report", command=load_history, bg=THEMES[self.theme_name]["accent2"], fg="white").pack(side=LEFT, padx=10)
        Button(filter_frame, text="Reprint Selected", command=reprint_receipt, bg=THEMES[self.theme_name]["warning"], fg="white").pack(side=LEFT, padx=10)

        load_history()
        self.apply_theme_to_widget(history_win, THEMES[self.theme_name])
    
    def user_management(self):
        if self.role != "admin":
            messagebox.showerror("Error", "Access denied! Admin only.")
            return
        
        user_win = Toplevel(self.root)
        user_win.title("User Management")
        user_win.geometry("600x400")
        
        tree = ttk.Treeview(user_win, columns=("ID", "Username", "Role", "Full Name"), show="headings")
        for col in ("ID", "Username", "Role", "Full Name"):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=10)

        scroll = ttk.Scrollbar(user_win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y, pady=10, padx=(0, 10))

        def load_users():
            for item in tree.get_children():
                tree.delete(item)
            users = self.db.fetch_all("SELECT id, username, role, full_name FROM users")
            for user in users:
                tree.insert("", END, values=user)
        
        def add_user():
            add_win = Toplevel(user_win)
            add_win.title("Add User")
            add_win.geometry("300x300")
            
            Label(add_win, text="Username:").pack(pady=5)
            username_entry = Entry(add_win)
            username_entry.pack()
            
            Label(add_win, text="Password:").pack(pady=5)
            password_entry = Entry(add_win, show="*")
            password_entry.pack()
            
            Label(add_win, text="Role:").pack(pady=5)
            role_combo = ttk.Combobox(add_win, values=["admin", "cashier"], state="readonly")
            role_combo.pack()
            role_combo.set("cashier")
            
            Label(add_win, text="Full Name:").pack(pady=5)
            fullname_entry = Entry(add_win)
            fullname_entry.pack()
            
            def save_user():
                if not username_entry.get() or not password_entry.get():
                    messagebox.showerror("Error", "Username and password required!")
                    return
                
                password_hash = hashlib.sha256(password_entry.get().encode()).hexdigest()
                try:
                    self.db.execute_query("""
                        INSERT INTO users (username, password, role, full_name)
                        VALUES (?, ?, ?, ?)
                    """, (username_entry.get(), password_hash, role_combo.get(), fullname_entry.get()))
                    messagebox.showinfo("Success", "User added successfully!")
                    load_users()
                    add_win.destroy()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Username already exists!")
            
            Button(add_win, text="Save", command=save_user, bg=THEMES[self.theme_name]["accent"], fg="white").pack(pady=20)
            self.apply_theme_to_widget(add_win, THEMES[self.theme_name])

        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user to delete!")
                return
            
            user_id = tree.item(selected[0])['values'][0]
            if user_id == self.user_id:
                messagebox.showerror("Error", "Cannot delete your own account!")
                return
            
            if messagebox.askyesno("Confirm", "Delete this user?"):
                self.db.execute_query("DELETE FROM users WHERE id=?", (user_id,))
                load_users()
        
        Button(user_win, text="Add User", command=add_user, bg=THEMES[self.theme_name]["accent"], fg="white").pack(side=LEFT, padx=10, pady=10)
        Button(user_win, text="Delete User", command=delete_user, bg=THEMES[self.theme_name]["danger"], fg="white").pack(side=LEFT, padx=10, pady=10)

        
        load_users()
        self.apply_theme_to_widget(user_win, THEMES[self.theme_name])
    
    def category_management(self):
        if self.role != "admin":
            messagebox.showerror("Error", "Access denied! Admin only.")
            return
        
        cat_win = Toplevel(self.root)
        cat_win.title("Category Management")
        cat_win.geometry("400x300")
        
        tree = ttk.Treeview(cat_win, columns=("ID", "Name", "Description"), show="headings")
        for col in ("ID", "Name", "Description"):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0), pady=10)

        scroll = ttk.Scrollbar(cat_win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y, pady=10, padx=(0, 10))

        def load_categories():
            for item in tree.get_children():
                tree.delete(item)
            categories = self.db.fetch_all("SELECT id, name, description FROM categories")
            for cat in categories:
                tree.insert("", END, values=cat)
        
        def add_category():
            name = simpledialog.askstring("Add Category", "Category Name:")
            if name:
                desc = simpledialog.askstring("Add Category", "Description (optional):")
                try:
                    self.db.execute_query("INSERT INTO categories (name, description) VALUES (?, ?)", (name, desc or ""))
                    load_categories()
                    self.load_categories()  # Refresh main UI categories
                    messagebox.showinfo("Success", "Category added!")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Category already exists!")
        
        def delete_category():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a category to delete!")
                return
            
            cat_id = tree.item(selected[0])['values'][0]
            cat_name = tree.item(selected[0])['values'][1]
            
            # Check if category has products
            products = self.db.fetch_one("SELECT COUNT(*) FROM products WHERE category_id=?", (cat_id,))
            if products[0] > 0:
                messagebox.showerror("Error", f"Cannot delete '{cat_name}' because it has {products[0]} products!")
                return
            
            if messagebox.askyesno("Confirm", f"Delete category '{cat_name}'?"):
                self.db.execute_query("DELETE FROM categories WHERE id=?", (cat_id,))
                load_categories()
                self.load_categories()
        
        Button(cat_win, text="Add Category", command=add_category, bg=THEMES[self.theme_name]["accent"], fg="white").pack(side=LEFT, padx=10, pady=10)
        Button(cat_win, text="Delete Category", command=delete_category, bg=THEMES[self.theme_name]["danger"], fg="white").pack(side=LEFT, padx=10, pady=10)

        
        load_categories()
        self.apply_theme_to_widget(cat_win, THEMES[self.theme_name])
    
    def logout(self):
        if messagebox.askyesno("Confirm", "Logout?"):
            self.db.close()
            self.root.destroy()
            login_root = Tk()
            LoginWindow(login_root, self.theme_name)
            login_root.mainloop()

if __name__ == "__main__":
    root = Tk()
    LoginWindow(root, "Dark")
    root.mainloop()
