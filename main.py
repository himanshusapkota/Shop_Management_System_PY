
import csv
import os
from datetime import datetime

PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"
EXPORT_FOLDER = "exports"
LOW_STOCK_LIMIT = 5

PRODUCT_FIELDS = ["id", "name", "category", "buying_price", "selling_price", "quantity"]

SALES_FIELDS = ["sale_id", "date", "product_id", "product_name", "quantity", "unit_price", "total", "profit"]


def write_csv(filename, fields, rows):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def id_number(value):
    return int(value[1:]) if value[1:].isdigit() else 0


class Product:
    def __init__(self, product_id, name, category, buying_price, selling_price, quantity):
        self.id = product_id
        self.name = name
        self.category = category
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.quantity = quantity

    def is_low_stock(self):
        return self.quantity < LOW_STOCK_LIMIT

    def to_row(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "buying_price": self.buying_price,
            "selling_price": self.selling_price,
            "quantity": self.quantity
        }


class Sale:
    def __init__(self, sale_id, date, product_id, product_name, quantity, unit_price, total, profit):
        self.sale_id = sale_id
        self.date = date
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total = total
        self.profit = profit

    def to_row(self):
        return {
            "sale_id": self.sale_id,
            "date": self.date,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total": self.total,
            "profit": self.profit
        }


class Shop:
    def __init__(self):
        self.products = []
        self.sales = []

    def load(self):

        for filename, fields in [
            (PRODUCTS_FILE, PRODUCT_FIELDS),
            (SALES_FILE, SALES_FIELDS)
        ]:

            if not os.path.exists(filename):
                write_csv(filename, fields, [])

        with open(PRODUCTS_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    self.products.append(Product(
                        row["id"],
                        row["name"],
                        row["category"],
                        float(row["buying_price"]),
                        float(row["selling_price"]),
                        int(row["quantity"])
                    ))

                except (ValueError, KeyError):
                    print("Skipped a broken row in", PRODUCTS_FILE)

        with open(SALES_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    self.sales.append(Sale(
                        row["sale_id"],
                        row["date"],
                        row["product_id"],
                        row["product_name"],
                        int(row["quantity"]),
                        float(row["unit_price"]),
                        float(row["total"]),
                        float(row["profit"])
                    ))

                except (ValueError, KeyError):
                    print("Skipped a broken row in", SALES_FILE)

    def save_products(self):
        write_csv(PRODUCTS_FILE, PRODUCT_FIELDS, [p.to_row() for p in self.products])

    def save_sales(self):
        write_csv(SALES_FILE, SALES_FIELDS, [s.to_row() for s in self.sales])

    def next_product_id(self):
        biggest = 0

        for p in self.products:
            biggest = max(biggest, id_number(p.id))

        for s in self.sales:
            biggest = max(biggest, id_number(s.product_id))

        return "P" + str(biggest + 1).zfill(3)

    def find_by_id(self, product_id):
        for p in self.products:
            if p.id.lower() == product_id.lower():
                return p

        return None

    def search(self, word):
        word = word.lower()
        found = []

        for p in self.products:
            if word == p.id.lower() or word in p.name.lower():
                found.append(p)

        return found

    def add_product(self, name, category, buying_price, selling_price, quantity):
        product = Product(
            self.next_product_id(),
            name,
            category,
            buying_price,
            selling_price,
            quantity
        )

        self.products.append(product)
        self.save_products()

        return product

    def delete_product(self, product):
        self.products.remove(product)
        self.save_products()

    def low_stock_products(self):
        return [p for p in self.products if p.is_low_stock()]

    def next_sale_id(self):
        biggest = 0

        for s in self.sales:
            biggest = max(biggest, id_number(s.sale_id))

        return "S" + str(biggest + 1).zfill(4)

    def sell(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")

        if quantity > product.quantity:
            raise ValueError(f"Not enough stock. Only {product.quantity} left.")

        total = quantity * product.selling_price
        profit = quantity * (product.selling_price - product.buying_price)

        product.quantity -= quantity

        sale = Sale(
            self.next_sale_id(),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            product.id,
            product.name,
            quantity,
            product.selling_price,
            total,
            profit
        )

        self.sales.append(sale)
        self.save_products()
        self.save_sales()

        return sale

    def total_revenue(self):
        return sum(s.total for s in self.sales)

    def total_profit(self):
        return sum(s.profit for s in self.sales)

    def export_products(self):
        write_csv(
            os.path.join(EXPORT_FOLDER, "products.csv"),
            PRODUCT_FIELDS,
            [p.to_row() for p in self.products]
        )

    def export_sales(self):
        write_csv(
            os.path.join(EXPORT_FOLDER, "sales.csv"),
            SALES_FIELDS,
            [s.to_row() for s in self.sales]
        )

    def export_inventory(self):
        fields = [
            "product_id", "product_name", "category", "quantity",
            "buying_price", "selling_price", "stock_cost_value",
            "stock_sale_value", "status"
        ]

        rows = []

        for p in self.products:
            if p.quantity == 0:
                status = "Out of Stock"

            elif p.is_low_stock():
                status = "Low Stock"

            else:
                status = "In Stock"

            rows.append({
                "product_id": p.id,
                "product_name": p.name,
                "category": p.category,
                "quantity": p.quantity,
                "buying_price": p.buying_price,
                "selling_price": p.selling_price,
                "stock_cost_value": round(p.quantity * p.buying_price, 2),
                "stock_sale_value": round(p.quantity * p.selling_price, 2),
                "status": status
            })

        write_csv(
            os.path.join(EXPORT_FOLDER, "inventory.csv"),
            fields,
            rows
        )

    def write_csv(filename , fields , rows):
        with open (filename , "w" , newline= "" , encoding = "utf-8") as f :
            writer = csv.DictWriter(f , fieldnames = fields)
            writer.writeheader()
            writer.writerows(rows)


    def id_number(text):        
        try:
            return int (text[-1:])

        except ValueError:
            return 0    


    def read_text(prompt):
        while True:
            text = input(prompt).strip()        
            if text != "":
                return text
            print("This can't be empty")

    def read_number(prompt, whole=False ,allow_blank=False):        
        while True:
            text = input(prompt).strip()
            if allow_blank and text == "":
                return None

            try : 
                value = int(text) if whole else float(text)

            except ValueError :    
                print("Please enter a whole number." if whole else "Please Enter a Number")

                continue

            if value < 0 :
                print("Negative values are not allowed")
                continue

            return value 

    def ask_yes_no (prompt):
        return input(prompt).strip().lower == "y"



    def print_products(products):    
        print("-" * 78)
        print(f"{'ID':<6}{'Name':<22}{'Category':<14}{'Buy':>9}{'Sell':>9}{'Qty':>6}")
        print("-" * 78)

        for p in products : 
            print(f"{p.id:<6}{p.name[:21]:<22}{p.category[:13]:<14}"
              f"{p.buying_price:>9.2f}{p.selling_price:>9.2f}{p.quantity:>6}")
        print("-" * 78)



        


