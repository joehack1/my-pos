# myPOS — Liquid Glass Edition

A modern, clean Point of Sale (POS) system built with Python and Tkinter!

## Features

- 🎨 Beautiful Liquid Glass theme design
- 🔐 User authentication with role-based access (admin / cashier)
- 🛒 Product management with categories
- 📊 Sales reports (Daily Sales, Inventory, Sales History)
- 🧾 Receipt generation in PDF format (using ReportLab)
- 📦 Inventory management with stock levels

## Installation

1. Make sure you have Python 3 installed
2. Install dependencies:
```bash
pip install reportlab
```

## Usage

1. Run the app:
```bash
python main.py
```

2. Default login (if you didn't set up your own first user):
- Username: `admin`
- Password: `admin123`

## Project Structure

```
my-pos/
├── main.py                  # Main application
├── setup.py                 # Script to add sample products
├── inventory_manager.py     # Inventory management utilities
├── inventorymanagement.py   # Duplicate inventory file (to be merged)
├── mypos.db                 # SQLite database (auto-created)
├── receipt_*.pdf            # Generated receipts
└── README.md                # This file
```

## To-Do

Check [TODO.md](TODO.md) for planned improvements!

## License

MIT
