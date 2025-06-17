class Bacteria ():
    def __init__ (self):
        self.__id= None #String
        self.__raza= None #String
        self.__energia= 0 #Entero
        self.__resistente= None #Booleano que luego cumplirá con ser true or false
        self.__estado= None #Booleano que determina el estado de vida de la bacteria
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
        
                
            
                
    