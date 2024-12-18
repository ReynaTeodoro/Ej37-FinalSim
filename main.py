from Clases.simulacion import Simulacion
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.ui import Ui_SimulacionRestaurant
import sys
def main():
    
    app = QtWidgets.QApplication(sys.argv)
    SimulacionRestaurant = QtWidgets.QWidget()
    ui = Ui_SimulacionRestaurant()
    ui.setupUi(SimulacionRestaurant)
    SimulacionRestaurant.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    # simulacion = Simulacion(
    #     seed = 2,
    #     minuto_inicial=1.0,
    #     minuto_corte=1000.0,
    #     mostrar_desde=1,
    #     iteraciones_a_mostrar=100,
    #     cant_mesas=6,
    #     cant_mozos=1,
    #     llegada_clientes_min=10.0,
    #     llegada_clientes_es_media=False,
    #     toma_pedido_min=1.0,
    #     toma_pedido_es_media=False,
    #     llevado_pedido_min=2.0,
    #     llevado_pedido_es_media=False,
    #     comer_media=60.0,
    #     comer_desv_estandar=20.0,
    #     menu_items=[
    #         {"Menu": "Tm1", "P(%)": 0.33, "Minutos preparacion": 10},
    #         {"Menu": "Tm2", "P(%)": 0.33, "Minutos preparacion": 15},
    #         {"Menu": "Tm3", "P(%)": 0.34, "Minutos preparacion": 18}
    #     ],
    #     grupos_items=[
    #         {"Tamaño": 1, "P(%)": 0.25},
    #         {"Tamaño": 2, "P(%)": 0.25},
    #         {"Tamaño": 3, "P(%)": 0.25},
    #         {"Tamaño": 4, "P(%)": 0.25}
    #     ]
    # )
    main()
