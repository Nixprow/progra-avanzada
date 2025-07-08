from bacteria import Espiroqueta, Estreptococo  #colonia.py importa Espiroqueta y Estreptococo, las cuales son bacterias hijas de Bacteria
from ambiente import Ambiente  # colonia.py importa ambiente.py aquí
import random
import pandas as pd

#Hacer uso del import de bacteria y usarlo
class Colonia():
    def __init__(self, filas=10, columnas=10):
        self.__filas = filas
        self.__columnas = columnas
        self.__ambiente = Ambiente(filas, columnas)  # Interacción: Colonia crea un Ambiente
        self.__bacterias = []  # Interacción: Colonia mantiene la lista de bacterias

    def get_bacterias(self):
        #Usado por SimuladorWindow y para importar/exportar bacterias
        return self.__bacterias

    def get_ambiente(self):
        # Usado por SimuladorWindow para graficar la grilla
        return self.__ambiente

    def agregar_bacteria(self, tipo="Estreptococo", fila=None, columna=None):
        # Llamado por SimuladorWindow y al importar CSV
        # Colonia crea instancias de Espiroqueta/Estreptococo aquí
        if tipo == "Espiroqueta":
            bacteria = Espiroqueta()
        elif tipo == "Estreptococo":
            bacteria = Estreptococo()
        else:
            return False
        grilla = self.__ambiente.get_grilla()
        if fila is None or columna is None:
            vacias = [(x, y) for x in range(self.__filas) for y in range(self.__columnas) if grilla[x][y] == 0]
            if not vacias:
                return False
            fila, columna = random.choice(vacias)
        if grilla[fila][columna] == 0:
            self.__bacterias.append(bacteria)
            valor = 3 if bacteria.es_resistente() else 1
            self.__ambiente.set_grilla_valor(fila, columna, valor)
            # Guarda la posición en la bacteria
            bacteria.fila = fila
            bacteria.columna = columna
            return True
        return False

    def paso(self):
        # Llamado por SimuladorWindow para avanzar la simulación
        # Ejecuta un paso de simulación usando objetos Bacteria
        matriz_consumo = [[0 for _ in range(self.__columnas)] for _ in range(self.__filas)]
        nuevas_bacterias = []
        for bacteria in self.__bacterias:
            x, y = bacteria.fila, bacteria.columna
            if not bacteria.esta_vivo():
                continue
            cantidad = random.randint(15, 50)
            bacteria.alimentar(cantidad)
            matriz_consumo[x][y] = cantidad
            self.__ambiente.aplicar_ambiente(x, y, bacteria)
            if not bacteria.esta_vivo():
                self.__ambiente.set_grilla_valor(x, y, 2)
                continue
            if bacteria.es_resistente():
                self.__ambiente.set_grilla_valor(x, y, 3)
            if bacteria.get_energia() >= 80:
                hija = bacteria.dividirse()
                if hija is not None:
                    # Buscar vecinos 
                    # Arriba
                    if x > 0 and self.__ambiente.get_grilla()[x-1][y] == 0:
                        self.__ambiente.set_grilla_valor(x-1, y, 3 if hija.es_resistente() else 1)
                        hija.fila, hija.columna = x-1, y
                        nuevas_bacterias.append(hija)
                    # Abajo
                    elif x < self.__filas - 1 and self.__ambiente.get_grilla()[x+1][y] == 0:
                        self.__ambiente.set_grilla_valor(x+1, y, 3 if hija.es_resistente() else 1)
                        hija.fila, hija.columna = x+1, y
                        nuevas_bacterias.append(hija)
                    # Izquierda
                    elif y > 0 and self.__ambiente.get_grilla()[x][y-1] == 0:
                        self.__ambiente.set_grilla_valor(x, y-1, 3 if hija.es_resistente() else 1)
                        hija.fila, hija.columna = x, y-1
                        nuevas_bacterias.append(hija)
                    # Derecha
                    elif y < self.__columnas - 1 and self.__ambiente.get_grilla()[x][y+1] == 0:
                        self.__ambiente.set_grilla_valor(x, y+1, 3 if hija.es_resistente() else 1)
                        hija.fila, hija.columna = x, y+1
                        nuevas_bacterias.append(hija)
        self.__ambiente.actualizar_nutrientes(matriz_consumo)
        self.__ambiente.difundir_nutrientes()
        self.__bacterias.extend(nuevas_bacterias)

    def reporte_estado(self):
        # Llamado por SimuladorWindow para mostrar el estado actual
        # Muestra el estado general de la colonia.
        # Se determinan variables para almacenar la informacion sobre bacterias, vivas, muertas o resistentes
        vivas = 0
        muertas = 0
        resistentes = 0

        for b in self.__bacterias:
            if b.esta_vivo():
                vivas += 1
                if b.es_resistente():
                    resistentes += 1
            else:
                muertas += 1

        print(f"[REPORTE] Vivas: {vivas} | Muertas: {muertas} | Resistentes: {resistentes}")
        return vivas, muertas, resistentes
    
    def exportar_csv(self, nombre="colonia_estado.csv"):
        # Llamado por SimuladorWindow para exportar el estado de la colonia
        data = [{
            "ID": b.get_id(),
            "Raza": b.get_raza(),
            "Energía": b.get_energia(),
            "Estado": "Viva" if b.esta_vivo() else "Muerta",
            "Resistente": "Si" if b.es_resistente() else "No"
        } for b in self.__bacterias]
        pd.DataFrame(data).to_csv(nombre, index=False, encoding="utf-8")
