from funciones import GeneradorAleatorio
import numpy as np
import copy
class Fila():
    def __init__(self,generador:GeneradorAleatorio,reloj_actual: float,simulacion):
        self.generador = generador
        self.simulacion = simulacion
        self.iteracion = None

        # Reloj
        self.siguiente_reloj = None
        self.evento = None
        self.reloj_actual = reloj_actual
        
        #llegada_cliente
        self.rnd_llegada_cliente = None
        self.tiempo_llegada_cliente = None
        self.proxima_llegada_cliente = None
        self.rnd_tamaño = None
        self.tamaño_grupo = None

        #toma_pedido
        self.rnd_tiempo_toma_pedido = None
        self.tiempo_toma_pedido = None
        self.tamaño_grupo_pidiendo = None
        self.fin_toma_pedido = None
        self.fin_toma_pedido_mozos = [None] * self.simulacion.cant_mozos

        #preparacion_pedido
        self.rnd_seleccion = None
        self.menu_seleccionado = None
        self.tiempo_de_preparacion = None
        self.fin_preparacion = None
        self.fin_preparacion_mesas = [None] * self.simulacion.cant_mesas

        #llevado_pedido
        self.rnd_llevado_pedido = None
        self.tiempo_de_llevado_pedido = None
        self.fin_llevado_pedido = None
        self.fin_llevado_pedido_mozos = [None] * self.simulacion.cant_mozos

        #retiro_clientes
        self.rnd1 = None
        self.rnd2 = None
        self.n1 = None
        self.n2 = None
        self.tiempo_para_comer = None
        self.fin_comer = None
        self.fin_comer_mesas = [None] * self.simulacion.cant_mesas

        #Mesas
        self.mesas = copy.copy(self.simulacion.mesas)
        self.cola_mesas = copy.copy(self.simulacion.cola_mesas)

        #Mozos
        self.mozos = copy.copy(self.simulacion.mozos)

        #Estadisticas
        self.personas_totales = self.simulacion.personas_totales
        self.personas_atendidas = self.simulacion.personas_atendidas
        self.personas_rechazadas = self.simulacion.personas_rechazadas

        #Grupos
        self.grupos = copy.copy(self.simulacion.grupos)


    def cerrarFila(self):
        self.cola_mesas = copy.deepcopy(self.simulacion.cola_mesas)
        self.mesas = copy.deepcopy(self.simulacion.mesas)
        self.mozos = copy.deepcopy(self.simulacion.mozos)
        self.grupos = copy.deepcopy(self.simulacion.grupos)
        self.personas_totales = self.simulacion.personas_totales
        self.personas_atendidas = self.simulacion.personas_atendidas
        self.personas_rechazadas = self.simulacion.personas_rechazadas

    def calcLlegadaCliente(self):
        """Calcula los datos random de la llegada de clientes"""
        if self.simulacion.llegada_clientes_es_media:
            self.rnd_llegada_cliente,self.tiempo_llegada_cliente = self.generador.generar_exponencial_negativa(self.simulacion.llegada_clientes_min)
        else:
            self.rnd_llegada_cliente = None
            self.tiempo_llegada_cliente = self.simulacion.llegada_clientes_min
        if self.tiempo_llegada_cliente <= 0:
            self.tiempo_llegada_cliente = 0.1
        self.proxima_llegada_cliente = self.reloj_actual + self.tiempo_llegada_cliente
        return self.proxima_llegada_cliente
    
    def calcTamañoGrupo(self):
        """Calcula el tamaño del grupo"""
        acumulado = 0
        for grupo in self.simulacion.grupos_items:
            acumulado += grupo["P(%)"]
            if self.rnd_tamaño < acumulado:
                return grupo["Tamaño"]
            if self.rnd_tamaño == 1:
                return self.simulacion.grupos_items[-1]["Tamaño"]
        return None
    def calcTomaPedido(self, grupo):
        """Calcula los datos random de la toma de pedido"""
        tamaño = grupo.tamaño
        if self.simulacion.toma_pedido_es_media:
            self.rnd_tiempo_toma_pedido,self.tiempo_toma_pedido = self.generador.generar_exponencial_negativa(self.simulacion.toma_pedido_min)
        else:
            self.rnd_tiempo_toma_pedido = None
            self.tiempo_toma_pedido = self.simulacion.toma_pedido_min
        if self.tiempo_toma_pedido <= 0:
            self.tiempo_toma_pedido = 0.1
        self.fin_toma_pedido = self.reloj_actual + (self.tiempo_toma_pedido * tamaño) 
        return self.fin_toma_pedido

    def calcMenu(self,rnd):
        """Calcula el menu seleccionado"""
        acumulado = 0
        rnd = 0.33
        for menu in self.simulacion.menu_items:
            acumulado += menu["P(%)"]
            if rnd < acumulado:
                return menu
            if rnd == 1:
                return self.simulacion.menu_items[-1]
        return None

    def calcPreparacionPedido(self):
        """Calcula los datos random de la preparacion de pedido"""
        self.rnd_seleccion = self.generador.generar_uniforme(0,1)
        self.menu_seleccionado = self.calcMenu(self.rnd_seleccion)
        #print(f'RND seleccion: {self.rnd_seleccion}, Menu seleccionado: {self.menu_seleccionado}')
        self.tiempo_de_preparacion = self.menu_seleccionado["Minutos preparacion"]
        if self.tiempo_de_preparacion <= 0:
            self.tiempo_de_preparacion = 0.1
        self.fin_preparacion = self.reloj_actual + self.tiempo_de_preparacion
        return self.fin_preparacion

    def calcLlevadoPedido(self):
        """Calcula los datos random del llevado de pedido"""
        if self.simulacion.llevado_pedido_es_media:
            self.rnd_llevado_pedido,self.tiempo_de_llevado_pedido = self.generador.generar_exponencial_negativa(self.simulacion.llevado_pedido_min)
        else:
            self.rnd_llevado_pedido = None
            self.tiempo_de_llevado_pedido = self.simulacion.llevado_pedido_min
        if self.tiempo_de_llevado_pedido <= 0:
            self.tiempo_de_llevado_pedido = 0.1
        self.fin_llevado_pedido = self.reloj_actual + self.tiempo_de_llevado_pedido
        return self.fin_llevado_pedido
    
    def calcRNDSRetiroClientes(self):
        """Calcula los random del retiro de clientes por primera vez, se usa otra funcion cuando los N ya estan definidos"""
        self.rnd1 = self.generador.generar_uniforme(0,1)
        self.rnd2 = self.generador.generar_uniforme(0,1)
        self.n1,self.n2 = self.generador.generar_normales(self.simulacion.comer_media,self.simulacion.comer_desv_estandar,2)
        self.simulacion.n2 = self.n2
        return self.rnd1,self.rnd2,self.n1,self.n2
    
    def calcComer(self):
        if self.n2:
            self.tiempo_para_comer = self.n2
            self.simulacion.n2 = None
        else:
            self.calcRNDSRetiroClientes()
            self.tiempo_para_comer = self.n1
        if self.tiempo_para_comer <= 0:
            self.tiempo_para_comer = 0.1
        self.fin_comer = self.reloj_actual + self.tiempo_para_comer
        return self.fin_comer
    def calcSiguienteEvento(self):
        """
        Busca el menor valor entre los atributos de tiempo relevantes.
        Retorna una lista de eventos con el mismo tiempo mínimo y el valor mínimo.
        """
        # Lista de atributos a considerar
        atributos = {
            "proxima_llegada_cliente": self.proxima_llegada_cliente,
            "fin_toma_pedido_mozos": min([v for v in self.fin_toma_pedido_mozos if v is not None], default=None),
            "fin_preparacion_mesas": min([v for v in self.fin_preparacion_mesas if v is not None], default=None),
            "fin_llevado_pedido_mozos": min([v for v in self.fin_llevado_pedido_mozos if v is not None], default=None),
            "fin_comer_mesas": min([v for v in self.fin_comer_mesas if v is not None], default=None),
        }
        
        # Filtramos los atributos que no son None
        atributos_filtrados = {k: v for k, v in atributos.items() if v is not None}

        # Encontramos el menor valor
        valor_min = min(atributos_filtrados.values())
        
        # Encontramos todos los nombres que tienen el valor mínimo
        nombres_min = [k for k, v in atributos_filtrados.items() if v == valor_min]
        if len(nombres_min) >= 1:
            self.evento = nombres_min[0]
        self.siguiente_reloj = valor_min
        return nombres_min, valor_min
    
    def parseFila(self):
        """
        Parsea la fila para mostrarla en la interfaz.
        Convierte todos los valores en strings.
        """
        def redondear(valor):
            return str(np.round(valor, 4)) if isinstance(valor, (int, float)) else str(valor)
        fila = {}
        fila["i"] = self.iteracion
        fila["Evento"] = str(self.evento)
        fila["Reloj Actual"] = redondear(self.reloj_actual)

        if self.simulacion.llegada_clientes_es_media:
            fila["RND Llegada"] = redondear(self.rnd_llegada_cliente)
        fila["Tiempo llegada"] = redondear(self.tiempo_llegada_cliente)
        fila["Prox llegada cliente"] = redondear(self.proxima_llegada_cliente)
        fila["RND tamaño"] = redondear(self.rnd_tamaño)
        fila["Tamaño grupo"] = redondear(self.tamaño_grupo)


        if self.simulacion.toma_pedido_es_media:
            fila["RND toma pedido"] = redondear(self.rnd_tiempo_toma_pedido)
        fila["Tiempo toma pedido"] = redondear(self.tiempo_toma_pedido)
        fila["Fin toma pedido"] = redondear(self.fin_toma_pedido)

        for i in range(len(self.fin_llevado_pedido_mozos)):
            fila["Fin toma pedido mozo " + str(i+1)] = redondear(self.fin_toma_pedido_mozos[i])

        fila["RND Seleccion"] = redondear(self.rnd_seleccion)
        fila["Menu seleccionado"] = str(self.menu_seleccionado["Menu"]) if self.menu_seleccionado else "None"
        fila["Tiempo de preparacion"] = redondear(self.tiempo_de_preparacion)
        fila["Fin preparacion"] = redondear(self.fin_preparacion)

        for i in range(len(self.fin_preparacion_mesas)):
            fila["Fin preparacion mesa " + str(i+1)] = redondear(self.fin_preparacion_mesas[i])

        if self.simulacion.llevado_pedido_es_media:
            fila["RND llevado pedido"] = redondear(self.rnd_llevado_pedido)
        fila["Tiempo de llevado pedido"] = redondear(self.tiempo_de_llevado_pedido)

        for i in range(len(self.fin_llevado_pedido_mozos)):
            fila["Fin llevado pedido mozo " + str(i+1)] = redondear(self.fin_llevado_pedido_mozos[i])

        fila["RND 1"] = redondear(self.rnd1)
        fila["RMD 2"] = redondear(self.rnd2)
        fila["N1"] = redondear(self.n1)
        fila["N2"] = redondear(self.n2)
        fila["Tiempo para comer"] = redondear(self.tiempo_para_comer)
        fila["Fin comer"] = redondear(self.fin_comer)

        for i in range(len(self.fin_comer_mesas)):
            fila["Fin comer mesa " + str(i+1)] = redondear(self.fin_comer_mesas[i])

        for i in range(len(self.mesas)):
            fila["Mesa " + str(i+1)] = str(self.mesas[i].estado)
        fila["Cola mesas"] = redondear(len(self.cola_mesas))

        for i in range(len(self.mozos)):
            fila["Mozo " + str(i+1)] = str(self.mozos[i].estado)

        
        fila["Personas Totales"] = redondear(self.personas_totales)
        fila["Personas Atendidas"] = redondear(self.personas_atendidas)
        fila["Personas Rechazadas"] = redondear(self.personas_rechazadas)
        fila["grupos"] = []
        for grupo in self.grupos:
            fila["grupos"].append({
                "id_grupo": grupo.id_grupo,
                "tamaño": grupo.tamaño,
                "estado": grupo.estado
            })

        return fila

    def __str__(self):
        print(f"Reloj: {self.reloj_actual}, Evento: {self.evento}, Proxima llegada cliente: {self.proxima_llegada_cliente}, Fin toma pedido: {self.fin_toma_pedido_mozos}, Fin preparacion: {self.fin_preparacion_mesas}, Fin llevado pedido: {self.fin_llevado_pedido_mozos}, Fin comer: {self.fin_comer_mesas}")
        print("-----Mesas-----")
        for mesa in self.mesas:
            print(mesa)
        print("-----Mozos-----")
        for mozo in self.mozos:
            print(mozo)
        print("-----Grupos-----")
        for grupo in self.grupos:
            print(grupo)
        return " "
