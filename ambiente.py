import random
#Se crea una clase matrizambiente, la cual otorga las bases para las futuras a matrices con las que se trabajará
class MatrizAmbiente():
    def __init__(self,filas,columnas):
        self._filas = filas
        self._columnas = columnas
    #Se hace una funcion para crear matrices segun el valor asignado    
    def crear_matriz (self,valor):
        
        return[[valor for y in range(self._columnas)] for x in range(self._filas)]
    
    def crear_matriz_func (self,funcion):
        
        return[[funcion() for y in range(self._columnas)] for x in range(self._filas)]
        
        
class Ambiente(MatrizAmbiente):
    def __init__(self, filas=10, columnas=10, nutrientes_iniciales=60, prob_antibiotico=0.1):
        super().__init__(filas, columnas)
        self.__grilla= self.crear_matriz(0)  # Interacción: Usada por Colonia para representar el estado de cada celda
        self.__nutrientes = self.crear_matriz(nutrientes_iniciales)
        self.__factor_ambiental= self.crear_matriz_func(lambda: random.random() < prob_antibiotico)
        
    # -Métodos
    def get_grilla(self):
        # Llamado por Colonia y SimuladorWindow para obtener el estado de la grilla
        return self.__grilla
    
    #La variable valor equivale al numero asignado segun el estado de la bacteria misma
    # 0 Vacia, 1 Viva ,2 Muerta, 3 Resistente
    def set_grilla_valor(self, x, y, valor):
        # Llamado por Colonia para actualizar el estado de la grilla
        if 0 <= x < self._filas and 0 <= y < self._columnas:
            self.__grilla[x][y] = valor

    # -Nutrientes
    def get_nutrientes(self):
        return self.__nutrientes

    def actualizar_nutrientes(self, matriz_consumo):
        #Descuenta los nutrientes según el consumo por celda.
        for x in range(self._filas):
            for y in range(self._columnas):
                consumo = matriz_consumo[x][y]
                if isinstance(consumo, int) and consumo > 0:
                    self.__nutrientes[x][y] = max(0, self.__nutrientes[x][y] - consumo)

    def difundir_nutrientes(self):
        # Difunde los nutrientes con vecinos directos (arriba, abajo, izquierda, derecha).
        # Se asigna una nueva variable con la finalidad de luego sobreescribirla en la cantidad originalmente asignada de nutrientes
        nueva = [[0 for _ in range(self._columnas)] for _ in range(self._filas)]
        for x in range(self._filas):
            for y in range(self._columnas):
                suma = self.__nutrientes[x][y]
                contador = 1
                if x > 0:
                    suma += self.__nutrientes[x-1][y]
                    contador += 1
                if x < self._filas - 1:
                    suma += self.__nutrientes[x+1][y]
                    contador += 1
                if y > 0:
                    suma += self.__nutrientes[x][y-1]
                    contador += 1
                if y < self._columnas - 1:
                    suma += self.__nutrientes[x][y+1]
                    contador += 1
                nueva[x][y] = suma // contador
        self.__nutrientes = nueva

    # -Antibióticos
    def get_factor_ambiental(self):
        return self.__factor_ambiental

    def aplicar_ambiente(self, x, y, bacteria):
        if self.__factor_ambiental[x][y]:
            if not bacteria.es_resistente():
                if random.random() > 0.15:
                    bacteria.morir()
                else:
                    print(f"{bacteria.get_id()} sobrevivió al antibiótico en ({x}, {y})")
