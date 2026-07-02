# main.py — myPOS Liquid Glass Edition
# Requires: pip install reportlab
 
import sqlite3
import datetime
import hashlib
import os
import math
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
 
# ─────────────────────────────────────────────
#  THEMES
# ─────────────────────────────────────────────
THEMES = {
    "Liquid Glass": {
        # backgrounds
        "shell":        "#D4DCFF",   # outermost gradient proxy
        "panel":        "#E8EEFF",   # glass panel
        "panel_hover":  "#F0F4FF",
        "card":         "#EEF2FF",
        "card_hover":   "#F5F8FF",
        "input_bg":     "#F2F5FF",
        "sidebar":      "#E2E8FF",

        # borders
        "border":       "#C0CAFF",
        "border_light": "#D8DEFF",

        # text
        "txt":          "#1A1A3A",
        "txt2":         "#5A5A8A",
        "txt3":         "#9898C0",
        "txt_white":    "#FFFFFF",

        # accents
        "accent":       "#5E6FFF",
        "accent_dark":  "#4050DD",
        "accent_light": "#8090FF",
        "accent2":      "#A78BFA",
        "green":        "#10B981",
        "green_bg":     "#D1FAE5",
        "red":          "#EF4444",
        "red_bg":       "#FEE2E2",
        "amber":        "#F59E0B",
        "amber_bg":     "#FEF3C7",
        "info_bg":      "#EFF6FF",
        "info":         "#3B82F6",

        # special
        "checkout_btn": "#5E6FFF",
        "topbar":       "#DDE5FF",
        "status_dot":   "#10B981",
        "scrollbar":    "#C8D0FF",
    },
    "Dark": {
        "shell":        "#121212",
        "panel":        "#1E1E1E",
        "panel_hover":  "#2A2A2A",
        "card":         "#1E1E1E",
        "card_hover":   "#2A2A2A",
        "input_bg":     "#2A2A2A",
        "sidebar":      "#1E1E1E",
        "border":       "#333333",
        "border_light": "#444444",
        "txt":          "#EAEAEA",
        "txt2":         "#AAAAAA",
        "txt3":         "#777777",
        "txt_white":    "#FFFFFF",
        "accent":       "#4CAF50",
        "accent_dark":  "#388E3C",
        "accent_light": "#66BB6A",
        "accent2":      "#2196F3",
        "green":        "#4CAF50",
        "green_bg":     "#1B5E20",
        "red":          "#F44336",
        "red_bg":       "#B71C1C",
        "amber":        "#FF9800",
        "amber_bg":     "#E65100",
        "info_bg":      "#0D47A1",
        "info":         "#2196F3",
        "checkout_btn": "#4CAF50",
        "topbar":       "#1E1E1E",
        "status_dot":   "#4CAF50",
        "scrollbar":    "#333333",
    },
    "Light": {
        "shell":        "#F5F5F5",
        "panel":        "#FFFFFF",
        "panel_hover":  "#E0E0E0",
        "card":         "#FFFFFF",
        "card_hover":   "#F0F0F0",
        "input_bg":     "#FFFFFF",
        "sidebar":      "#F0F0F0",
        "border":       "#E0E0E0",
        "border_light": "#F0F0F0",
        "txt":          "#111111",
        "txt2":         "#555555",
        "txt3":         "#999999",
        "txt_white":    "#FFFFFF",
        "accent":       "#4CAF50",
        "accent_dark":  "#388E3C",
        "accent_light": "#66BB6A",
        "accent2":      "#2196F3",
        "green":        "#4CAF50",
        "green_bg":     "#D1FAE5",
        "red":          "#F44336",
        "red_bg":       "#FEE2E2",
        "amber":        "#FF9800",
        "amber_bg":     "#FEF3C7",
        "info_bg":      "#E3F2FD",
        "info":         "#2196F3",
        "checkout_btn": "#4CAF50",
        "topbar":       "#F5F5F5",
        "status_dot":   "#4CAF50",
        "scrollbar":    "#E0E0E0",
    },
    "Blue": {
        "shell":        "#0B1B3A",
        "panel":        "#12315E",
        "panel_hover":  "#1A4A8A",
        "card":         "#12315E",
        "card_hover":   "#1A4A8A",
        "input_bg":     "#163B70",
        "sidebar":      "#12315E",
        "border":       "#1A4A8A",
        "border_light": "#2A6ACC",
        "txt":          "#EAF2FF",
        "txt2":         "#A0C0FF",
        "txt3":         "#6080CC",
        "txt_white":    "#FFFFFF",
        "accent":       "#2E7DFF",
        "accent_dark":  "#1A5CCC",
        "accent_light": "#5E97FF",
        "accent2":      "#00BCD4",
        "green":        "#00BCD4",
        "green_bg":     "#004D40",
        "red":          "#FF5252",
        "red_bg":       "#B71C1C",
        "amber":        "#FFC107",
        "amber_bg":     "#E65100",
        "info_bg":      "#0D47A1",
        "info":         "#2E7DFF",
        "checkout_btn": "#2E7DFF",
        "topbar":       "#12315E",
        "status_dot":   "#00BCD4",
        "scrollbar":    "#1A4A8A",
    },
    "Mint": {
        "shell":        "#06221C",
        "panel":        "#0B3A2E",
        "panel_hover":  "#125544",
        "card":         "#0B3A2E",
        "card_hover":   "#125544",
        "input_bg":     "#0F4A39",
        "sidebar":      "#0B3A2E",
        "border":       "#125544",
        "border_light": "#1A7755",
        "txt":          "#E9FFF6",
        "txt2":         "#A0E0CC",
        "txt3":         "#60AA88",
        "txt_white":    "#FFFFFF",
        "accent":       "#2ECC71",
        "accent_dark":  "#1A9944",
        "accent_light": "#58D68D",
        "accent2":      "#1ABC9C",
        "green":        "#2ECC71",
        "green_bg":     "#1A5533",
        "red":          "#E74C3C",
        "red_bg":       "#7F1D1D",
        "amber":        "#F39C12",
        "amber_bg":     "#8B4513",
        "info_bg":      "#0D3D28",
        "info":         "#1ABC9C",
        "checkout_btn": "#2ECC71",
        "topbar":       "#0B3A2E",
        "status_dot":   "#2ECC71",
        "scrollbar":    "#125544",
    }
}

# Current active theme
current_theme_name = "Liquid Glass"
G = THEMES[current_theme_name]
 
# Map roles used in buttons so theme engine can remap them
ROLE_COLORS = {
    "accent":  G["accent"],
    "accent2": G["info"],
    "danger":  G["red"],
    "warning": G["amber"],
    "info":    G["accent2"],
}
 
# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
 
def blend(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g_val = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g_val:02x}{b:02x}"
 
def rounded_rect(canvas, x1, y1, x2, y2, r=12, **kwargs):
    """Draw a rounded rectangle on a Canvas widget."""
    pts = [
        x1+r, y1, x2-r, y1,
        x2, y1, x2, y1+r,
        x2, y2-r, x2, y2,
        x2-r, y2, x1+r, y2,
        x1, y2, x1, y2-r,
        x1, y1+r, x1, y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)
 
def style_entry(e):
    e.config(bg=G["input_bg"], fg=G["txt"], insertbackground=G["accent"],
              relief=FLAT, highlightthickness=1,
              highlightbackground=G["border"], highlightcolor=G["accent"])
 
def style_button(b, role="accent"):
    color = ROLE_COLORS.get(role, G["accent"])
    b.config(bg=color, fg=G["txt_white"], activebackground=G["accent_dark"],
             activeforeground=G["txt_white"], relief=FLAT, cursor="hand2",
             bd=0, highlightthickness=0)
 
def apply_scrollbar(sb):
    sb.config(bg=G["scrollbar"], troughcolor=G["panel"],
              activebackground=G["accent"], relief=FLAT, bd=0, width=6,
              highlightthickness=0)
 
