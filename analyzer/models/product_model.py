class ProductModel :
    def __init__(self, id, name, price, quantity,note):
        self.ID = id
        self.Nom : String = name
        self.Prix : Number = price
        self.Quantité : Number = quantity
        self.Note_Client : Number = note 

    def __str__(self):
        return f"ProductModel({self.id}, {self.name}, {self.price}, {self.quantity})"
    
    def to_dict(self):
        return {
            "ID": self.id,
            "Nom": self.name,
            "Prix": self.price,
            "Quantité": self.quantity,
            "Note_Client": self.note
        }
    
    
class ProductModelOnError(ProductModel):
    def __init__(self, id, name, price, quantity,note, error_message):
        super().__init__(id, name, price, quantity,note)
        self.error_message = error_message
        
    def __str__(self):
        return f"ProductModelOnError({self.id}, {self.name}, {self.price}, {self.quantity}, {self.error_message})"
    
    def to_dict(self):
        data = super().to_dict()
        data["error_message"] = self.error_message
        return data
    