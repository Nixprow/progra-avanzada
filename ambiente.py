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
        return self.__nutrientes
    
    def set_nutrientes(self,x,y,cantidad):
        if isinstance(cantidad,int) and cantidad >= 0: # Se verifica que la cantidad de nutrientes disponibles en el ambiente y que la cantidad tiene que ser mayor que 0
            self.__nutrientes[x,y] = cantidad # Se trabaja con el [x,y], ya que actualmente se está trabajando con una array o matriz
        else:
            raise ValueError("La cantidad debe ser un entero positivo")
        
        
    def get_antibiotico(self):
        return self.__antibiotico
    
    def get_dimensiones(self):
        return (self.__filas, self.__columnas)
    
    def hay_antibiotico(self, x,y):
        return self.__antibiotico[x,y]
    
    def nutrientes_en (self,x,y):
        return self.__nutrientes[x,y]
            