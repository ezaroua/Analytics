import csv as csv_lib

from models.product_model import ProductModel


class CSVProductParseur : 
    def __init__(self, path) : 
        self.path = path
        self.products = []
        self.load_products()
        
    def load_products(self) : 
        with open(self.path, 'r',encoding="ISO-8859-1") as csv_file : 
            reader = csv_lib.DictReader(csv_file)
            for row in reader :
                product = ProductModel(
                    id=int(row["ID"]),
                    name=str(row["Nom"]),
                    price=float(row["Prix"]),
                    quantity=int(row["Quantite"]),
                    note=float(row["Note_Client"])
                )
                self.products.append(product)
        
                
    def get_data(self) : 
        return self.products