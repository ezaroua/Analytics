import json

from csv_analyzer import CSVAnalyzer
from models.analyzed_result_model import (AnalyzedNote, AnalyzedPrice,
                                          AnalyzedQuantity)
from models.product_model import ProductModel, ProductModelOnError


class ReportGenerator:
    
    def __init__(self, path) :
        self.path : str = path
        self.analyzer = CSVAnalyzer(path) 
        self.analyzed_price : AnalyzedPrice = None
        self.analyzed_quantity : AnalyzedQuantity = None
        self.analyzed_note : AnalyzedNote = None
        self.products_on_error = []
        self.product = []
        

    def generate_report(self, file_key):
        # Perform Analysis
        self.analyzer.analyze()
        self.analyzed_price = self.analyzer.analyzed_price
        self.analyzed_quantity = self.analyzer.analyzed_quantity
        self.analyzed_note = self.analyzer.analyzed_note
        self.products_on_error = self.analyzer.products_on_error
        self.products = self.analyzer.products
        print("that goes here")
        # Generate Report
        report = {
            "file_id": file_key,
            "products_on_error": [product.to_dict() for product in self.analyzer.products_on_error],
            "analyzed_results": {
                "price": self.analyzer.analyzed_price.to_dict(),
                "quantity": self.analyzer.analyzed_quantity.to_dict(),
                "note": self.analyzer.analyzed_note.to_dict()
            }
        } 
        
        return json.dumps(report, indent=4)