# ─────────────────────────────────────────────
#  DATABASE
# ─────────────────────────────────────────────
class Database:
    def __init__(self, db_name="mypos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
 
    def create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
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
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_no TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                total REAL NOT NULL,
                paid REAL,
                change REAL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        ''')
        admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (username, password, role, full_name) VALUES (?,?,?,?)",
            ("admin", admin_pass, "admin", "System Administrator"))
        for cat in ["Beverages", "Snacks", "Dairy", "Vegetables", "Fruits", "Cleaning", "Personal Care"]:
            self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
        self.conn.commit()
 
    def execute_query(self, q, p=()):
        self.cursor.execute(q, p)
        self.conn.commit()
        return self.cursor
 
    def fetch_all(self, q, p=()):
        self.cursor.execute(q, p)
        return self.cursor.fetchall()
 
    def fetch_one(self, q, p=()):
        self.cursor.execute(q, p)
        return self.cursor.fetchone()
 
    def close(self):
        self.conn.close()
 
# ─────────────────────────────────────────────
#  TTK STYLE SETUP
# ─────────────────────────────────────────────
def setup_ttk_style(style: ttk.Style, theme):
    try:
        style.theme_use('clam')
    except Exception:
        pass

    style.configure("Glass.Treeview",
                    background=theme["card"],
                    foreground=theme["txt"],
                    fieldbackground=theme["card"],
                    rowheight=28,
                    font=("Segoe UI", 10))
    style.configure("Glass.Treeview.Heading",
                    background=theme["topbar"],
                    foreground=theme["txt"],
                    font=("Segoe UI", 10, "bold"),
                    relief="flat")
    style.map("Glass.Treeview",
              background=[("selected", theme["accent"])],
              foreground=[("selected", "#FFFFFF")])

    style.configure("Glass.TCombobox",
                    fieldbackground=theme["input_bg"],
                    background=theme["input_bg"],
                    foreground=theme["txt"],
                    selectbackground=theme["accent"],
                    selectforeground="#FFFFFF",
                    bordercolor=theme["border"],
                    arrowcolor=theme["accent"])
    style.map("Glass.TCombobox",
              fieldbackground=[("readonly", theme["input_bg"])],
              foreground=[("readonly", theme["txt"])])

    style.configure("GlassV.TScrollbar",
                    background=theme["scrollbar"],
                    troughcolor=theme["panel"],
                    arrowcolor=theme["accent"],
                    relief=FLAT, bd=0)
    style.configure("Vertical.GlassV.TScrollbar",
                    background=theme["scrollbar"],
                    troughcolor=theme["panel"],
                    arrowcolor=theme["accent"],
                    relief=FLAT, bd=0)
    style.configure("GlassH.TScrollbar",
                    background=theme["scrollbar"],
                    troughcolor=theme["panel"],
                    arrowcolor=theme["accent"],
                    relief=FLAT, bd=0)
    style.configure("Horizontal.GlassH.TScrollbar",
                    background=theme["scrollbar"],
                    troughcolor=theme["panel"],
                    arrowcolor=theme["accent"],
                    relief=FLAT, bd=0)


def apply_theme_to_widget(widget, theme):
    """Recursively apply theme to a widget and all its children"""
    try:
        # Configure widget based on type
        if isinstance(widget, (Tk, Toplevel)):
            widget.configure(bg=theme["shell"])
        elif isinstance(widget, Frame):
            widget.configure(bg=theme["panel"])
        elif isinstance(widget, Label):
            widget.configure(bg=theme["panel"], fg=theme["txt"])
        elif isinstance(widget, Entry):
            widget.configure(
                bg=theme["input_bg"],
                fg=theme["txt"],
                insertbackground=theme["accent"],
                highlightbackground=theme["border"],
                highlightcolor=theme["accent"]
            )
        elif isinstance(widget, Button):
            # Keep track of button's original role if possible, but for now use accent
            widget.configure(
                bg=theme["accent"],
                fg=theme["txt_white"],
                activebackground=theme["accent_dark"],
                activeforeground=theme["txt_white"]
            )
    except Exception:
        pass

    # Recursively apply to children
    for child in widget.winfo_children():
        apply_theme_to_widget(child, theme)
 
# ─────────────────────────────────────────────
#  GLASS FRAME WIDGET
# ─────────────────────────────────────────────
class GlassFrame(Frame):
    """A Frame that draws a rounded glass panel behind its children."""
    def __init__(self, parent, radius=14, bg_color=None, border_color=None,
                 highlight_top=True, **kwargs):
        self.radius = radius
        self.bg_color = bg_color or G["panel"]
        self.border_color = border_color or G["border"]
        self.highlight_top = highlight_top
 
        super().__init__(parent, bg=self.bg_color, **kwargs)
        self.bind("<Configure>", self._redraw)
 
    def _redraw(self, event=None):
        pass  # Tkinter Frame handles its own bg; canvas overlays are in subclass
 
 
class GlassCard(Frame):
    """Card widget with subtle top-highlight border."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent,
                         bg=G["card"],
                         highlightbackground=G["border_light"],
                         highlightthickness=1,
                         **kwargs)
 
 
# ─────────────────────────────────────────────
#  ANIMATED TOAST
# ─────────────────────────────────────────────
class Toast:
    def __init__(self, root):
        self.root = root
        self._after_id = None
        self.lbl = Label(root, text="", font=("Segoe UI", 11, "bold"),
                         bg=G["txt"], fg="#FFFFFF", padx=20, pady=10,
                         relief=FLAT, bd=0)
 
    def show(self, msg, duration=1800):
        self.lbl.config(text=msg)
        self.lbl.place(relx=0.5, rely=0.93, anchor=CENTER)
        self.lbl.lift()
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self._after_id = self.root.after(duration, self._hide)
 
    def _hide(self):
        self.lbl.place_forget()
 
# ─────────────────────────────────────────────
#  LOGIN WINDOW
# ─────────────────────────────────────────────
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("myPOS — Liquid Glass")
        self.root.geometry("460x360")
        self.root.resizable(False, False)
        self.root.configure(bg=G["shell"])
        self.db = Database()
        self._center(460, 360)
        self._build()
 
    def _center(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
 
    def _build(self):
        # Background gradient strips
        for i in range(20):
            t = i / 19
            c = blend(G["shell"], "#C8D8FF", t)
            Frame(self.root, bg=c, height=18).pack(fill=X)
 
        # Glass card
        card = Frame(self.root, bg=G["panel"],
                     highlightbackground=G["border"], highlightthickness=1,
                     padx=36, pady=32)
        card.place(relx=0.5, rely=0.5, anchor=CENTER, width=360, height=300)
 
        # Logo row
        logo_f = Frame(card, bg=G["panel"])
        logo_f.pack(pady=(0, 18))
        dot = Canvas(logo_f, width=12, height=12, bg=G["panel"],
                     highlightthickness=0)
        dot.pack(side=LEFT, padx=(0, 6), pady=3)
        dot.create_oval(0, 0, 12, 12, fill=G["accent"], outline="")
        Label(logo_f, text="myPOS", font=("Segoe UI", 22, "bold"),
              bg=G["panel"], fg=G["txt"]).pack(side=LEFT)
 
        # Fields
        for label_text, attr, show in [
            ("Username", "user_entry", ""),
            ("Password", "pass_entry", "•"),
        ]:
            f = Frame(card, bg=G["panel"])
            f.pack(fill=X, pady=5)
            Label(f, text=label_text, font=("Segoe UI", 10),
                  bg=G["panel"], fg=G["txt2"], width=9, anchor=W).pack(side=LEFT)
            e = Entry(f, font=("Segoe UI", 12), show=show, relief=FLAT,
                      bg=G["input_bg"], fg=G["txt"], insertbackground=G["accent"],
                      highlightbackground=G["border"], highlightthickness=1,
                      highlightcolor=G["accent"])
            e.pack(side=LEFT, fill=X, expand=True, ipady=6, padx=4)
            setattr(self, attr, e)
 
        self.user_entry.focus()
 
        # Login button
        btn = Button(card, text="Sign In →", font=("Segoe UI", 12, "bold"),
                     command=self.login, relief=FLAT, cursor="hand2",
                     bg=G["accent"], fg="#FFFFFF",
                     activebackground=G["accent_dark"], activeforeground="#FFFFFF",
                     bd=0, padx=24, pady=10)
        btn.pack(pady=(20, 0), ipadx=10)
 
        # Hint
        Label(card, text="Default: admin / admin123",
              font=("Segoe UI", 9), bg=G["panel"], fg=G["txt3"]).pack(pady=(8, 0))
 
        self.root.bind('<Return>', lambda _: self.login())
 
    def login(self):
        username = self.user_entry.get().strip()
        password = hashlib.sha256(self.pass_entry.get().encode()).hexdigest()
        user = self.db.fetch_one(
            "SELECT id, username, role, full_name FROM users WHERE username=? AND password=?",
            (username, password))
        if user:
            self.db.close()
            self.root.destroy()
            r = Tk()
            MainApp(r, user)
            r.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
 
# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class MainApp:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.user_id, self.username, self.role, self.full_name = user
        self.root.title(f"myPOS  ·  {self.full_name}")
        self.root.geometry("1280x760")
        self.root.configure(bg=G["shell"])
        self.root.minsize(1100, 680)

        self.db = Database()
        self.cart = []
        self.pay_method = StringVar(value="Cash")
        self._active_cat = "All"  # Initialize early!
        self.current_theme_name = current_theme_name
        self.style = ttk.Style(self.root)
        setup_ttk_style(self.style, G)

        self._center(1280, 760)
        self.toast = Toast(self.root)

        self._build_menu()
        self._build_ui()
        self._load_categories()
        self._load_products()
    
    def switch_theme(self, theme_name):
        """Switch to a new theme"""
        global G, current_theme_name
        
        # Update global variables
        current_theme_name = theme_name
        G = THEMES[theme_name]
        self.current_theme_name = theme_name
        
        # Update ROLE_COLORS
        ROLE_COLORS["accent"] = G["accent"]
        ROLE_COLORS["accent2"] = G["info"]
        ROLE_COLORS["danger"] = G["red"]
        ROLE_COLORS["warning"] = G["amber"]
        ROLE_COLORS["info"] = G["accent2"]
        
        # Update ttk styles
        setup_ttk_style(self.style, G)
        
        # Apply theme to all widgets
        apply_theme_to_widget(self.root, G)
        
        # Reload UI components that depend on theme
        self._load_products()
 
    def _center(self, w, h):
        self.root.update_idletasks()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
 
    # ── MENU ──────────────────────────────────
    def _build_menu(self):
        mb = Menu(self.root, bg=G["topbar"], fg=G["txt"],
                  activebackground=G["accent"], activeforeground="#FFF",
                  relief=FLAT, bd=0)
        self.root.config(menu=mb)
 
        file_m = Menu(mb, tearoff=0, bg=G["panel"], fg=G["txt"],
                      activebackground=G["accent"], activeforeground="#FFF")
        mb.add_cascade(label="File", menu=file_m)
        file_m.add_command(label="Change Password", command=self._change_password)
        file_m.add_separator()
        file_m.add_command(label="Logout", command=self._logout)
        file_m.add_command(label="Exit", command=self.root.quit)
 
        rep_m = Menu(mb, tearoff=0, bg=G["panel"], fg=G["txt"],
                     activebackground=G["accent"], activeforeground="#FFF")
        mb.add_cascade(label="Reports", menu=rep_m)
        rep_m.add_command(label="Daily Sales", command=self._daily_sales)
        rep_m.add_command(label="Inventory", command=self._inventory_report)
        rep_m.add_command(label="Sales History", command=self._sales_history)
 
        if self.role == "admin":
            mgmt_m = Menu(mb, tearoff=0, bg=G["panel"], fg=G["txt"],
                          activebackground=G["accent"], activeforeground="#FFF")
            mb.add_cascade(label="Management", menu=mgmt_m)
            mgmt_m.add_command(label="Users", command=self._user_management)
            mgmt_m.add_command(label="Categories", command=self._category_management)
            mgmt_m.add_command(label="Products", command=self._product_management)
 
    # ── MAIN UI ───────────────────────────────
    def _build_ui(self):
        # Top bar
        topbar = Frame(self.root, bg=G["topbar"], height=52)
        topbar.pack(fill=X, padx=12, pady=(10, 0))
        topbar.pack_propagate(False)

        # Brand
        brand_f = Frame(topbar, bg=G["topbar"])
        brand_f.pack(side=LEFT, padx=16, pady=10)
        dot_c = Canvas(brand_f, width=10, height=10, bg=G["topbar"], highlightthickness=0)
        dot_c.pack(side=LEFT, padx=(0, 6), pady=2)
        dot_c.create_oval(0, 0, 10, 10, fill=G["accent"], outline="")
        Label(brand_f, text="myPOS", font=("Segoe UI", 16, "bold"),
              bg=G["topbar"], fg=G["txt"]).pack(side=LEFT)

        # Status dot
        status_f = Frame(topbar, bg=G["topbar"], highlightbackground=G["border"],
                         highlightthickness=1)
        status_f.pack(side=LEFT, padx=16, pady=14)
        dot2 = Canvas(status_f, width=8, height=8, bg=G["topbar"], highlightthickness=0)
        dot2.pack(side=LEFT, padx=(6, 4), pady=1)
        dot2.create_oval(0, 0, 8, 8, fill=G["green"], outline="")
        Label(status_f, text="Online", font=("Segoe UI", 9),
              bg=G["topbar"], fg=G["txt2"]).pack(side=LEFT, padx=(0, 6))

        # Right side info
        right_f = Frame(topbar, bg=G["topbar"])
        right_f.pack(side=RIGHT, padx=16, pady=8)
        
        # Theme selector
        theme_f = Frame(right_f, bg=G["topbar"])
        theme_f.pack(side=RIGHT, padx=8)
        self.theme_var = StringVar(value=self.current_theme_name)
        theme_combo = ttk.Combobox(theme_f, textvariable=self.theme_var,
                                  values=list(THEMES.keys()), state="readonly",
                                  width=12, style="Glass.TCombobox")
        theme_combo.pack(side=LEFT, pady=2)
        theme_combo.bind("<<ComboboxSelected>>", 
                         lambda e: self.switch_theme(self.theme_var.get()))
        
        now = datetime.datetime.now().strftime("%d %b %Y  %H:%M")
        Label(right_f, text=now, font=("Segoe UI", 9),
              bg=G["topbar"], fg=G["txt2"]).pack(side=RIGHT, padx=8)
        initials = "".join(w[0].upper() for w in self.full_name.split()[:2])
        avatar = Label(right_f, text=initials, font=("Segoe UI", 10, "bold"),
                       bg=G["accent"], fg="#FFF", width=3, height=1)
        avatar.pack(side=RIGHT)
        Label(right_f, text=self.full_name, font=("Segoe UI", 10),
              bg=G["topbar"], fg=G["txt"]).pack(side=RIGHT, padx=8)
 
        # Body
        body = Frame(self.root, bg=G["shell"])
        body.pack(fill=BOTH, expand=True, padx=12, pady=10)
 
        # LEFT — product browser
        self._build_left(body)
        # RIGHT — cart
        self._build_right(body)
 
        # Status bar
        self.status_var = StringVar(value="Ready")
        sb = Label(self.root, textvariable=self.status_var,
                   font=("Segoe UI", 9), bg=G["topbar"], fg=G["txt2"],
                   anchor=W, padx=12, pady=4)
        sb.pack(fill=X, side=BOTTOM)
 
    def _build_left(self, parent):
        lf = Frame(parent, bg=G["shell"])
        lf.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))
 
        # Search bar
        search_panel = Frame(lf, bg=G["panel"],
                             highlightbackground=G["border"], highlightthickness=1)
        search_panel.pack(fill=X, pady=(0, 8))
 
        search_inner = Frame(search_panel, bg=G["panel"])
        search_inner.pack(fill=X, padx=12, pady=10)
 
        Label(search_inner, text="⌕", font=("Segoe UI", 14),
              bg=G["panel"], fg=G["txt2"]).pack(side=LEFT, padx=(0, 6))
 
        self.search_var = StringVar()
        se = Entry(search_inner, textvariable=self.search_var,
                   font=("Segoe UI", 12), relief=FLAT,
                   bg=G["input_bg"], fg=G["txt"],
                   insertbackground=G["accent"],
                   highlightbackground=G["border"], highlightthickness=1,
                   highlightcolor=G["accent"])
        se.pack(side=LEFT, fill=X, expand=True, ipady=7, padx=4)
        se.insert(0, "Search products...")
        se.bind("<FocusIn>", lambda e: (se.delete(0, END) if se.get() == "Search products..." else None))
        se.bind("<FocusOut>", lambda e: (se.insert(0, "Search products...") if not se.get() else None))
        self.search_var.trace_add("write", lambda *_: self._load_products())
 
        # Barcode label
        Label(search_inner, text="Barcode ▸", font=("Segoe UI", 9),
              bg=G["panel"], fg=G["txt3"]).pack(side=RIGHT, padx=8)
        self.barcode_var = StringVar()
        be = Entry(search_inner, textvariable=self.barcode_var,
                   font=("Segoe UI", 11), relief=FLAT, width=14,
                   bg=G["input_bg"], fg=G["txt"],
                   insertbackground=G["accent"],
                   highlightbackground=G["border"], highlightthickness=1,
                   highlightcolor=G["accent"])
        be.pack(side=RIGHT, ipady=7)
        be.bind("<Return>", self._barcode_lookup)
 
        # Category pills
        self.cat_frame = Frame(lf, bg=G["shell"])
        self.cat_frame.pack(fill=X, pady=(0, 8))
 
        # Product treeview panel
        prod_panel = Frame(lf, bg=G["panel"],
                           highlightbackground=G["border"], highlightthickness=1)
        prod_panel.pack(fill=BOTH, expand=True)
 
        header = Frame(prod_panel, bg=G["topbar"])
        header.pack(fill=X)
        Label(header, text="Products", font=("Segoe UI", 11, "bold"),
              bg=G["topbar"], fg=G["txt"], padx=14, pady=8).pack(side=LEFT)
        self.prod_count_lbl = Label(header, text="", font=("Segoe UI", 9),
                                    bg=G["topbar"], fg=G["txt2"])
        self.prod_count_lbl.pack(side=RIGHT, padx=14)
 
        cols = ("ID", "Barcode", "Name", "Category", "Price", "Stock", "Unit")
        tree_f = Frame(prod_panel, bg=G["panel"])
        tree_f.pack(fill=BOTH, expand=True, padx=8, pady=8)
 
        self.prod_tree = ttk.Treeview(tree_f, columns=cols, show="headings",
                                      style="Glass.Treeview", height=16,
                                      selectmode="browse")
        widths = {"ID": 40, "Barcode": 100, "Name": 200, "Category": 100,
                  "Price": 70, "Stock": 60, "Unit": 60}
        for col in cols:
            self.prod_tree.heading(col, text=col)
            self.prod_tree.column(col, width=widths[col], stretch=(col == "Name"))
 
        # Alternate row colors
        self.prod_tree.tag_configure("odd", background=G["card"])
        self.prod_tree.tag_configure("even", background=G["panel"])
        self.prod_tree.tag_configure("low", foreground=G["red"])
 
        vsb = ttk.Scrollbar(tree_f, orient=VERTICAL, command=self.prod_tree.yview)
        self.prod_tree.configure(yscrollcommand=vsb.set)
        self.prod_tree.pack(side=LEFT, fill=BOTH, expand=True)
        vsb.pack(side=RIGHT, fill=Y)
 
        self.prod_tree.bind("<Double-Button-1>", lambda _: self._add_to_cart())
        self.prod_tree.bind("<Return>", lambda _: self._add_to_cart())
 
        # Add to cart button
        btn_row = Frame(lf, bg=G["shell"])
        btn_row.pack(fill=X, pady=(8, 0))
        add_btn = Button(btn_row, text="＋  Add to Cart",
                         font=("Segoe UI", 11, "bold"),
                         command=self._add_to_cart,
                         bg=G["info"], fg="#FFF",
                         activebackground=G["accent_dark"],
                         activeforeground="#FFF",
                         relief=FLAT, cursor="hand2",
                         bd=0, pady=10)
        add_btn.pack(fill=X)
 
    def _build_right(self, parent):
        rf = Frame(parent, bg=G["shell"], width=360)
        rf.pack(side=RIGHT, fill=BOTH)
        rf.pack_propagate(False)
 
        # Cart panel
        cart_panel = Frame(rf, bg=G["panel"],
                           highlightbackground=G["border"], highlightthickness=1)
        cart_panel.pack(fill=BOTH, expand=True)
 
        # Cart header
        ch = Frame(cart_panel, bg=G["topbar"])
        ch.pack(fill=X)
        Label(ch, text="🛒  Cart", font=("Segoe UI", 12, "bold"),
              bg=G["topbar"], fg=G["txt"], padx=14, pady=10).pack(side=LEFT)
        self.cart_count_lbl = Label(ch, text="0 items",
                                    font=("Segoe UI", 9, "bold"),
                                    bg=G["accent"], fg="#FFF",
                                    padx=10, pady=4)
        self.cart_count_lbl.pack(side=RIGHT, padx=12, pady=8)
 
        # Cart tree
        cart_tree_f = Frame(cart_panel, bg=G["panel"])
        cart_tree_f.pack(fill=BOTH, expand=True, padx=8, pady=8)
 
        ccols = ("#", "Name", "Qty", "Price", "Total")
        self.cart_tree = ttk.Treeview(cart_tree_f, columns=ccols, show="headings",
                                      style="Glass.Treeview", height=10,
                                      selectmode="browse")
        cwidths = {"#": 28, "Name": 140, "Qty": 40, "Price": 65, "Total": 70}
        for col in ccols:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=cwidths[col], stretch=(col == "Name"))
 
        self.cart_tree.tag_configure("odd", background=G["card"])
        self.cart_tree.tag_configure("even", background=G["panel"])
 
        cvsb = ttk.Scrollbar(cart_tree_f, orient=VERTICAL, command=self.cart_tree.yview,
                             style="GlassV.TScrollbar")
        self.cart_tree.configure(yscrollcommand=cvsb.set)
        self.cart_tree.pack(side=LEFT, fill=BOTH, expand=True)
        cvsb.pack(side=RIGHT, fill=Y)
 
        # Cart buttons
        cbf = Frame(cart_panel, bg=G["panel"])
        cbf.pack(fill=X, padx=8, pady=(0, 6))
 
        for txt, cmd, role in [
            ("✕ Remove", self._remove_from_cart, G["red"]),
            ("⟳ Qty", self._update_quantity, G["amber"]),
            ("✕ Clear", self._clear_cart, G["txt2"]),
        ]:
            Button(cbf, text=txt, font=("Segoe UI", 9, "bold"),
                   command=cmd, bg=role, fg="#FFF",
                   activebackground=G["accent_dark"], activeforeground="#FFF",
                   relief=FLAT, cursor="hand2", bd=0, padx=10, pady=6).pack(
                side=LEFT, padx=(0, 4))
 
        # Separator
        Frame(cart_panel, bg=G["border"], height=1).pack(fill=X, padx=8)
 
        # Totals
        totals_f = Frame(cart_panel, bg=G["panel"])
        totals_f.pack(fill=X, padx=14, pady=10)
 
        self.subtotal_lbl = self._total_row(totals_f, "Subtotal", "$0.00")
        self.tax_lbl      = self._total_row(totals_f, "Tax (16%)", "$0.00")
        Frame(totals_f, bg=G["border"], height=1).pack(fill=X, pady=6)
        self.grand_lbl    = self._total_row(totals_f, "TOTAL", "$0.00",
                                            big=True, color=G["accent"])
 
        # Payment method
        Frame(cart_panel, bg=G["border"], height=1).pack(fill=X, padx=8)
        pm_f = Frame(cart_panel, bg=G["panel"])
        pm_f.pack(fill=X, padx=12, pady=8)
        Label(pm_f, text="Payment", font=("Segoe UI", 9, "bold"),
              bg=G["panel"], fg=G["txt2"]).pack(anchor=W, pady=(0, 4))
 
        pay_btns_f = Frame(pm_f, bg=G["panel"])
        pay_btns_f.pack(fill=X)
        self.pay_btns = {}
        for method, icon in [("Cash", "💵"), ("Card", "💳"),
                              ("Mobile", "📱"), ("Crypto", "₿")]:
            b = Button(pay_btns_f, text=f"{icon} {method}",
                       font=("Segoe UI", 9, "bold"),
                       command=lambda m=method: self._select_pay(m),
                       relief=FLAT, cursor="hand2", bd=0,
                       padx=8, pady=6)
            b.pack(side=LEFT, padx=(0, 4))
            self.pay_btns[method] = b
        self._select_pay("Cash")
 
        # Checkout button
        self.checkout_btn = Button(cart_panel,
                                   text="Charge $0.00  →",
                                   font=("Segoe UI", 13, "bold"),
                                   command=self._checkout,
                                   bg=G["accent"], fg="#FFF",
                                   activebackground=G["accent_dark"],
                                   activeforeground="#FFF",
                                   relief=FLAT, cursor="hand2",
                                   bd=0, pady=14)
        self.checkout_btn.pack(fill=X, padx=12, pady=(4, 12))
 
    def _total_row(self, parent, label, value, big=False, color=None):
        f = Frame(parent, bg=G["panel"])
        f.pack(fill=X, pady=2)
        font_l = ("Segoe UI", 11 if big else 9, "bold" if big else "normal")
        font_v = ("Segoe UI", 14 if big else 10, "bold")
        Label(f, text=label, font=font_l,
              bg=G["panel"], fg=G["txt"] if big else G["txt2"]).pack(side=LEFT)
        lbl = Label(f, text=value, font=font_v,
                    bg=G["panel"], fg=color or G["txt"])
        lbl.pack(side=RIGHT)
        return lbl
 
    def _select_pay(self, method):
        self.pay_method.set(method)
        for m, b in self.pay_btns.items():
            if m == method:
                b.config(bg=G["accent"], fg="#FFF")
            else:
                b.config(bg=G["card"], fg=G["txt2"])
 
    # ── CATEGORIES ────────────────────────────
    def _load_categories(self):
        cats = self.db.fetch_all("SELECT name FROM categories ORDER BY name")
        self._cat_list = ["All"] + [c[0] for c in cats]
        self._active_cat = "All"
 
        for w in self.cat_frame.winfo_children():
            w.destroy()
 
        for cat in self._cat_list:
            active = (cat == self._active_cat)
            b = Button(self.cat_frame,
                       text=cat,
                       font=("Segoe UI", 9, "bold" if active else "normal"),
                       relief=FLAT, cursor="hand2", bd=0,
                       padx=12, pady=5,
                       command=lambda c=cat: self._select_cat(c))
            if active:
                b.config(bg=G["accent"], fg="#FFF")
            else:
                b.config(bg=G["panel"], fg=G["txt2"],
                         activebackground=G["card"], activeforeground=G["txt"])
            b.pack(side=LEFT, padx=(0, 4))
 
    def _select_cat(self, cat):
        self._active_cat = cat
        self._load_categories()
        self._load_products()
 
    # ── PRODUCTS ──────────────────────────────
    def _load_products(self, *_):
        for item in self.prod_tree.get_children():
            self.prod_tree.delete(item)

        raw_search = self.search_var.get()
        search = "" if raw_search == "Search products..." else raw_search.strip()
        cat = self._active_cat

        if cat == "All":
            if search:
                q = """SELECT p.id, p.barcode, p.name, c.name, p.price, p.quantity, p.unit
                       FROM products p LEFT JOIN categories c ON p.category_id = c.id
                       WHERE p.name LIKE ? OR p.barcode LIKE ? ORDER BY p.name"""
                rows = self.db.fetch_all(q, (f"%{search}%", f"%{search}%"))
            else:
                q = """SELECT p.id, p.barcode, p.name, c.name, p.price, p.quantity, p.unit
                       FROM products p LEFT JOIN categories c ON p.category_id = c.id
                       ORDER BY p.name"""
                rows = self.db.fetch_all(q)
        else:
            if search:
                q = """SELECT p.id, p.barcode, p.name, c.name, p.price, p.quantity, p.unit
                       FROM products p JOIN categories c ON p.category_id = c.id
                       WHERE c.name=? AND (p.name LIKE ? OR p.barcode LIKE ?) ORDER BY p.name"""
                rows = self.db.fetch_all(q, (cat, f"%{search}%", f"%{search}%"))
            else:
                q = """SELECT p.id, p.barcode, p.name, c.name, p.price, p.quantity, p.unit
                       FROM products p JOIN categories c ON p.category_id = c.id
                       WHERE c.name=? ORDER BY p.name"""
                rows = self.db.fetch_all(q, (cat,))

        for i, row in enumerate(rows):
            tag = "odd" if i % 2 else "even"
            tags = [tag]
            if row[5] is not None and row[5] <= 3:
                tags.append("low")
            self.prod_tree.insert("", END, values=row, tags=tags)

        self.prod_count_lbl.config(text=f"{len(rows)} products")
 
    def _barcode_lookup(self, event=None):
        bc = self.barcode_var.get().strip()
        if not bc:
            return
        row = self.db.fetch_one(
            "SELECT id FROM products WHERE barcode=?", (bc,))
        if row:
            for item in self.prod_tree.get_children():
                if self.prod_tree.item(item)["values"][0] == row[0]:
                    self.prod_tree.selection_set(item)
                    self.prod_tree.focus(item)
                    self._add_to_cart()
                    self.barcode_var.set("")
                    return
        else:
            self.toast.show(f"Barcode not found: {bc}")
        self.barcode_var.set("")
 
    # ── CART ──────────────────────────────────
    def _add_to_cart(self):
        sel = self.prod_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a product first.")
            return
        vals = self.prod_tree.item(sel[0])["values"]
        pid   = int(vals[0])
        name  = str(vals[2])
        price = float(vals[4])
        stock = int(vals[5]) if vals[5] is not None else 0
 
        if stock <= 0:
            messagebox.showwarning("Out of Stock", f"{name} is out of stock.")
            return
 
        for item in self.cart:
            if item["id"] == pid:
                if item["qty"] + 1 > stock:
                    messagebox.showwarning("Stock Limit", f"Only {stock} units available.")
                    return
                item["qty"] += 1
                item["total"] = item["qty"] * item["price"]
                self._refresh_cart()
                self.toast.show(f"+ {name}")
                return
 
        self.cart.append({"id": pid, "name": name, "price": price,
                          "qty": 1, "total": price, "stock": stock})
        self._refresh_cart()
        self.toast.show(f"Added {name}")
 
    def _refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        for i, it in enumerate(self.cart):
            tag = "odd" if i % 2 else "even"
            self.cart_tree.insert("", END,
                values=(i+1, it["name"], it["qty"],
                        f"${it['price']:.2f}", f"${it['total']:.2f}"),
                tags=(tag,))
        self._update_totals()
 
    def _update_totals(self):
        subtotal = sum(i["total"] for i in self.cart)
        tax      = subtotal * 0.16
        grand    = subtotal + tax
 
        self.subtotal_lbl.config(text=f"${subtotal:.2f}")
        self.tax_lbl.config(text=f"${tax:.2f}")
        self.grand_lbl.config(text=f"${grand:.2f}")
        self.checkout_btn.config(text=f"Charge ${grand:.2f}  →")
        n = sum(i["qty"] for i in self.cart)
        self.cart_count_lbl.config(text=f"{n} item{'s' if n != 1 else ''}")
        self.status_var.set(f"Cart: {n} items  |  Total: ${grand:.2f}")
        return grand
 
    def _remove_from_cart(self):
        sel = self.cart_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a cart item first.")
            return
        idx = int(self.cart_tree.item(sel[0])["values"][0]) - 1
        removed = self.cart.pop(idx)
        self._refresh_cart()
        self.toast.show(f"Removed {removed['name']}")
 
    def _clear_cart(self):
        if self.cart and messagebox.askyesno("Clear Cart", "Remove all items?"):
            self.cart.clear()
            self._refresh_cart()
            self.toast.show("Cart cleared")
 
    def _update_quantity(self):
        sel = self.cart_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a cart item first.")
            return
        idx  = int(self.cart_tree.item(sel[0])["values"][0]) - 1
        item = self.cart[idx]
        new_qty = simpledialog.askinteger(
            "Update Qty", f"New quantity for {item['name']}:",
            initialvalue=item["qty"], minvalue=1, maxvalue=item["stock"])
        if new_qty:
            item["qty"]   = new_qty
            item["total"] = new_qty * item["price"]
            self._refresh_cart()
            self.toast.show(f"Updated {item['name']} → {new_qty}")
 
    # ── CHECKOUT ──────────────────────────────
    def _checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add items before checkout.")
            return
 
        win = Toplevel(self.root)
        win.title("Checkout")
        win.geometry("420x340")
        win.resizable(False, False)
        win.configure(bg=G["shell"])
        win.transient(self.root)
        win.grab_set()
        self._center_win(win, 420, 340)
 
        grand = self._update_totals()
 
        panel = Frame(win, bg=G["panel"],
                      highlightbackground=G["border"], highlightthickness=1,
                      padx=28, pady=24)
        panel.place(relx=0.5, rely=0.5, anchor=CENTER, width=380, height=300)
 
        Label(panel, text="Complete Sale", font=("Segoe UI", 14, "bold"),
              bg=G["panel"], fg=G["txt"]).pack(pady=(0, 16))
 
        # Total display
        total_card = Frame(panel, bg=G["card"],
                           highlightbackground=G["border_light"], highlightthickness=1)
        total_card.pack(fill=X, pady=(0, 14))
        Label(total_card, text=f"${grand:.2f}", font=("Segoe UI", 28, "bold"),
              bg=G["card"], fg=G["accent"], pady=8).pack()
        Label(total_card, text=f"Payment: {self.pay_method.get()}",
              font=("Segoe UI", 10), bg=G["card"], fg=G["txt2"]).pack(pady=(0, 8))
 
        # Amount paid
        row = Frame(panel, bg=G["panel"])
        row.pack(fill=X, pady=4)
        Label(row, text="Amount Paid:", font=("Segoe UI", 10),
              bg=G["panel"], fg=G["txt2"]).pack(side=LEFT)
        paid_e = Entry(row, font=("Segoe UI", 13), width=14, relief=FLAT,
                       bg=G["input_bg"], fg=G["txt"],
                       insertbackground=G["accent"],
                       highlightbackground=G["border"], highlightthickness=1,
                       highlightcolor=G["accent"])
        paid_e.pack(side=RIGHT, ipady=6)
        paid_e.insert(0, f"{grand:.2f}")
 
        change_lbl = Label(panel, text="Change: $0.00",
                           font=("Segoe UI", 11, "bold"),
                           bg=G["panel"], fg=G["green"])
        change_lbl.pack(pady=4)
 
        def calc_change(*_):
            try:
                paid = float(paid_e.get())
                diff = paid - grand
                if diff >= 0:
                    change_lbl.config(text=f"Change: ${diff:.2f}", fg=G["green"])
                else:
                    change_lbl.config(text=f"Short: ${-diff:.2f}", fg=G["red"])
            except ValueError:
                change_lbl.config(text="Change: —", fg=G["txt3"])
 
        paid_e.bind("<KeyRelease>", calc_change)
        calc_change()
 
        def complete():
            try:
                paid = float(paid_e.get())
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount.", parent=win)
                return
            if paid < grand:
                messagebox.showerror("Error", "Insufficient payment.", parent=win)
                return
            change = paid - grand
            inv_no = f"INV-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
            self.db.execute_query(
                "INSERT INTO sales (invoice_no, user_id, total, paid, change, payment_method) VALUES (?,?,?,?,?,?)",
                (inv_no, self.user_id, grand, paid, change, self.pay_method.get()))
            sale_id = self.db.cursor.lastrowid
            for it in self.cart:
                self.db.execute_query(
                    "INSERT INTO sale_items (sale_id, product_id, quantity, price, total) VALUES (?,?,?,?,?)",
                    (sale_id, it["id"], it["qty"], it["price"], it["total"]))
                self.db.execute_query(
                    "UPDATE products SET quantity = quantity - ? WHERE id=?",
                    (it["qty"], it["id"]))
            self._generate_receipt(inv_no, sale_id)
            self.cart.clear()
            self._refresh_cart()
            self._load_products()
            win.destroy()
            self.toast.show(f"✓ Sale complete — Change ${change:.2f}")
            messagebox.showinfo("Sale Complete",
                                f"Invoice: {inv_no}\nChange: ${change:.2f}")
 
        Button(panel, text=f"Complete Sale  →",
               font=("Segoe UI", 12, "bold"),
               command=complete,
               bg=G["accent"], fg="#FFF",
               activebackground=G["accent_dark"], activeforeground="#FFF",
               relief=FLAT, cursor="hand2", bd=0, pady=10).pack(fill=X, pady=(10, 0))
 
    # ── RECEIPT ───────────────────────────────
    def _generate_receipt(self, invoice_no, sale_id):
        sale  = self.db.fetch_one("SELECT * FROM sales WHERE id=?", (sale_id,))
        items = self.db.fetch_all(
            """SELECT p.name, si.quantity, si.price, si.total
               FROM sale_items si JOIN products p ON si.product_id = p.id
               WHERE si.sale_id=?""", (sale_id,))
 
        filename = f"receipt_{invoice_no}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        title_s = ParagraphStyle("T", parent=styles["Heading1"], fontSize=22,
                                  alignment=1, spaceAfter=20)
        sub_s   = ParagraphStyle("S", parent=styles["Normal"], fontSize=11,
                                  alignment=1, spaceAfter=4)
        story = [
            Paragraph("myPOS", title_s),
            Paragraph("Your Store Name", sub_s),
            Paragraph("123 Business Street · (555) 123-4567", sub_s),
            Spacer(1, 16),
            Paragraph(f"Invoice: {invoice_no}", styles["Normal"]),
            Paragraph(f"Date: {sale[6]}", styles["Normal"]),
            Paragraph(f"Cashier: {self.full_name}", styles["Normal"]),
            Paragraph(f"Payment: {sale[7]}", styles["Normal"]),
            Spacer(1, 16),
        ]
        data = [["Item", "Qty", "Unit Price", "Total"]]
        for it in items:
            data.append([it[0], str(it[1]), f"${it[2]:.2f}", f"${it[3]:.2f}"])
        tbl = Table(data, colWidths=[220, 60, 100, 100])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#5E6FFF")),
            ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
            ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,0), 11),
            ("BOTTOMPADDING",(0,0),(-1,0), 10),
            ("BACKGROUND",  (0,1), (-1,-1), colors.HexColor("#F0F4FF")),
            ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#C0CAFF")),
            ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 16))
        story += [
            Paragraph(f"Subtotal: ${sale[3]/1.16:.2f}", styles["Normal"]),
            Paragraph(f"Tax (16%): ${sale[3] - sale[3]/1.16:.2f}", styles["Normal"]),
            Paragraph(f"<b>Total: ${sale[3]:.2f}</b>", styles["Normal"]),
            Paragraph(f"Paid: ${sale[4]:.2f}", styles["Normal"]),
            Paragraph(f"Change: ${sale[5]:.2f}", styles["Normal"]),
            Spacer(1, 20),
            Paragraph("Thank you for shopping with us!", styles["Normal"]),
        ]
        doc.build(story)
        self.status_var.set(f"Receipt saved: {filename}")
        try:
            os.startfile(filename)
        except Exception:
            pass
 
    # ── REPORTS ───────────────────────────────
    def _daily_sales(self):
        win = self._report_win("Daily Sales Report", 700, 440)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        rows = self.db.fetch_all(
            """SELECT s.invoice_no, s.total, s.sale_date, s.payment_method, u.full_name
               FROM sales s JOIN users u ON s.user_id = u.id
               WHERE DATE(s.sale_date)=? ORDER BY s.sale_date DESC""", (today,))
 
        Label(win, text=f"Date: {today}", font=("Segoe UI", 10),
              bg=G["panel"], fg=G["txt2"]).pack(padx=14, anchor=W)
 
        cols = ("Invoice", "Total", "Time", "Payment", "Cashier")
        tree = self._make_report_tree(win, cols, {c: 120 for c in cols})
        total = 0
        for r in rows:
            tree.insert("", END,
                values=(r[0], f"${r[1]:.2f}", r[2][11:16], r[3], r[4]))
            total += r[1]
 
        Label(win, text=f"Total Sales: ${total:.2f}",
              font=("Segoe UI", 13, "bold"),
              bg=G["panel"], fg=G["accent"]).pack(pady=10)
 
    def _inventory_report(self):
        win = self._report_win("Inventory Report", 860, 520)
        rows = self.db.fetch_all(
            """SELECT p.name, c.name, p.price, p.quantity, p.min_stock, p.unit
               FROM products p JOIN categories c ON p.category_id = c.id
               ORDER BY c.name, p.name""")
 
        cols = ("Product", "Category", "Price", "Stock", "Min", "Unit", "Status")
        widths = {"Product": 200, "Category": 120, "Price": 80,
                  "Stock": 70, "Min": 60, "Unit": 70, "Status": 90}
        tree = self._make_report_tree(win, cols, widths)
        tree.tag_configure("low", foreground=G["red"])
 
        low = []
        for r in rows:
            status = "Low Stock" if r[3] <= r[4] else "OK"
            tags = ("low",) if r[3] <= r[4] else ()
            tree.insert("", END,
                values=(r[0], r[1], f"${r[2]:.2f}", r[3], r[4], r[5] or "", status),
                tags=tags)
            if r[3] <= r[4]:
                low.append(r[0])
 
        if low:
            Label(win, text=f"⚠  Low stock: {', '.join(low)}",
                  font=("Segoe UI", 9), bg=G["panel"],
                  fg=G["red"], wraplength=800).pack(padx=14, pady=6, anchor=W)
 
    def _sales_history(self):
        win = self._report_win("Sales History", 860, 520)
 
        # Filter row
        ff = Frame(win, bg=G["panel"])
        ff.pack(fill=X, padx=14, pady=8)
        Label(ff, text="From:", font=("Segoe UI", 10),
              bg=G["panel"], fg=G["txt2"]).pack(side=LEFT)
        from_e = Entry(ff, width=12, font=("Segoe UI", 10), relief=FLAT,
                       bg=G["input_bg"], fg=G["txt"],
                       highlightbackground=G["border"], highlightthickness=1)
        from_e.pack(side=LEFT, padx=4, ipady=4)
        from_e.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
 
        Label(ff, text="To:", font=("Segoe UI", 10),
              bg=G["panel"], fg=G["txt2"]).pack(side=LEFT, padx=(8, 0))
        to_e = Entry(ff, width=12, font=("Segoe UI", 10), relief=FLAT,
                     bg=G["input_bg"], fg=G["txt"],
                     highlightbackground=G["border"], highlightthickness=1)
        to_e.pack(side=LEFT, padx=4, ipady=4)
        to_e.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
 
        cols = ("Invoice", "Date", "Total", "Cashier", "Payment")
        tree = self._make_report_tree(win, cols, {c: 150 for c in cols})
 
        def load():
            for i in tree.get_children():
                tree.delete(i)
            rows = self.db.fetch_all(
                """SELECT s.invoice_no, s.sale_date, s.total, u.full_name, s.payment_method
                   FROM sales s JOIN users u ON s.user_id = u.id
                   WHERE DATE(s.sale_date) BETWEEN ? AND ? ORDER BY s.sale_date DESC""",
                (from_e.get(), to_e.get()))
            for r in rows:
                tree.insert("", END,
                    values=(r[0], r[1][:19], f"${r[2]:.2f}", r[3], r[4]))
 
        def reprint():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Warning", "Select a sale.", parent=win)
                return
            inv = tree.item(sel[0])["values"][0]
            rec = self.db.fetch_one("SELECT id FROM sales WHERE invoice_no=?", (inv,))
            if rec:
                self._generate_receipt(inv, rec[0])
 
        Button(ff, text="Load", font=("Segoe UI", 9, "bold"),
               command=load, bg=G["accent"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=14, pady=5).pack(side=LEFT, padx=8)
        Button(ff, text="Reprint Selected", font=("Segoe UI", 9, "bold"),
               command=reprint, bg=G["amber"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=14, pady=5).pack(side=LEFT)
        load()
 
    def _report_win(self, title, w, h):
        win = Toplevel(self.root)
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.configure(bg=G["panel"])
        self._center_win(win, w, h)
        Label(win, text=title, font=("Segoe UI", 13, "bold"),
              bg=G["topbar"], fg=G["txt"], pady=10).pack(fill=X, padx=0)
        return win
 
    def _make_report_tree(self, parent, cols, widths):
        f = Frame(parent, bg=G["panel"])
        f.pack(fill=BOTH, expand=True, padx=14, pady=8)
        tree = ttk.Treeview(f, columns=cols, show="headings",
                            style="Glass.Treeview", selectmode="browse")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 120),
                        stretch=(col == cols[0]))
        vsb = ttk.Scrollbar(f, orient=VERTICAL, command=tree.yview,
                            style="GlassV.TScrollbar")
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        vsb.pack(side=RIGHT, fill=Y)
        tree.tag_configure("odd", background=G["card"])
        tree.tag_configure("even", background=G["panel"])
        return tree
 
    # ── MANAGEMENT ────────────────────────────
    def _user_management(self):
        if self.role != "admin":
            messagebox.showerror("Access Denied", "Admin only.")
            return
        win = self._report_win("User Management", 640, 440)
        cols = ("ID", "Username", "Role", "Full Name")
        tree = self._make_report_tree(win, cols, {"ID": 50, "Username": 150, "Role": 100, "Full Name": 200})
 
        def load():
            for i in tree.get_children():
                tree.delete(i)
            for u in self.db.fetch_all("SELECT id, username, role, full_name FROM users"):
                tree.insert("", END, values=u)
 
        def add():
            aw = Toplevel(win)
            aw.title("Add User")
            aw.geometry("320x320")
            aw.configure(bg=G["panel"])
            aw.transient(win)
            aw.grab_set()
            self._center_win(aw, 320, 320)
 
            fields = {}
            for lbl, key, show in [("Username", "u", ""), ("Password", "p", "•"),
                                    ("Full Name", "n", "")]:
                Label(aw, text=lbl, font=("Segoe UI", 10),
                      bg=G["panel"], fg=G["txt2"]).pack(pady=(10, 2))
                e = Entry(aw, show=show, font=("Segoe UI", 11), relief=FLAT,
                          bg=G["input_bg"], fg=G["txt"],
                          highlightbackground=G["border"], highlightthickness=1)
                e.pack(ipady=6, padx=24, fill=X)
                fields[key] = e
 
            Label(aw, text="Role", font=("Segoe UI", 10),
                  bg=G["panel"], fg=G["txt2"]).pack(pady=(10, 2))
            role_cb = ttk.Combobox(aw, values=["admin", "cashier"],
                                   state="readonly", style="Glass.TCombobox")
            role_cb.set("cashier")
            role_cb.pack(padx=24, fill=X)
 
            def save():
                if not fields["u"].get() or not fields["p"].get():
                    messagebox.showerror("Error", "Username and password required.", parent=aw)
                    return
                ph = hashlib.sha256(fields["p"].get().encode()).hexdigest()
                try:
                    self.db.execute_query(
                        "INSERT INTO users (username, password, role, full_name) VALUES (?,?,?,?)",
                        (fields["u"].get(), ph, role_cb.get(), fields["n"].get()))
                    load()
                    aw.destroy()
                    self.toast.show("User added")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Username exists.", parent=aw)
 
            Button(aw, text="Save", font=("Segoe UI", 11, "bold"),
                   command=save, bg=G["accent"], fg="#FFF",
                   relief=FLAT, cursor="hand2", bd=0, pady=10).pack(
                fill=X, padx=24, pady=16)
 
        def delete():
            sel = tree.selection()
            if not sel:
                return
            uid = tree.item(sel[0])["values"][0]
            if uid == self.user_id:
                messagebox.showerror("Error", "Cannot delete your own account.", parent=win)
                return
            if messagebox.askyesno("Confirm", "Delete this user?", parent=win):
                self.db.execute_query("DELETE FROM users WHERE id=?", (uid,))
                load()
                self.toast.show("User deleted")
 
        bf = Frame(win, bg=G["panel"])
        bf.pack(pady=8)
        Button(bf, text="Add User", font=("Segoe UI", 10, "bold"),
               command=add, bg=G["accent"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        Button(bf, text="Delete User", font=("Segoe UI", 10, "bold"),
               command=delete, bg=G["red"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        load()
 
    def _category_management(self):
        if self.role != "admin":
            messagebox.showerror("Access Denied", "Admin only.")
            return
        win = self._report_win("Category Management", 500, 380)
        cols = ("ID", "Name", "Description")
        tree = self._make_report_tree(win, cols, {"ID": 50, "Name": 180, "Description": 220})
 
        def load():
            for i in tree.get_children():
                tree.delete(i)
            for c in self.db.fetch_all("SELECT id, name, description FROM categories"):
                tree.insert("", END, values=c)
 
        def add():
            name = simpledialog.askstring("Add Category", "Category name:", parent=win)
            if name:
                desc = simpledialog.askstring("Add Category", "Description (optional):", parent=win)
                try:
                    self.db.execute_query(
                        "INSERT INTO categories (name, description) VALUES (?,?)",
                        (name, desc or ""))
                    load()
                    self._load_categories()
                    self._load_products()
                    self.toast.show("Category added")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Category already exists.", parent=win)
 
        def delete():
            sel = tree.selection()
            if not sel:
                return
            cid  = tree.item(sel[0])["values"][0]
            cname = tree.item(sel[0])["values"][1]
            count = self.db.fetch_one("SELECT COUNT(*) FROM products WHERE category_id=?", (cid,))
            if count[0] > 0:
                messagebox.showerror("Error", f"'{cname}' has {count[0]} products.", parent=win)
                return
            if messagebox.askyesno("Confirm", f"Delete '{cname}'?", parent=win):
                self.db.execute_query("DELETE FROM categories WHERE id=?", (cid,))
                load()
                self._load_categories()
                self.toast.show("Category deleted")
 
        bf = Frame(win, bg=G["panel"])
        bf.pack(pady=8)
        Button(bf, text="Add Category", font=("Segoe UI", 10, "bold"),
               command=add, bg=G["accent"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        Button(bf, text="Delete Category", font=("Segoe UI", 10, "bold"),
               command=delete, bg=G["red"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        load()
 
    def _product_management(self):
        if self.role != "admin":
            messagebox.showerror("Access Denied", "Admin only.")
            return
        win = self._report_win("Product Management", 900, 540)
        cols = ("ID", "Barcode", "Name", "Category", "Price", "Cost", "Stock", "Min", "Unit")
        widths = {"ID": 40, "Barcode": 100, "Name": 180, "Category": 110,
                  "Price": 70, "Cost": 70, "Stock": 60, "Min": 60, "Unit": 60}
        tree = self._make_report_tree(win, cols, widths)
        tree.tag_configure("low", foreground=G["red"])
 
        def load():
            for i in tree.get_children():
                tree.delete(i)
            rows = self.db.fetch_all(
                """SELECT p.id, p.barcode, p.name, c.name, p.price, p.cost,
                          p.quantity, p.min_stock, p.unit
                   FROM products p LEFT JOIN categories c ON p.category_id = c.id
                   ORDER BY p.name""")
            for row in rows:
                tags = ("low",) if (row[6] or 0) <= (row[7] or 0) else ()
                tree.insert("", END, values=row, tags=tags)
 
        def add_product():
            cats = self.db.fetch_all("SELECT id, name FROM categories ORDER BY name")
            cat_map = {c[1]: c[0] for c in cats}
 
            aw = Toplevel(win)
            aw.title("Add Product")
            aw.geometry("360x480")
            aw.configure(bg=G["panel"])
            aw.transient(win)
            aw.grab_set()
            self._center_win(aw, 360, 480)
 
            entries = {}
            field_defs = [
                ("Barcode", "barcode"), ("Name *", "name"), ("Price *", "price"),
                ("Cost", "cost"), ("Stock", "stock"), ("Min Stock", "min_stock"),
                ("Unit (pcs/kg/l…)", "unit"),
            ]
            for lbl, key in field_defs:
                Label(aw, text=lbl, font=("Segoe UI", 9),
                      bg=G["panel"], fg=G["txt2"]).pack(pady=(6, 1), anchor=W, padx=24)
                e = Entry(aw, font=("Segoe UI", 11), relief=FLAT,
                          bg=G["input_bg"], fg=G["txt"],
                          highlightbackground=G["border"], highlightthickness=1)
                e.pack(ipady=5, padx=24, fill=X)
                entries[key] = e
 
            Label(aw, text="Category", font=("Segoe UI", 9),
                  bg=G["panel"], fg=G["txt2"]).pack(pady=(6, 1), anchor=W, padx=24)
            cat_cb = ttk.Combobox(aw, values=list(cat_map.keys()),
                                  state="readonly", style="Glass.TCombobox")
            if cats:
                cat_cb.set(cats[0][1])
            cat_cb.pack(padx=24, fill=X)
 
            def save():
                name = entries["name"].get().strip()
                price = entries["price"].get().strip()
                if not name or not price:
                    messagebox.showerror("Error", "Name and Price are required.", parent=aw)
                    return
                try:
                    price_v = float(price)
                    cost_v  = float(entries["cost"].get() or 0)
                    stock_v = int(entries["stock"].get() or 0)
                    min_v   = int(entries["min_stock"].get() or 0)
                except ValueError:
                    messagebox.showerror("Error", "Invalid numeric values.", parent=aw)
                    return
                cat_id = cat_map.get(cat_cb.get())
                bc = entries["barcode"].get().strip() or None
                try:
                    self.db.execute_query(
                        """INSERT INTO products
                           (barcode, name, category_id, price, cost, quantity, min_stock, unit)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (bc, name, cat_id, price_v, cost_v, stock_v, min_v,
                         entries["unit"].get().strip() or "pcs"))
                    load()
                    self._load_products()
                    aw.destroy()
                    self.toast.show(f"Product '{name}' added")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Barcode already exists.", parent=aw)
 
            Button(aw, text="Save Product", font=("Segoe UI", 11, "bold"),
                   command=save, bg=G["accent"], fg="#FFF",
                   relief=FLAT, cursor="hand2", bd=0, pady=10).pack(
                fill=X, padx=24, pady=12)
 
        def delete_product():
            sel = tree.selection()
            if not sel:
                return
            pid  = tree.item(sel[0])["values"][0]
            name = tree.item(sel[0])["values"][2]
            if messagebox.askyesno("Confirm", f"Delete '{name}'?", parent=win):
                self.db.execute_query("DELETE FROM products WHERE id=?", (pid,))
                load()
                self._load_products()
                self.toast.show(f"Product '{name}' deleted")
 
        bf = Frame(win, bg=G["panel"])
        bf.pack(pady=8)
        Button(bf, text="Add Product", font=("Segoe UI", 10, "bold"),
               command=add_product, bg=G["accent"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        Button(bf, text="Delete Product", font=("Segoe UI", 10, "bold"),
               command=delete_product, bg=G["red"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        Button(bf, text="Refresh", font=("Segoe UI", 10, "bold"),
               command=load, bg=G["txt2"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, padx=16, pady=7).pack(side=LEFT, padx=4)
        load()
 
    # ── AUTH ──────────────────────────────────
    def _change_password(self):
        win = Toplevel(self.root)
        win.title("Change Password")
        win.geometry("340x280")
        win.configure(bg=G["panel"])
        win.transient(self.root)
        win.grab_set()
        self._center_win(win, 340, 280)
 
        Label(win, text="Change Password", font=("Segoe UI", 13, "bold"),
              bg=G["topbar"], fg=G["txt"], pady=10).pack(fill=X)
 
        entries = {}
        for lbl, key in [("Current Password", "cur"), ("New Password", "new"),
                          ("Confirm Password", "con")]:
            Label(win, text=lbl, font=("Segoe UI", 9),
                  bg=G["panel"], fg=G["txt2"]).pack(pady=(8, 1), anchor=W, padx=24)
            e = Entry(win, show="•", font=("Segoe UI", 11), relief=FLAT,
                      bg=G["input_bg"], fg=G["txt"],
                      highlightbackground=G["border"], highlightthickness=1)
            e.pack(ipady=6, padx=24, fill=X)
            entries[key] = e
 
        def change():
            cur_hash = hashlib.sha256(entries["cur"].get().encode()).hexdigest()
            if not self.db.fetch_one(
                    "SELECT id FROM users WHERE id=? AND password=?",
                    (self.user_id, cur_hash)):
                messagebox.showerror("Error", "Current password incorrect.", parent=win)
                return
            if entries["new"].get() != entries["con"].get():
                messagebox.showerror("Error", "New passwords don't match.", parent=win)
                return
            if len(entries["new"].get()) < 4:
                messagebox.showerror("Error", "Minimum 4 characters.", parent=win)
                return
            new_hash = hashlib.sha256(entries["new"].get().encode()).hexdigest()
            self.db.execute_query(
                "UPDATE users SET password=? WHERE id=?", (new_hash, self.user_id))
            win.destroy()
            self.toast.show("✓ Password changed")
 
        Button(win, text="Update Password", font=("Segoe UI", 11, "bold"),
               command=change, bg=G["accent"], fg="#FFF",
               relief=FLAT, cursor="hand2", bd=0, pady=10).pack(
            fill=X, padx=24, pady=14)
 
    def _logout(self):
        if messagebox.askyesno("Logout", "Log out of myPOS?"):
            self.db.close()
            self.root.destroy()
            r = Tk()
            LoginWindow(r)
            r.mainloop()
 
    # ── UTIL ──────────────────────────────────
    def _center_win(self, win, w, h):
        win.update_idletasks()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
 
 
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    LoginWindow(root)
    root.mainloop()
 