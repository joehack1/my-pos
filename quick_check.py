
import sqlite3
db = sqlite3.connect('mypos.db')
c = db.cursor()
c.execute('SELECT id, name FROM products')
products = c.fetchall()
print(f'Number of products: {len(products)}')
for p in products:
    print(f'  {p[0]}: {p[1]}')
db.close()
