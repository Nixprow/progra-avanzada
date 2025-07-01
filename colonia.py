from bacteria import Bacteria
from ambiente import Ambiente
import random
import csv
import pandas as pd


class Colonia:
    def __init__(self, filas=10, columnas=10):
        self.__filas = filas
        self.__columnas = columnas
        self.__ambiente = Ambiente(filas, columnas)
        self.__bacterias = []  # Lista de bacterias 

    def get_bacterias(self):
        return self.__bacterias

    def get_ambiente(self):
        return self.__ambiente

    def agregar_bacteria(self, bacteria, fila, columna):
        
        #Agrega una bacteria a la colonia y la ubica en el ambiente si la celda está vacía.
        
        if self.__ambiente.get_grilla()[fila][columna] == 0:
            self.__bacterias.append((bacteria, fila, columna))
            valor = 3 if bacteria.es_resistente() else 1
            self.__ambiente.set_grilla_valor(fila, columna, valor)
            #Ejemplo self.__ambiente.get_grilla()= 1,2,0 segun si esta vacio el espacio, esta viva, o muerta la bacteria

    def paso(self):
        
        #Ejecuta un paso de simulación: alimentar, aplicar ambiente, dividir, morir, difundir.
        
        nuevas_bacterias = []
        matriz_consumo = [[0 for _ in range(self.__columnas)] for _ in range(self.__filas)]

        for b in self.__bacterias:
            bacteria, x, y = b

            if not bacteria.esta_vivo():
                continue

            # Alimentar con cantidad aleatoria
            cantidad = random.randint(15, 50)
            bacteria.alimentar(cantidad)
            matriz_consumo[x][y] = cantidad

            # Aplicar antibiótico si corresponde
            self.__ambiente.aplicar_ambiente(x, y, bacteria)

            # Si muere, se le asigna el valor de 2
            if not bacteria.esta_vivo():
                self.__ambiente.set_grilla_valor(x,y, 2)
                continue

            # Si está viva y resistente, se le asigna el valor de 3
            if bacteria.es_resistente():
                self.__ambiente.set_grilla_valor(x, y, 3)

            # Intentar dividir
            if bacteria.get_energia() >= 80:
                hija = bacteria.dividirse()
                if hija is not None:
                    # Posibilidad de mutar (5%)
                    if random.random() < 0.05:
                        hija.mutar()

                    # Buscar vecinos cardinales simples (ya que la otra funcion no funcionaba .-.)
                    if x > 0 and self.__ambiente.get_grilla()[x-1][y] == 0:
                        self.__ambiente.set_grilla_valor(x-1, y, 3 if hija.es_resistente() else 1)
                        nuevas_bacterias.append((hija, x-1, y))
                    elif x < self.__filas - 1 and self.__ambiente.get_grilla()[x+1][y] == 0:
                        self.__ambiente.set_grilla_valor(x+1, y, 3 if hija.es_resistente() else 1)
                        nuevas_bacterias.append((hija, x+1, y))
                    elif y > 0 and self.__ambiente.get_grilla()[x][y-1] == 0:
                        self.__ambiente.set_grilla_valor(x, y-1, 3 if hija.es_resistente() else 1)
                        nuevas_bacterias.append((hija, x, y-1))
                    elif y < self.__columnas - 1 and self.__ambiente.get_grilla()[x][y+1] == 0:
                        self.__ambiente.set_grilla_valor(x, y+1, 3 if hija.es_resistente() else 1)
                        nuevas_bacterias.append((hija, x, y+1))

        # Actualizar ambiente
        self.__ambiente.actualizar_nutrientes(matriz_consumo)
        self.__ambiente.difundir_nutrientes()

        # Agregar nuevas bacterias
        self.__bacterias.extend(nuevas_bacterias)

    def reporte_estado(self):
        
        #Muestra el estado general de la colonia.
        #Se determinan variables para almacenar la informacion sobre bacterias, vivas, muertas o resistentes
        vivas = 0
        muertas = 0
        resistentes = 0

        for b, _, _ in self.__bacterias:
            if b.esta_vivo():
                vivas += 1
                if b.es_resistente():
                    resistentes += 1
            else:
                muertas += 1

        print(f"[REPORTE] Vivas: {vivas} | Muertas: {muertas} | Resistentes: {resistentes}")
    # El método importar_csv ha sido eliminado. Ahora la lógica de importación se maneja en simulador.py
    def exportar_csv(self, nombre="colonia_estado.csv"):
        # Exporta el estado de las bacterias a un archivo.csv usando pandas
        import pandas as pd
        data = []
        for b, _, _ in self.__bacterias:
            data.append({
                "ID": b.get_id(),
                "Raza": b.get_raza(),
                "Energía": b.get_energia(),
                "Estado": "Viva" if b.esta_vivo() else "Muerta",
                "Resistente": "Si" if b.es_resistente() else "No"
            })
        df = pd.DataFrame(data)
        df.to_csv(nombre, index=False, encoding="utf-8")
