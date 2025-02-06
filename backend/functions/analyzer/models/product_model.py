class ProductModel :
    def __init__(self, id, name, price, quantity,note):
        self.ID = id
        self.nom : str = name
        self.prix : float = price
        self.quantite : int = quantity
        self.note_client : float = note 

    def __str__(self):
        return f"ProductModel({self.ID}, {self.nom}, {self.prix}, {self.quantite})"
    
    def to_dict(self):
        return {
            "ID": self.ID,
            "Nom": self.nom,
            "Prix": self.prix,
            "Quantite": self.quantite,
            "Note_Client": self.note_client
        }
    
    
class ProductModelOnError(ProductModel):
    def __init__(self, id, name, price, quantity,note, error_message):
        super().__init__(id, name, price, quantity,note)
        self.error_message = error_message
        
    def __str__(self):
        return f"ProductModelOnError({self.ID}, {self.nom}, {self.prix}, {self.quantite}, {self.error_message})"
    
    def to_dict(self):
        data = super().to_dict()
        data["error_message"] = self.error_message
        return data
    