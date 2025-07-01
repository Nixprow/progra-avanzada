from ambiente import Ambiente

def mostrar_matriz(matriz, titulo):
    print(f"\n{titulo}:")
    for fila in matriz:
        print(fila)

# Crear un ambiente 5x5 para facilitar la prueba
amb = Ambiente(filas=5, columnas=5, nutrientes_iniciales=50, prob_antibiotico=0.2)

# Mostrar nutrientes iniciales
mostrar_matriz(amb.get_nutrientes(), "Nutrientes iniciales")

# Crear una matriz de consumo artificial
consumo = [[10 if i == j else 0 for j in range(5)] for i in range(5)]
amb.actualizar_nutrientes(consumo)
mostrar_matriz(amb.get_nutrientes(), "Nutrientes luego de consumo")

# Difundir nutrientes
amb.difundir_nutrientes()
mostrar_matriz(amb.get_nutrientes(), "Nutrientes luego de difusión")

# Mostrar presencia de antibióticos
mostrar_matriz(amb.get_factor_ambiental(), "Mapa de antibióticos (True = presente)")

# Mostrar grilla inicial (vacía, con ceros)
mostrar_matriz(amb.get_grilla(), "Grilla inicial (numérica)")
