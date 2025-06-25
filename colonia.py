from bacteria import Bacteria
from ambiente import Ambiente
import random

class Colonia():
    def __init__(self,ambiente):
        self.__bacterias= [] #Lista de objetos
        self.__ambiente= None #Considera la instancia de ambiente
        self.__posiciones_bacterias= {}
    def get_ambiente(self):
        return self.__ambiente
    
    def set_ambiente(self,ambiente):
        if isinstance(ambiente, Ambiente):
            self.__ambiente= ambiente
        else: 
            raise TypeError("El tipo no corresponde a la instancia Ambiente")
        
    
    def agregar_bacteria(self,bacteria=Bacteria(),ambiente= Ambiente(), x=None, y=None):
        if x is None or y is None:
            x=random.randint(0,ambiente.get_dimensiones()[0]- 1)
            y=random.randint(0,ambiente.get_dimensiones()[1]- 1)
        if not self.celda_ocupada(x,y):
            self.__bacterias.append(bacteria)
            self.__posiciones_bacterias[bacteria.get_id()] =(x,y)
            
    def celda_ocupada(self,x,y):
        return (x,y) in self.__posiciones_bacterias.values()
    
    def paso(self):
        nuevas_bacterias= [] #Variable para almacenar las bacterias nuevas
            
            