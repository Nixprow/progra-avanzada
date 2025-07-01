import random

class Ambiente:
    def __init__(self, filas=10, columnas=10, nutrientes_iniciales=60, prob_antibiotico=0.1):
        self.__filas = filas
        self.__columnas = columnas

        # Grilla teniendo en consideracion que 0 = vacío, 1 = activa, 2 muerta, 3 = resistente, 4 = biofilm 
        self.__grilla = [[0 for _ in range(columnas)] for _ in range(filas)]

        # Nutrientes distribuidas en la grilla
        self.__nutrientes = [[nutrientes_iniciales for _ in range(columnas)] for _ in range(filas)]

        # Antibióticos (True si hay antibiótico en la casilla o coordenada(?))
        self.__factor_ambiental = [[random.random() < prob_antibiotico for _ in range(columnas)] for _ in range(filas)]

    # -Métodos
    def get_grilla(self):
        return self.__grilla
    
    #La variable valor equivale al numero asignado segun el estado de la bacteria misma
    def set_grilla_valor(self, x, y, valor):
        if 0 <= x < self.__filas and 0 <= y < self.__columnas:
            self.__grilla[x][y] = valor

    # -Nutrientes
    def get_nutrientes(self):
        return self.__nutrientes

    def actualizar_nutrientes(self, matriz_consumo):
        
        #Descuenta los nutrientes según el consumo por celda.
        
        for x in range(self.__filas):
            for y in range(self.__columnas):
                consumo = matriz_consumo[x][y]
                if isinstance(consumo, int) and consumo > 0:
                    self.__nutrientes[x][y] = max(0, self.__nutrientes[x][y] - consumo)

    def difundir_nutrientes(self):
        
        #Difunde los nutrientes con vecinos directos (arriba, abajo, izquierda, derecha).
        #Se asigna una nueva variable con la finalidad de luego sobreescribirla en la cantidad originalmente asignada de nutrientes
        nueva = [[0 for _ in range(self.__columnas)] for _ in range(self.__filas)]
        
        for x in range(self.__filas):
            for y in range(self.__columnas):
                suma = self.__nutrientes[x][y]
                contador = 1

                if x > 0:
                    suma += self.__nutrientes[x-1][y]
                    contador += 1
                if x < self.__filas - 1:
                    suma += self.__nutrientes[x+1][y]
                    contador += 1
                if y > 0:
                    suma += self.__nutrientes[x][y-1]
                    contador += 1
                if y < self.__columnas - 1:
                    suma += self.__nutrientes[x][y+1]
                    contador += 1

                nueva[x][y] = suma // contador

        self.__nutrientes = nueva

    # -Antibióticos
    def get_factor_ambiental(self):
        return self.__factor_ambiental

    def aplicar_ambiente(self, x, y, bacteria):
        
        #Aplica el efecto del antibiótico si la bacteria no es resistente (gracias a un random).
        
        if self.__factor_ambiental[x][y]:
            if not bacteria.es_resistente():
                if random.random() > 0.15:
                    bacteria.morir()
                else:
                    print(f"{bacteria.get_id()} sobrevivió al antibiótico en ({x}, {y})")
