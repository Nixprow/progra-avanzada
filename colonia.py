from bacteria import Bacteria
from ambiente import Ambiente
import random
import csv

class Colonia:
    def __init__(self, filas=10, columnas=10):
        self.__filas = filas
        self.__columnas = columnas
        self.__ambiente = Ambiente(filas, columnas)
        self.__bacterias = []  # Lista de bacterias activas

    def get_bacterias(self):
        return self.__bacterias

    def get_ambiente(self):
        return self.__ambiente

    def agregar_bacteria(self, bacteria, fila, columna):
        """
        Agrega una bacteria a la colonia y la ubica en el ambiente si la celda está vacía.
        """
        if self.__ambiente.get_grilla()[fila][columna] == 0:
            self.__bacterias.append((bacteria, fila, columna))
            self.__ambiente.set_grilla_valor(fila, columna, 1)

    def paso(self):
        """
        Ejecuta un paso de simulación: alimentar, aplicar ambiente, dividir, morir, difundir.
        """
        nuevas_bacterias = []
        matriz_consumo = [[0 for _ in range(self.__columnas)] for _ in range(self.__filas)]

        for b in self.__bacterias:
            bacteria, i, j = b

            if not bacteria.esta_vivo():
                continue

            # Alimentar con cantidad aleatoria
            cantidad = random.randint(15, 25)
            bacteria.alimentar(cantidad)
            matriz_consumo[i][j] = cantidad

            # Aplicar antibiótico si corresponde
            self.__ambiente.aplicar_ambiente(i, j, bacteria)

            # Si muere, marcar en la grilla
            if not bacteria.esta_vivo():
                self.__ambiente.set_grilla_valor(i, j, 2)
                continue

            # Intentar dividir
            if bacteria.get_energia() >= 80:
                hija = bacteria.dividirse()
                if hija is not None:
                    # Vecinos cardinales simples
                    if i > 0 and self.__ambiente.get_grilla()[i-1][j] == 0:
                        self.__ambiente.set_grilla_valor(i-1, j, 1)
                        nuevas_bacterias.append((hija, i-1, j))
                    elif i < self.__filas - 1 and self.__ambiente.get_grilla()[i+1][j] == 0:
                        self.__ambiente.set_grilla_valor(i+1, j, 1)
                        nuevas_bacterias.append((hija, i+1, j))
                    elif j > 0 and self.__ambiente.get_grilla()[i][j-1] == 0:
                        self.__ambiente.set_grilla_valor(i, j-1, 1)
                        nuevas_bacterias.append((hija, i, j-1))
                    elif j < self.__columnas - 1 and self.__ambiente.get_grilla()[i][j+1] == 0:
                        self.__ambiente.set_grilla_valor(i, j+1, 1)
                        nuevas_bacterias.append((hija, i, j+1))

        # Actualizar ambiente
        self.__ambiente.actualizar_nutrientes(matriz_consumo)
        self.__ambiente.difundir_nutrientes()

        # Agregar nuevas bacterias
        self.__bacterias.extend(nuevas_bacterias)

    def reporte_estado(self):
        """
        Muestra el estado general de la colonia.
        """
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

    def exportar_csv(self, nombre="colonia_estado.csv"):
        """
        Exporta el estado de las bacterias a un archivo CSV.
        """
        with open(nombre, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Raza", "Energía", "Resistente", "Estado"])
            for b, _, _ in self.__bacterias:
                writer.writerow([
                    b.get_id(),
                    b.get_raza(),
                    b.get_energia(),
                    b.es_resistente(),
                    "Viva" if b.esta_vivo() else "Muerta"
                ])
