from csv_parseur import CSVProductParseur
from models.analyzed_result_model import (AnalyzedNote, AnalyzedQuantity,
                                          AnayzedPrice)
from models.product_model import ProductModel, ProductModelOnError
from models.product_on_error_model import ProductsOnError


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
        verify_products_compliance()
        analyze_price()
        analyze_quantity()
        analyze_note()

    
    def verify_compliance():
        
        is_compliant = True
        for product in products :
            if verify_product_compliance(product) :
                next
            else :
                is_compliant = False
        return is_compliant 
        
    def verify_product_compliance(self, product):
        for product in products :
            verify_product_field_compliance(product)
        
        if products_on_error == []:
            return True
        else :
            return False 
            
    def verify_product_field_compliance(product) :  
        if products.contains(product) :
            product = ProductModelOnError(product.id, product.name, product.price, product.quantity, product.note, "This product is already in the list on product id: " + product.id)
            products_on_error.append(product)
            next
        if product.price < 0 or product.price > 500:
            product = ProductModelOnError(product.id, product.name, product.price, product.quantity, product.note, "The price is not between 0 and 500 on product id: " + product.id)
            products_on_error.append(product)
            next
        if product.quantity < 0 or product.quantity == None or product.quantity > 1000:
            product = ProductModelOnError(product.id, product.name, product.price, product.quantity, product.note, "The quantity is not between 0 and 1000 on product id: " + product.id)
            products_on_error.append(product)
            next
        if product.note < 0 or product.note > 5:
            product = ProductModelOnError(product.id, product.name, product.price, product.quantity, product.note, "The note is not between 0 and 5 on product id: " + product.id)
            products_on_error.append(product)
            next    
        
    def analyze_price(self):
        prices = []
        for product in self.products :
            if(is_id_contained_in_products_on_error(product.id)):
                next
            else :
                prices.append(product.price)
                prices.sort()
        average_price = sum(prices) / len(prices)
        median_price = prices[len(prices) // 2]
        gap_on_price = prices[len(prices) - 1] - prices[0]
        self.analyze_price = AnalyzedPrice(average_price, median_price, gap_on_price)
    
    def analyze_quantity(self):
        quantities = []
        for product in self.products :
            if(is_id_contained_in_products_on_error(product.id)):
                next
            else :
                quantities.append(product.quantity)
                quantities.sort()
        average_quantity = sum(quantities) / len(quantities)
        median_quantity = quantities[len(quantities) // 2]
        gap_on_quantity = quantities[len(quantities) - 1] - quantities[0]
        self.analyze_quantity = AnalyzedQuantity(average_quantity, median_quantity, gap_on_quantity)
    
    def analyze_note(self):
        notes = []
        for product in self.products :
            if(is_id_contained_in_products_on_error(product.id)):
                next
            else :
                notes.append(product.note)
                notes.sort()
        average_note = sum(notes) / len(notes)
        median_note = notes[len(notes) // 2]
        gap_on_note = notes[len(notes) - 1] - notes[0]
        self.analyze_note = AnalyzedNote(average_note, median_note, gap_on_note)
    
    
    def is_id_contained_in_products_on_error(self, id):
       id_set = {product["ID"] for product in self.products_on_error}
       if id in id_set:
           return True
       else:
            return False
    
    