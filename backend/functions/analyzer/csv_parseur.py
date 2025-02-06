import csv as csv_lib

from models.product_model import ProductModel


class CSVProductParseur : 
    def __init__(self, path) : 
        self.path = path
        products = []
        self.load_products()
        
    def load_products(self) : 
        with open(self.path, 'r') as csv_file : 
            reader = csv_lib.reader(csv_file)
            for row in reader :
                product = ProductModel(row[0], row[1], row[2], row[3], row[4])
                self.products.append(product)
        
                
    def get_data(self) : 
        return self.data