from csv_parseur import CSVProductParseur
from models import (AnalyzedNote, AnalyzedPrice, AnalyzedQuantity,
                    ProductModel, ProductModelOnError)
import statistics

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
        for product in self.products :
           self.verify_product_field_compliance(product)
        for product in self.products :
            print(product.__str__())
        
            
    def verify_product_field_compliance(self, product) :
        is_valid = True
        mpoe: ProductModelOnError
        if(isinstance(product.prix, float) or isinstance(product.quantite, int) or isinstance(product.note_client, float)):
            mpoe = ProductModelOnError(product.ID, product.nom, product.prix, product.quantite, product.note_client, f"Invalid value type for prix or quantité or note_client {product.ID}")
            self.products_on_error.append(mpoe)
            is_valid = False
        if product.prix < 0 or product.prix > 500:
            mpoe = ProductModelOnError(product.ID, product.nom, product.prix, product.quantite, product.note_client, f"The price is not between 0 and 500 on product id: {product.ID}")
            self.products_on_error.append(mpoe)
            is_valid = False
        if product.quantite < 0 or product.quantite == None or product.quantite > 1000:
            mpoe = ProductModelOnError(product.ID, product.nom, product.prix, product.quantite, product.note_client, f"The quantity is not between 0 and 1000 on product id: {product.ID}")
            self.products_on_error.append(mpoe)
            is_valid = False
        if product.note_client < 0 or product.note_client > 5:
            mpoe = ProductModelOnError(product.ID, product.nom, product.prix, product.quantite, product.note_client, f"The note is not between 0 and 5 on product id: {product.ID}")
            self.products_on_error.append(mpoe)
            is_valid = False
        if not is_valid:
            self.products.remove(product)
        
    def analyze_price(self):
        prices = [float(product.prix) for product in self.products if isinstance(product.prix, (int, float, str)) and product.prix]  # Conversion sécurisée
        if not prices:
            print("No prices to analyze.")
            return
        
        prices.sort()
        average_price = sum(prices) / len(prices)
        median_price = statistics.median(prices)
        gap_on_price = prices[-1] - prices[0]
        self.analyzed_price = AnalyzedPrice(average_price, median_price, gap_on_price)

    def analyze_quantity(self):
        quantities = [int(product.quantite) for product in self.products if isinstance(product.quantite, (int, str)) and product.quantite]
        if not quantities:
            print("No quantities to analyze.")
            return
        
        quantities.sort()
        average_quantity = sum(quantities) / len(quantities)
        median_quantity = statistics.median(quantities)
        gap_on_quantity = quantities[-1] - quantities[0]
        self.analyzed_quantity = AnalyzedQuantity(average_quantity, median_quantity, gap_on_quantity)

    def analyze_note(self):
        notes = [float(product.note_client) for product in self.products if isinstance(product.note_client, (int, float, str)) and product.note_client]
        if not notes:
            print("No notes to analyze.")
            return
        
        notes.sort()
        average_note = sum(notes) / len(notes)
        median_note = statistics.median(notes)
        gap_on_note = notes[-1] - notes[0]
        self.analyzed_note = AnalyzedNote(average_note, median_note, gap_on_note)