import csv
from bacteria import Bacteria
from ambiente import Ambiente
import random

class Colonia():
    def __init__(self):
        self.__bacterias= [] #Lista de objetos
        self.__ambiente= Ambiente() #Considera la instancia de ambiente 
        self.__posiciones_bacterias= {} #Un diccionario :3
    def get_ambiente(self):
        return self.__ambiente
    
    def set_ambiente(self,ambiente):
        if isinstance(ambiente, Ambiente):
            self.__ambiente= ambiente
        else: 
            raise TypeError("El tipo no corresponde a la instancia Ambiente")
        
    def get_bacterias(self):
        return self.__bacterias.copy()
    
    def set_bacterias(self, lista_bacterias):
        if isinstance(lista_bacterias, list) and all(isinstance(b, Bacteria) for b in lista_bacterias):
            self.__bacterias = lista_bacterias
            self.__posiciones_bacterias = {
                b.get_id(): self.__generar_posicion_valida()
                for b in self.__bacterias
            }
        else:
            raise TypeError("Debe entregar una lista de instancias Bacteria")
        
        
    def agregar_bacteria(self, x=None, y=None):
        filas, columnas = self.get_ambiente().get_dimensiones()
        bacteria= Bacteria()
        if x is None or y is None:
            x=random.randint(0,filas - 1)
            y=random.randint(0,columnas - 1)
        if not self.celda_ocupada(x,y):
            self.__bacterias.append(bacteria)
            self.__posiciones_bacterias[bacteria.get_id()] =(x,y)
            
    def celda_ocupada(self,x,y):
        return (x,y) in self.__posiciones_bacterias.values()
    
    def paso(self):
        nuevas_bacterias = []

        for bacteria in self.__bacterias:
            if not bacteria.esta_vivo():
                continue

            id_b = bacteria.get_id()
            x, y = self.__posiciones_bacterias[id_b]

            # Alimentar
            cantidad = self.__ambiente.consumir_nutrientes(x, y)
            bacteria.alimentar(cantidad)

            # Aplicar antibiótico
            self.__ambiente.aplicar_antibiotico(bacteria, x, y)

            # División
            hija = bacteria.dividirse()
            if hija:
                pos_hija = self.__buscar_espacio_vecino(x, y)
                if pos_hija:
                    nuevas_bacterias.append((hija, pos_hija))

        for hija, (hx, hy) in nuevas_bacterias:
            self.agregar_bacteria(hija, hx, hy)

        # Filtrar bacterias vivas y actualizar posiciones
        self.__bacterias = [b for b in self.__bacterias if b.esta_vivo()]
        self.__posiciones_bacterias = {
            b.get_id(): self.__posiciones_bacterias[b.get_id()]
            for b in self.__bacterias
            if b.get_id() in self.__posiciones_bacterias
        }

    def __buscar_espacio_vecino(self, x, y):
        vecinos = self.__ambiente._Ambiente__obtener_vecinos(x, y)
        random.shuffle(vecinos)
        for nx, ny in vecinos:
            if not self.celda_ocupada(nx, ny):
                return (nx, ny)
        return None

    def reporte_estado(self):
        datos = []
        for b in self.__bacterias:
            datos.append( (
                b.get_id(),
                b.get_energia(),
                "viva" if b.esta_vivo() else "muerta",
                "resistente" if b.es_resistente() else "normal",
                self.__posiciones_bacterias.get(b.get_id(), ("?", "?"))
            ))
        return datos

    def exportar_csv(self, nombre_archivo="estado_colonia.csv"):
        try:
            with open(nombre_archivo, mode='w', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["ID", "Energia", "Estado", "Tipo", "Posicion"])
                for fila in self.reporte_estado():
                    escritor.writerow(fila)
            print(f"✅ Exportado correctamente a {nombre_archivo}")
        except Exception as e:
            print(f"❌ Error al exportar CSV: {e}")
            
            