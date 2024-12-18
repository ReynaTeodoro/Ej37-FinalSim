class Grupo():
    def __init__(self, id_grupo: int, tamaño: int):
        self.id_grupo = id_grupo
        self.tamaño = tamaño
        self.mesa = None
        self.estado = "En espera"
    def __str__(self):
        return f"Grupo {self.id_grupo} - Tamaño: {self.tamaño} - Mesa: {self.mesa} - Estado: {self.estado}"
