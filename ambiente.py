import random

class Ambiente:
    def __init__(self, filas=10, columnas=10, nutrientes_iniciales=50, prob_antibiotico=0.1):
        self.__filas = filas
        self.__columnas = columnas

        # Grilla lógica numérica: 0 = vacío, 1 = activa, 2 = muerta, 3 = resistente, 4 = biofilm
        self.__grilla = [[0 for _ in range(columnas)] for _ in range(filas)]

        # Nutrientes por celda
        self.__nutrientes = [[nutrientes_iniciales for _ in range(columnas)] for _ in range(filas)]

        # Antibióticos (True si hay antibiótico en la celda)
        self.__factor_ambiental = [[random.random() < prob_antibiotico for _ in range(columnas)] for _ in range(filas)]

    # --- Métodos para acceder y modificar la grilla ---
    def get_grilla(self):
        return self.__grilla

    def set_grilla_valor(self, i, j, valor):
        if 0 <= i < self.__filas and 0 <= j < self.__columnas:
            self.__grilla[i][j] = valor

    # --- Nutrientes ---
    def get_nutrientes(self):
        return self.__nutrientes

    def actualizar_nutrientes(self, matriz_consumo):
        """
        Descuenta los nutrientes según el consumo por celda.
        """
        for i in range(self.__filas):
            for j in range(self.__columnas):
                consumo = matriz_consumo[i][j]
                if isinstance(consumo, int) and consumo > 0:
                    self.__nutrientes[i][j] = max(0, self.__nutrientes[i][j] - consumo)

    def difundir_nutrientes(self):
        """
        Difunde los nutrientes con vecinos directos (arriba, abajo, izquierda, derecha).
        """
        nueva = [[0 for _ in range(self.__columnas)] for _ in range(self.__filas)]

        for i in range(self.__filas):
            for j in range(self.__columnas):
                suma = self.__nutrientes[i][j]
                contador = 1

                if i > 0:
                    suma += self.__nutrientes[i-1][j]
                    contador += 1
                if i < self.__filas - 1:
                    suma += self.__nutrientes[i+1][j]
                    contador += 1
                if j > 0:
                    suma += self.__nutrientes[i][j-1]
                    contador += 1
                if j < self.__columnas - 1:
                    suma += self.__nutrientes[i][j+1]
                    contador += 1

                nueva[i][j] = suma // contador

        self.__nutrientes = nueva

    # --- Antibióticos ---
    def get_factor_ambiental(self):
        return self.__factor_ambiental

    def aplicar_ambiente(self, i, j, bacteria):
        """
        Aplica el efecto del antibiótico si la bacteria no es resistente.
        """
        if self.__factor_ambiental[i][j]:
            if not bacteria.es_resistente():
                if random.random() > 0.15:
                    bacteria.morir()
                else:
                    print(f"{bacteria.get_id()} sobrevivió al antibiótico en ({i}, {j})")
