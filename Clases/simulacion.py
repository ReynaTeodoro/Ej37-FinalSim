from typing import List
from Clases.mozo import Mozo
from Clases.mesa import Mesa
from Clases.grupo import Grupo
from Clases.fila import Fila
import numpy as np
import copy

from funciones import GeneradorAleatorio
class Simulacion:
    def __init__(self,
                 seed: int,
                 minuto_inicial: float,
                 minuto_corte: float,
                 mostrar_desde: int,
                 iteraciones_a_mostrar: int,
                 cant_mesas: int,
                 cant_mozos: int,
                 llegada_clientes_min: float,
                 llegada_clientes_es_media: bool,
                 toma_pedido_min: float,
                 toma_pedido_es_media: bool,
                 llevado_pedido_min: float,
                 llevado_pedido_es_media: bool,
                 comer_media: float,
                 comer_desv_estandar: float,
                 menu_items: List[dict],
                 grupos_items: List[dict]):
        """
        Clase para representar los datos de simulación.
        :param seed: Semilla para el generador de números aleatorios.
        :param minuto_inicial: Tiempo inicial en minutos (To).
        :param minuto_corte: Tiempo de corte en minutos (Tc).
        :param mostrar_desde: Iteración desde la que se muestran los resultados.
        :param iteraciones_a_mostrar: Número de iteraciones a mostrar.
        :param cant_mesas: Número de mesas en el restaurante.
        :param cant_mozos: Número de mozos disponibles.
        :param llegada_clientes_min: Tiempo de llegada de clientes en minutos.
        :param llegada_clientes_es_media: Indica si el tiempo de llegada es una media.
        :param toma_pedido_min: Tiempo de toma de pedido en minutos.
        :param toma_pedido_es_media: Indica si el tiempo de toma de pedido es una media.
        :param llevado_pedido_min: Tiempo de llevado de pedido en minutos.
        :param llevado_pedido_es_media: Indica si el tiempo de llevado de pedido es una media.
        :param comer_media: Media para el tiempo de corner (distribución normal).
        :param comer_desv_estandar: Desviación estándar para el tiempo de corner.
        :param menu_items: Lista de ítems del menú, cada uno con "Menu", "P(%)" y "Minutos preparacion".
        :param grupos_items: Lista de tamaños de grupo, cada uno con "Tamaño" y "P(%)".
        """
        self.seed = seed
        self.minuto_inicial = minuto_inicial
        self.minuto_corte = minuto_corte
        self.mostrar_desde = mostrar_desde
        self.iteraciones_a_mostrar = iteraciones_a_mostrar
        self.cant_mesas = cant_mesas
        self.cant_mozos = cant_mozos
        self.llegada_clientes_min = llegada_clientes_min
        self.llegada_clientes_es_media = llegada_clientes_es_media
        self.toma_pedido_min = toma_pedido_min
        self.toma_pedido_es_media = toma_pedido_es_media
        self.llevado_pedido_min = llevado_pedido_min
        self.llevado_pedido_es_media = llevado_pedido_es_media
        self.comer_media = comer_media
        self.comer_desv_estandar = comer_desv_estandar
        self.menu_items = menu_items
        self.grupos_items = grupos_items

        self.generador = GeneradorAleatorio(seed=seed)
        self.filas = [] 
        self.mesas = []
        self.mozos = []
        self.cola_mesas = []
        self.grupos = []
        self.reloj = 0.0
        

        self.personas_totales = 0
        self.personas_rechazadas = 0
        self.personas_atendidas = 0
    def __str__(self):
        return f"Semilla: {self.seed}\n" \
                f"Minuto inicial: {self.minuto_inicial}\n" \
                f"Minuto corte: {self.minuto_corte}\n" \
                f"Mostrar desde: {self.mostrar_desde}\n" \
                f"Iteraciones a mostrar: {self.iteraciones_a_mostrar}\n" \
                f"Mesas: {self.cant_mesas}\n" \
                f"Mozos: {self.cant_mozos}\n" \
                f"Llegada clientes min: {self.llegada_clientes_min}\n" \
                f"Llegada clientes es media: {self.llegada_clientes_es_media}\n" \
                f"Toma pedido min: {self.toma_pedido_min}\n" \
                f"Toma pedido es media: {self.toma_pedido_es_media}\n" \
                f"Llevado pedido min: {self.llevado_pedido_min}\n" \
                f"Llevado pedido es media: {self.llevado_pedido_es_media}\n" \
                f"Comer media: {self.comer_media}\n" \
                f"Comer desv estandar: {self.comer_desv_estandar}\n" \
                f"Menu items: {self.menu_items}\n" \
                f"Grupos items: {self.grupos_items}\n" \
                f"Generador: {self.generador}"
    def obtenerIdGrupo(self):
        return len(self.grupos) + 1
    def inicializar(self):
        #crear mesas
        self.mesas = [Mesa(i) for i in range(1, self.cant_mesas + 1)]
        #crear mozos
        self.mozos = [Mozo(i) for i in range(1, self.cant_mozos + 1)]
        fila = Fila(self.generador, self.reloj,self)
        fila.evento = "Inicializar"
        fila.calcLlegadaCliente()
        return fila
    def crearFilaNueva(self):
        fila = Fila(self.generador, self.reloj,self)
        if len(self.filas) > 0:
            fila.proxima_llegada_cliente = self.filas[-1].proxima_llegada_cliente
            fila.fin_toma_pedido_mozos = copy.deepcopy(self.filas[-1].fin_toma_pedido_mozos)
            fila.fin_preparacion_mesas = copy.deepcopy(self.filas[-1].fin_preparacion_mesas)
            fila.fin_llevado_pedido_mozos = copy.deepcopy(self.filas[-1].fin_llevado_pedido_mozos)
            fila.fin_comer_mesas = copy.deepcopy(self.filas[-1].fin_comer_mesas)
            fila.n2 = self.filas[-1].n2
            
        return fila
    def eventoLlegadaCliente(self,fila:Fila):
        rndTamaño = self.generador.generar_uniforme(0,1)
        fila.rnd_tamaño = rndTamaño
        grupo = Grupo(self.obtenerIdGrupo(), fila.calcTamañoGrupo())
        fila.tamaño_grupo = grupo.tamaño
        #print(f"rndTamaño: {rndTamaño} - grupo {grupo.id_grupo} - tamaño: {grupo.tamaño}")
        self.personas_totales += grupo.tamaño
        for mesa in self.mesas:
            if mesa.estaLibre():
                mesa_libre = mesa
                grupo.mesa = mesa
                mesa.ocupar()
                grupo.estado = "Esperando toma de pedido"
                self.personas_atendidas += grupo.tamaño
                break
        if grupo.mesa is None:
            if self.cola_mesas == []:
                grupo.estado = "Esperando mesa"
                self.personas_atendidas += grupo.tamaño
                self.cola_mesas.append(grupo)
            else:
                #print("Grupo rechazado")
                grupo.estado = "Rechazado"
                self.personas_rechazadas += grupo.tamaño
        #Iniciar tomar de pedido si hay mozo disponible
        for mozo in self.mozos:
            if mozo.estaLibre() and grupo.estado == "Esperando toma de pedido":
                mozo.ocupar()
                mozo.enMesa = grupo.mesa
                grupo.estado = "Eligiendo pedido"
                grupo.mozo = mozo
                fin_toma_pedido = fila.calcTomaPedido(grupo)
                fila.fin_toma_pedido = fin_toma_pedido
                fila.fin_toma_pedido_mozos[mozo.id-1] = fila.fin_toma_pedido
                break
        self.grupos.append(grupo)
        fila.evento = f'Llegada de cliente {grupo.id_grupo}' 
        #obtiene la siguiente llegada de cliente
        fila.calcLlegadaCliente()

    def eventoFinTomaPedido(self,fila:Fila):
        indice_mozo = min((i for i, v in enumerate(fila.fin_toma_pedido_mozos) if v is not None), key=lambda i: fila.fin_toma_pedido_mozos[i])
        fila.fin_toma_pedido_mozos[indice_mozo] = None
        mozo = self.mozos[indice_mozo]
        for grupo in self.grupos:
            if grupo.mesa == mozo.enMesa and grupo.estado == "Eligiendo pedido":
                grupo.estado = "Esperando pedido"
                fin_preparacion = fila.calcPreparacionPedido()
                fila.fin_preparacion = fin_preparacion
                fila.fin_preparacion_mesas[grupo.mesa.numero-1] = fin_preparacion
                break
        fila.evento = f'Fin Toma de pedido - mesa {mozo.enMesa.numero}'
        mozo.desocupar()
       
    def eventoFinPreparacionPedido(self,fila:Fila):
        indice_mesa = min((i for i, v in enumerate(fila.fin_preparacion_mesas) if v is not None), key=lambda i: fila.fin_preparacion_mesas[i])
        mesa = self.mesas[indice_mesa]
        for grupo in self.grupos:
            if grupo.mesa == mesa and grupo.estado == "Esperando pedido":
                grupo.estado = "Esperando entrega pedido"
                mesa.estado = "Pedido listo"
                break
        for grupo in self.grupos:
            if grupo.estado == "Esperando toma de pedido":
                #Priorizar toma de pedido
                for mozo in self.mozos:
                    if mozo.estaLibre():
                        mozo.ocupar()
                        mozo.enMesa = grupo.mesa
                        grupo.estado = "Eligiendo pedido"
                        grupo.mozo = mozo
                        fin_toma_pedido = fila.calcTomaPedido(grupo)
                        fila.fin_toma_pedido = fin_toma_pedido
                        fila.fin_toma_pedido_mozos[mozo.id-1] = fila.fin_toma_pedido
                        break
        for mozo in self.mozos:
            if mozo.estaLibre() :
                mozo.ocupar()
                mozo.enMesa = mesa
                grupo.estado = "Esperando entrega pedido"
                grupo.mozo = mozo
                fin_llevado_pedido = fila.calcLlevadoPedido()
                fila.fin_llevado_pedido = fin_llevado_pedido
                fila.fin_llevado_pedido_mozos[mozo.id-1] = fin_llevado_pedido
                break
        fila.fin_preparacion_mesas[indice_mesa] = None
        fila.evento = f'Fin Preparacion de pedido - mesa {mesa.numero}'

    def eventoFinLlevadoPedido(self,fila:Fila):
        indice_mozo = min((i for i, v in enumerate(fila.fin_llevado_pedido_mozos) if v is not None), key=lambda i: fila.fin_llevado_pedido_mozos[i])
        fila.fin_llevado_pedido_mozos[indice_mozo] = None
        mozo = self.mozos[indice_mozo]
        for grupo in self.grupos:
            if grupo.mesa == mozo.enMesa and grupo.estado == "Esperando entrega pedido":
                grupo.estado = "Comiendo"
                fin_comer = fila.calcComer()
                fila.fin_comer = fin_comer
                fila.fin_comer_mesas[grupo.mesa.numero-1] = fin_comer
                break
        fila.evento = f'Fin Llevado de pedido - mesa {mozo.enMesa.numero}'
        mozo.desocupar()

    def eventoRetiroGrupo(self,fila:Fila):
        indice_mesa = min((i for i, v in enumerate(fila.fin_comer_mesas) if v is not None), key=lambda i: fila.fin_comer_mesas[i])
        mesa = self.mesas[indice_mesa]
        mesa.desocupar()
        for grupo in self.grupos:
            if grupo.mesa == mesa and grupo.estado == "Comiendo":
                grupo.estado = "Retirado"
                fila.personas_atendidas += grupo.tamaño
                break
        fila.fin_comer_mesas[indice_mesa] = None
        fila.evento = f'Retiro de clientes - mesa {mesa.numero}'
        self.finEsperaCola(fila)

    def finEsperaCola(self, fila:Fila):
        if len(self.cola_mesas) > 0:
            grupo = self.cola_mesas.pop(0)
            for mesa in self.mesas:
                if mesa.estaLibre():
                    mesa_libre = mesa
                    grupo.mesa = mesa
                    mesa.ocupar()
                    grupo.estado = "Esperando toma de pedido"
                    self.personas_atendidas += grupo.tamaño
                    break
            #Iniciar toma de pedido si hay mozo disponible
            for mozo in self.mozos:
                if mozo.estaLibre():
                    mozo.ocupar()
                    mozo.enMesa = grupo.mesa
                    grupo.estado = "Eligiendo pedido"
                    grupo.mozo = mozo
                    fin_toma_pedido = fila.calcTomaPedido(grupo)
                    fila.fin_toma_pedido = fin_toma_pedido
                    fila.fin_toma_pedido_mozos[mozo.id-1] = fila.fin_toma_pedido
                    break
                else:
                    grupo.estado = "Esperando toma de pedido"
        else:
            pass
            

    def simular(self):
        self.reloj = self.minuto_inicial
        i = 0
        while (len(self.filas)-1)<= self.minuto_corte :
            eventos=self.calcular_proximo_evento()
            #print(f"Eventos: {eventos}")
            for evento in eventos:
                min_minimo = evento[1]
                evento_nombre = evento[0]
                if min_minimo >= self.reloj:
                    self.reloj = min_minimo
                #print(f"Evento: {evento_nombre} - minimo: {min_minimo}")
                fila = self.simularEvento(evento_nombre)
                fila.iteracion = i
                fila.cerrarFila()
                #print(f"Iteración {i} - Evento: {fila.evento}")
           # print(fila)
            if not fila.evento:
                break
            i += 1
        print("Simulación finalizada")
        print(f"Personas totales: {self.personas_totales}")
        print(f"Personas atendidas: {self.personas_atendidas}")
        print(f"Personas rechazadas: {self.personas_rechazadas}")
    def get_resultados(self):
        filas_simulacion = []
        desde = self.minuto_inicial
        hasta = self.minuto_inicial + self.iteraciones_a_mostrar
        print(f"Desde: {desde} - Hasta: {hasta}")
        ultimaFila = self.filas[-1].parseFila()
        for i, fila in enumerate(self.filas):
            if i >= desde and i < hasta:
                filas_simulacion.append(fila.parseFila())
            elif i >= hasta:
                break
        filas_simulacion.append(ultimaFila)
        resultados = {
            "personas_totales": self.personas_totales,
            "personas_atendidas": self.personas_atendidas,
            "personas_rechazadas": self.personas_rechazadas,
            "porcentaje_rechazo": f'{np.round((self.personas_rechazadas/self.personas_totales)*100,4)}%'
        }
        return filas_simulacion, resultados
    def calcular_proximo_evento(self):
        if len(self.filas) == 0:
            # Caso inicial
            return [("Inicializar", self.minuto_inicial)]
        else:
            # Obtener la última fila y calcular los próximos eventos
            ultima_fila = self.filas[-1]
            nombres, valor = ultima_fila.calcSiguienteEvento()

            # Construir los resultados como una lista de tuplas
            resultados = []
            for nombre in nombres:
                if nombre == "proxima_llegada_cliente":
                    resultados.append(("Llegada de cliente", valor))
                elif nombre == "fin_toma_pedido_mozos":
                    resultados.append(("Fin Toma de pedido", valor))
                elif nombre == "fin_preparacion_mesas":
                    resultados.append(("Fin Preparacion de pedido", valor))
                elif nombre == "fin_llevado_pedido_mozos":
                    resultados.append(("Fin Llevado de pedido", valor))
                elif nombre == "fin_comer_mesas":
                    resultados.append(("Retiro de clientes", valor))
                else:
                    raise Exception(f"No se pudo determinar el próximo evento para {nombre}")
            
            # Retornar todos los eventos encontrados
            return resultados
    def simularEvento(self,evento):
        fila = self.crearFilaNueva()
        if evento == "Inicializar":
            fila = self.inicializar()
            self.filas.append(fila)
            return fila
        elif evento == "Llegada de cliente":
            self.eventoLlegadaCliente(fila)
            self.filas.append(fila)
            return fila
        elif evento == "Fin Toma de pedido":
            self.eventoFinTomaPedido(fila)
            self.filas.append(fila)
            return fila
        elif evento == "Fin Preparacion de pedido":
            self.eventoFinPreparacionPedido(fila)
            self.filas.append(fila)
            return fila
        elif evento == "Fin Llevado de pedido":
            self.eventoFinLlevadoPedido(fila)
            self.filas.append(fila)
            return fila
        elif evento == "Retiro de clientes":
            self.eventoRetiroGrupo(fila)
            self.filas.append(fila)
            return fila
        else:
            fila = Fila(self.generador,self.reloj,self)
            return fila
