class Mozo:
    def __init__(self,id:int):
        self.id = id
        self.estado = "Libre"
        self.enMesa = None
    def estaLibre(self):
        return self.estado == "Libre"
    def ocupar(self):
        self.estado = "Ocupado"
    def desocupar(self):
        self.enMesa = None
        self.estado = "Libre"
    def __str__(self):
        return f"Mozo {self.id} - Estado: {self.estado}- Mesa: {self.enMesa}"
