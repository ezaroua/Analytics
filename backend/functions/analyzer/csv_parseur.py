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
            FIRST_RUN = 0
            list_index = 0
            for row in reader :
                if(list_index == FIRST_RUN):
                    list_index + 1
                    next
            else :
                product = ProductModel(
                    id=row["ID"],
                    name=row["Nom"],
                    price=row["Prix"],
                    quantity=row["Quantite"],
                    note=row["Note_Client"]
                )
                self.products.append(product)
        
                
    def get_data(self) : 
        return self.products