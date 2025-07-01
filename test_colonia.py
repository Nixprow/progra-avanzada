from colonia import Colonia
from bacteria import Bacteria
from pprint import pprint  # Para imprimir matrices bonitas

# Crear colonia de tamaño 5x5
colonia = Colonia(filas=5, columnas=5)

# Agregar 3 bacterias aleatorias en posiciones distintas
b1 = Bacteria()
b2 = Bacteria()
b3 = Bacteria()

colonia.agregar_bacteria(b1, 1, 1)
colonia.agregar_bacteria(b2, 2, 2)
colonia.agregar_bacteria(b3, 3, 3)

print("\n Bacterias iniciales:")
for b, _, _ in colonia.get_bacterias():
    print(f"- ID: {b.get_id()}, Raza: {b.get_raza()}, Energía: {b.get_energia()}")

# Simular 5 pasos
for paso in range(5):
    print(f"\n Paso {paso + 1}")
    colonia.paso()
    colonia.reporte_estado()
    print("\nGrilla actual:")
    pprint(colonia.get_ambiente().get_grilla())

# Exportar resultados a CSV
colonia.exportar_csv("colonia_estado.csv")
print("\n Estado final exportado a 'colonia_estado.csv'")
