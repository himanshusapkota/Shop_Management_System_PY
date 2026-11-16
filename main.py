import csv 
import os
from datetime import datetime 

PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"
LOW_STOCK_LIMIT = 5

PRODUCT_FIELDS = ["id", "name" , "category" , "buying_price" , "selling_price" , "quantity"]

SALES_FIELDS = ["sale_id" , "date" , "product_id" , "product_name" , "qunatity" , "unit_price" , "total" , "profit"]

class Product:
    def __init__(self, product_id , name , category , buying_price , selling_price , quantity) :
        self.id = product_id
        self.name = name 
        self.category = category
        self.buying_price = buying_price
        self.selling_price = selling_price


    def is_low_stock(self):

        return self.quantity < LOW_STOCK_LIMIT    

    def to_row (self):
        return {
            "id" : self.id,
            "name" : self.name,
            "category" : self.category,
            "buying_price" : self.buying_price,
            "selling_price": self.selling_price,

              }

class Sale :
    def __init__(self , sale_id , date , product_id , product_name , quantity , unit_price , total , profit):

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
                "sale_id" : self.sale_id,
                "date": self.date,
                "product_id": self.product_id,
                "product_name" : self.product_name,
                "quantiy": self.quantity,
                "unit_price" : self.unit_price,
                "total" : self.total,
                "profit" : self.profit

            }


class Shop: 
     def __init__(self):
          self.product = []
          self.sales = []

     def load(self):
       
        for filename, fields in [(PRODUCTS_FILE, PRODUCT_FIELDS), (SALES_FILE, SALES_FIELDS)]:

            if not os.path.exists(filename):

                write_csv(filename, fields, [])


        with open(PRODUCTS_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:

                    self.products.append(Product(

                        row["id"], row["name"], row["category"],

                        float(row["buying_price"]), float(row["selling_price"]),

                        int(row["quantity"])))
                    
                except (ValueError, KeyError):

                    print("Skipped a broken row in", PRODUCTS_FILE)

     
    
        with open (SALES_FILE , newline = "" , encoding = "utf-8") as f : 
            for row in csv.DictReader(f):
                try:
                    self.sales.append(Sale(

                        row["sale_id"],
                        row ["date"],
                        row["product_id"],
                        row ["product_name"],
                        int(row["quantity"]),
                        float(row["unit_price"]),
                        float(row["total"]),
                        float(row["profit"])))

                except (ValueError, KeyError):
                    print("Skipped a broken row in " , SALES_FILE)


        def save_products(self):
            write_csv(PRODUCTS_FILE , PRODUCT_FIELDS , [p.to_row() for p in self.products])   

        def save_sales (self):
            write_csv (SALES_FILE,SALES_FIELDS, [s.to_row() for s in self.sales])         

    
        def next_product_id (self): 
            biggest = 0  
            for p in self.products:
                biggest = max(biggest, id_number(p.id))

            for s in self.sales:
                biggest = max(biggest , id_number(s.product_id))    

            return "P" + str(biggest + 1).zfill(3)    

        def find_by_id(self , product_id):    
            for p in self.products:
                if p.id.lower() == product_id.lower():
                    return p
            return None    

        def search (self , word)  :  
            word = word.lower()
            found = []
            for p in self.products:
                if word == p.id.lower() or word in p.name.lower():
                    found.append(p)

                return found    

                







