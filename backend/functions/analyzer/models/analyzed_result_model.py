class AnalyzedPrice:
    def __init__(self, average_price, median_price, gap_on_price):
        self.average_price = Number
        self.median_price = Number
        self.gap_on_price = Number
        
    def __str__(self):  
        return f"AnalyzedPrice({self.average_price}, {self.median_price}, {self.gap_on_price})"
    
    def to_dict(self):
        return {
            "average_price": self.average_price,
            "median_price": self.median_price,
            "gap_on_price": self.gap_on_price
        }
    
class AnalyzedQuantity:
    
    def __init__(self, average_quantity, median_quantity, gap_on_quantity):
        self.average_quantity = Number
        self.median_quantity = Number
        self.gap_on_quantity = Number
        
    def __str__(self):
        return f"AnalyzedQuantity({self.average_quantity}, {self.median_quantity}, {self.gap_on_quantity})"
    
    def to_dict(self):
        return {
            "average_quantity": self.average_quantity,
            "median_quantity": self.median_quantity,
            "gap_on_quantity": self.gap_on_quantity
        }
    
class AnalyzedNote:
    
    def __init__(self, average_note, median_note, gap_on_note):
        self.average_note = Number
        self.median_note = Number
        self.gap_on_note = Number
        
    def __str__(self):
        return f"AnalyzedNote({self.average_note}, {self.median_note}, {self.gap_on_note})"
    
    def to_dict(self):
        return {
            "average_note": self.average_note,
            "median_note": self.median_note,
            "gap_on_note": self.gap_on_note
        }

    
        
        