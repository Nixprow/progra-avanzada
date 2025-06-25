import numpy as np
import random

class Ambiente():
    #Se definen atributos del ambiente
    def __init__(self, filas=10, columnas=10):
        self.__filas = filas
        self.__columnas = columnas
        self.__nutrientes = np.random.randint(15,30, size=(filas,columnas))
        self.__antibiotico = np.zeros((filas,columnas), dtype=bool) #Dtype siendo un booleano, devuelve el tipo de datos de los elementos de la matriz, y siendo "False=No hay antibiotico"
        self.__factor_ambiental = "normal" #Es algo temporal, ya que despues se puede cambiar
        
    def get_nutrientes(self):
        return self.__nutrientes.copy() #El .copy() se encarga de crear una copia independiente del arreglo numpy, con fin de mantener encapsulamiento
    
    def set_nutrientes(self,x,y,cantidad):
        if isinstance(cantidad,int) and cantidad >= 0: # Se verifica que la cantidad de nutrientes disponibles en el ambiente y que la cantidad tiene que ser mayor que 0
            self.__nutrientes[x,y] = cantidad # Se trabaja con el [x,y], ya que actualmente se está trabajando con una array o matriz
        else:
            raise ValueError("La cantidad debe ser un entero positivo")
        
        
    def get_antibiotico(self):
        return self.__antibiotico.copy()
    
    def get_dimensiones(self):
        return (self.__filas, self.__columnas) #Getter con el fin de facilitar el uso de las dimensiones de la matriz
    
    def hay_antibiotico_en(self, x,y): #  El "en" alfinal de los getters sirven para distinguir la cantidad disponible de antibiotico en el ambiente
        return self.__antibiotico[x,y]
    
    def nutrientes_en (self,x,y): #  El "en" alfinal de los getters sirven para distinguir la cantidad disponible de nutrientes en el ambiente
        return self.__nutrientes[x,y]
    
    #(Recordatorio: Profesor o Ayudante ignore esto)
    #(Columnas,verticales ,eje y)
    #(Filas, horizontales, eje x)
    def aplicar_antibiotico(self, x,y): #Equivalente a aplicar_ambiente que solicita la guia
        if 0 <= x < self.__filas and 0 <= y < self.__columnas:
            self.__antibiotico [x,y]= True
            
    def eliminar_antibiotico(self, x,y):
        if 0 <= x < self.__filas and 0 <= y < self.__columnas:
            self.__antibiotico [x,y]= False
    
    def difundir_nutrientes(self):
        new= self.__nutrientes.copy()
        for i in range(self.__filas):
            for j in range (self.__columnas):
                vecinos = self.__obtener_vecinos(i,j)
                promedio = sum(self.__nutrientes[x,y] for x,y in vecinos) // len(vecinos)
                new[i,j]= (self.__nutrientes[i,j] + promedio) // 2
        self.__nutrientes= new
        
    def __obtener_vecinos(self,x,y):
        vecinos= [] #Se crea lista vacia para almacenar
        for dx in [-1,0,1]:
            for dy in [-1,0,1]: # Se hace el analisis dentro de la matriz como tal viendo los vecinos 
                if (dx != 0 or dy != 0): # Se busca que el valor de la posicion sea distinto del que se está analizando ej: distinto de [1,1]
                    nx= x + dx
                    ny = y + dy
                if 0<= nx < self.__filas and 0<= ny < self.__columnas:
                    vecinos.append ((nx,ny))
        return vecinos
    
    def consumir_nutrientes(self,x,y):
        if 0<= x < self.__filas and 0<= y < self.__columnas:
            cantidad = random.randint(15,25)
            disponible = self.__nutrientes[x,y]
            consumido = min(disponible, cantidad) #Busca la cantidad minima entre cantidad y disponible, ya que min() busca la cantidad minima de una lista o tupla
            self.__nutrientes[x,y] -= consumido
            return consumido
        return 0
    
    
    def mostrar_nutrientes(self):
        print("Matriz de nutrientes: \n", self.__nutrientes) #Muestra la matriz asociada a los nutrientes en el ambiente
    
    def mostrar_antibiotico(self):
        print("Matriz de antibioticos: \n", self.__antibiotico.astype(int)) #Muestra la matriz asociada a los antibioticos del ambiente :D 
        
        
        