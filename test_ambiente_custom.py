from ambiente import Ambiente

def test_ambiente_manual():
    print("Test manual de Ambiente:")
    filas, columnas = 4, 4
    ambiente = Ambiente(filas, columnas, nutrientes_iniciales=20, prob_antibiotico=0.5)
    print("Grilla inicial:")
    for fila in ambiente.get_grilla():
        print(fila)
    print("Nutrientes iniciales:")
    for fila in ambiente.get_nutrientes():
        print(fila)
    print("Antibióticos:")
    for fila in ambiente.get_factor_ambiental():
        print(fila)
    # Modificar valores y volver a mostrar
    ambiente.set_grilla_valor(2, 2, 3)
    print("\nGrilla tras set_grilla_valor(2,2,3):")
    for fila in ambiente.get_grilla():
        print(fila)
    # Consumir nutrientes
    matriz_consumo = [[1,2,3,4],[0,0,0,0],[2,2,2,2],[1,1,1,1]]
    ambiente.actualizar_nutrientes(matriz_consumo)
    print("\nNutrientes tras consumo:")
    for fila in ambiente.get_nutrientes():
        print(fila)
    # Difundir nutrientes
    ambiente.difundir_nutrientes()
    print("\nNutrientes tras difusión:")
    for fila in ambiente.get_nutrientes():
        print(fila)

if __name__ == "__main__":
    test_ambiente_manual()
