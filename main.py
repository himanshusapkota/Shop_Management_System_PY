import csv 
import os
from datetime import datetime 

PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"
LOW_STOCK_LIMIT = 5

PRODUCT_FIELDS = ["id", "name" , "category" , "buying_price" , "selling_price" , "quantity"]

SALES_FIELD = ["sale_id" , "date" , "product_id" , "product_name" , "qunatity" , "unit_price" , "total" , "profit"]

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


    

