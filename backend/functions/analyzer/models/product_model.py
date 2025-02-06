class ProductModel :
    def __init__(self, id, name, price, quantity,note):
        self.ID = id
        self.Nom : str = name
        self.Prix : float = price
        self.Quantité : int = quantity
        self.Note_Client : float = note 

    def __str__(self):
        return f"ProductModel({self.ID}, {self.Nom}, {self.Prix}, {self.Quantité})"
    
    def to_dict(self):
        return {
            "ID": self.ID,
            "Nom": self.Nom,
            "Prix": self.Prix,
            "Quantité": self.Quantité,
            "Note_Client": self.Note_Client
        }
    
    
class ProductModelOnError(ProductModel):
    def __init__(self, id, name, price, quantity,note, error_message):
        super().__init__(id, name, price, quantity,note)
        self.error_message = error_message
        
    def __str__(self):
        return f"ProductModelOnError({self.ID}, {self.Nom}, {self.Prix}, {self.Quantité}, {self.error_message})"
    
    def to_dict(self):
        data = super().to_dict()
        data["error_message"] = self.error_message
        return data
    