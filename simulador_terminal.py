import random
from ambiente import Ambiente
from colonia import Colonia

# Simulación simple por terminal para mostrar el funcionamiento de Ambiente y Colonia

def mostrar_grilla(grilla):
    for fila in grilla:
        print(' '.join(str(c) for c in fila))
    print()

def main():
    print("Simulación de colonia bacteriana (terminal)")
    colonia = Colonia(filas=5, columnas=5)
    # Agregar algunas bacterias
    colonia.agregar_bacteria("Espiroqueta")
    colonia.agregar_bacteria("Estreptococo")
    colonia.agregar_bacteria("Estreptococo")
    colonia.agregar_bacteria("Espiroqueta")
    print("Estado inicial de la grilla:")
    mostrar_grilla(colonia.get_ambiente().get_grilla())
    pasos = 5
    for paso in range(1, pasos+1):
        print(f"--- Paso {paso} ---")
        colonia.paso()
        mostrar_grilla(colonia.get_ambiente().get_grilla())
        vivas, muertas, resistentes = colonia.reporte_estado()
        print(f"Vivas: {vivas} | Muertas: {muertas} | Resistentes: {resistentes}\n")

if __name__ == "__main__":
    main()
