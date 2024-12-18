import numpy as np


class GeneradorAleatorio:

    def __init__(self, seed=0):
        self.seed = seed
        np.random.seed(self.seed)

    def generar_numeros_uniformes(self, a, b, n) -> list:
        return np.sort([self.generar_uniforme(a, b) for _ in range(n)])

    def generar_numeros_exponenciales(self, media, n) -> list:
        return np.sort([self.generar_exponencial_negativa(media) for _ in range(n)])

    def generar_normales(self, media, desviacion, n) -> list:
        datos = []
        while len(datos) < n:
            u1 = self.generar_uniforme(0, 1)
            u2 = self.generar_uniforme(0, 1)
            # Evitar que u1 sea 0 o 1 ya que el logaritmo de 0 no está definido y la raiz de un número negativo tampoco
            if u1 == 0:
                u1 = 0.0001
            n1 = round(((np.sqrt(-2 * np.log(u1))) * np.cos(2 * np.pi * u2)) * desviacion + media, 4)
            n2 = round(((np.sqrt(-2 * np.log(u1))) * np.sin(2 * np.pi * u2)) * desviacion + media, 4)
            datos.append(n1)
            datos.append(n2)

        if n % 2 != 0:
            return datos[:-1]  # Si la cantidad de datos es impar, se elimina el último elemento
        return datos

    def generar_uniforme(self, a, b) -> float:
        rnd = np.random.rand()
        if a == 0 and b == 1:
            return round(rnd,4)
        return round(rnd,4), round(rnd * (b - a) + a, 4)

    def generar_exponencial_negativa(self, media) -> float:
        rnd = np.random.rand()
        lam = 1 / media
        num = - (1.0 / lam) * np.log(1 - rnd)
        return round(rnd,4), round(num, 4)

    # def generar_normal(self, media, desviacion, k=12) -> float:
    #     x = 0
    #     for _ in range(0, k + 1):
    #         x += (self.generar_uniforme(0, 1) - k / 2) / np.sqrt(k / 12)  # método de convolución
    #     return round(media + desviacion * x, 4)

# def definirIntervalos(numeros, cantidad_intervalos,a,b):
#     longitud_intervalo = (b - a) / cantidad_intervalos
#     intervalos = []
#     tagIntervalos = []
#     for i in range(cantidad_intervalos + 1):
        
#         intervalo = a + i * longitud_intervalo
#         intervaloLimite = a + (i+1) * longitud_intervalo
#         if i != (cantidad_intervalos - 1 ):
#             tagIntervalos.append('[{:.4f} - {:.4f})'.format(intervalo, intervaloLimite))
#         else:
#             tagIntervalos.append('[{:.4f} - {:.4f}]'.format(intervalo, intervaloLimite))
#         intervalos.append(round(intervalo,4))
#     frecuencia_intervalo = []
#     for intervalo in intervalos[:-1]:# Se excluye el último intervalo porque sino da 1 intervalo de mas
#         conteo = 0
#         for num in numeros:
#             if intervalo <= num < intervalo + longitud_intervalo:
#                 conteo +=1
#         frecuencia_intervalo.append(conteo)
    
#     return intervalos[:-1], frecuencia_intervalo, tagIntervalos[:-1]
# # Ejemplo de uso
# generador = GeneradorAleatorio(seed=42)
#
# # Generar 10 números aleatorios uniformes entre 0 y 100
# print(generador.generar_numeros_uniformes(0, 100, 10))
# def generarHistograma(numeros,cantIntervalos):
#     plt.clf()
#     plt.hist(numeros, bins=cantIntervalos, edgecolor='black')
#     plt.xlabel('Intervalos')
#     plt.ylabel('Frecuencia')
#     plt.title('Histograma Personalizado')
#     plt.grid(True)

#     fig = plt.gcf()
#     buff = BytesIO()
#     fig.savefig(buff, format='png')
#     buff.seek(0)

#     string = base64.b64encode(buff.read())
#     uri = urllib.parse.quote(string)
#     return uri
