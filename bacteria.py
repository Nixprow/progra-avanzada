import random

class Bacteria ():
    def __init__ (self):
        self.__id= None #String
        self.__raza= None #String
        self.__energia= 0 #Entero
        self.__resistente= False #Booleano que luego cumplirá con ser true or false
        self.__estado= True #Booleano que determina el estado de vida de la bacteria siendo "True"= vivo y "False" = muerto
    #Funciones para trabajar con el id o "Nombre" de la bacteria
    def get_id(self):
        return self.__id
    
    def set_id(self,id):
        try:
            if isinstance(id,str):
                self.__id=id
            else:
                raise TypeError("El tipo de dato de dato no corresponde a un String")
        except TypeError as e:
            print(f"Error al ingresar la id de la bacteria {e}")
            self.__id= None
    #Funciones para obtener y manejar informacion con respecto a la raza de la bacteria 
    def get_raza(self):
        return self.__raza
    
    def set_raza(self,raza):
        try:
            if isinstance(raza,str):
                self.__raza= raza
            else:
                raise TypeError("El tipo de dato de dato no corresponde a un String")
        except TypeError as e:
            print(f"Error al ingresar la raza de la bacteria {e}")
            self.__raza= None
    #Funciones para obtener y trabajar con la privacidad de los datos con respecto a la cantidad de energia que posee la bacteria
    def get_energia(self):
        return self.__energia
    
    def set_energia (self,energia):
        try:
            if isinstance(energia, int):
                self.__energia = energia
                return True
            else:
                raise TypeError("El tipo de dato no corresponde a Entero")
        except TypeError as e:
            print(f"Error al ingresar la energia de la Bacteria {e}")
            self.__energia= 0
            return False
        
        except ValueError as e:
            print(f"Error al ingresar la energia de la Bacteria {e}")
            self.__energia= 0
            return False
    
    def es_resistente(self):
        return self.__resistente
    
    def set_resistente(self,resistente):
        if isinstance(resistente,bool):
            self.__resistente= resistente
        else:
            raise TypeError("El tipo de dato no corresponde a un booleano")
    
    def esta_vivo(self):
        return self.__estado
    
    def set_estado(self,vivo):
        if isinstance(vivo,bool):
            self.__estado= vivo
        else:
            raise TypeError("El tipo de dato no corresponde a un booleano")
    #Metodos 
    def alimentar(self,cantidad):
        if self.__estado:
            if isinstance(cantidad, int) and cantidad > 0: #Aqui se analiza primero, que cantidad sea entero y luego que la cantidad sea mayor a 0 para alimentar a la bacter
                self.__energia += cantidad
            else: 
                print("Cantidad insuficiente de nutrientes") #En caso de que no sea mayor a 0 arrojará que hay una cantidad insuficiente de nutrientes
    
    
    def dividirse(self):
        if self.__estado and self.__energia >= 80:
            hija=Bacteria()
            hija.set_id(self.__id + "_hija")
            hija.set_raza(self.__raza)
            hija.set_energia(self.__energia // 2)
            hija.set_resistente(self.__resistente)
            hija.set_estado(True)
            self.__energia //= 2   
            
            # Para que tenga un poco más de aletoreidad haremos que exista una probabilidad de que una mitosis nazca una bacteria con mutacion y su prob será de (5%)
            if random.random() < 0.05:
                hija.mutar()
            return hija
        return None #Se retorna a nada por que ya se hizo la division celular 
    def mutar(self):
        if self.__estado:
            self.__resistente = True #Aqui se hace cambio del estado resistente original de la bacteria que se encontraba en falso por True para que la bacteria pueda presentar una resistencia a los antibioticos o tal vez a otros factores
            print(f"{self.__id} mutó y ahora es resistente")
    
    def morir(self):
        if self.__estado:
            self.__estado = False # Se hace cambio de self.estado, pasa de True (vivo) a False (Muerto)
            self.__energia = 0
            print (f"{self.__id} ha muerto :c ") 
    
                
            
                
    