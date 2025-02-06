from csv_parseur import CSVProductParseur
from models import (AnalyzedNote, AnalyzedPrice, AnalyzedQuantity,
                    ProductModel, ProductModelOnError)


class CSVAnalyzer :

    def __init__(self, path) : 
        self.path = path
        self.parseur = CSVProductParseur(path)
        self.products = self.parseur.get_data()
        self.products_on_error = []
        self.analyzed_price : AnalyzedPrice = None
        self.analyzed_quantity : AnalyzedQuantity = None
        self.analyzed_note : AnalyzedNote = None
        
    def analyze(self):
        self.verify_compliance()
        self.analyze_price()
        self.analyze_quantity()
        self.analyze_note()

    
    def verify_compliance(self):
        is_compliant = True
        for product in self.products :
            if self.verify_products_compliance(product) :
                next
            else :
                is_compliant = False
        return is_compliant 
        
    def verify_products_compliance(self, product):
        self.verify_product_field_compliance(product)    
        
        if self.products_on_error == []:
            return True
        else :
            return False 
            
    def verify_product_field_compliance(self, product) :  
        try:
            product.Prix = float(product.Prix)
            product.Quantité = int(product.Quantité)
            product.Note_Client = float(product.Note_Client)
        except ValueError as e:
            product = ProductModelOnError(product.ID, product.Nom, product.Prix, product.Quantité, product.Note_Client, f"Invalid value: {e}")
            self.products_on_error.append(product)
            return
        if self.products.__contains__(product) :
            product = ProductModelOnError(product.ID, product.Nom, product.Prix, product.Quantité, product.Note_Client, "This product is already in the list on product id: " + product.ID)
            self.products_on_error.append(product)
            next
        if product.Prix < 0 or product.Prix > 500:
            product = ProductModelOnError(product.ID, product.Nom, product.Prix, product.Quantité, product.Note_Client, "The price is not between 0 and 500 on product id: " + product.ID)
            self.products_on_error.append(product)
            next
        if product.Quantité < 0 or product.Quantité == None or product.Quantité > 1000:
            product = ProductModelOnError(product.ID, product.Nom, product.Prix, product.Quantité, product.Note_Client, "The quantity is not between 0 and 1000 on product id: " + product.ID)
            self.products_on_error.append(product)
            next
        if product.Note_Client < 0 or product.Note_Client > 5:
            product = ProductModelOnError(product.ID, product.Nom, product.Prix, product.Quantité, product.Note_Client, "The note is not between 0 and 5 on product id: " + product.ID)
            self.products_on_error.append(product)
            next    
        
    def analyze_price(self):
        prices = []
        for product in self.products :
            if not self.is_id_contained_in_products_on_error(product.ID):
                next
            else :
                prices.append(product.Prix)
                prices.sort()
                print(prices)
        average_price = sum(prices) / len(prices)
        median_price = prices[len(prices) // 2]
        gap_on_price = prices[len(prices) - 1] - prices[0]
        self.analyze_price = AnalyzedPrice(average_price, median_price, gap_on_price)
    
    def analyze_quantity(self):
        quantities = []
        for product in self.products :
            if not self.is_id_contained_in_products_on_error(product.ID):
                next
            else :
                quantities.append(product.Quantité)
                quantities.sort()
        average_quantity = sum(quantities) / len(quantities)
        median_quantity = quantities[len(quantities) // 2]
        gap_on_quantity = quantities[len(quantities) - 1] - quantities[0]
        self.analyze_quantity = AnalyzedQuantity(average_quantity, median_quantity, gap_on_quantity)
    
    def analyze_note(self):
        notes = []
        for product in self.products :
            if not self.is_id_contained_in_products_on_error(product.ID):
                next
            else :
                notes.append(product.Note_Client)
                notes.sort()
        average_note = sum(notes) / len(notes)
        median_note = notes[len(notes) // 2]
        gap_on_note = notes[len(notes) - 1] - notes[0]
        self.analyze_note = AnalyzedNote(average_note, median_note, gap_on_note)
    
    
    def is_id_contained_in_products_on_error(self, id):
       id_set = {product.ID for product in self.products_on_error}
       if id in id_set:
           return True
       else:
            return False
    
    