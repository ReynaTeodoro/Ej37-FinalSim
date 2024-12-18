class Mesa():
    def __init__(self, numero:int):
        self.numero = numero
        self.estado = "Libre"
    def estaLibre(self):
        return self.estado == "Libre"
    def ocupar(self):
        self.estado = "Ocupada"
    def desocupar(self):
        self.estado = "Libre"
    def __str__(self):
        return f"Mesa {self.numero} - Estado: {self.estado}"
