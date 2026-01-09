import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

def grid_para_matriz(model):
    largura = model.grid.width
    altura = model.grid.height

    matriz = np.zeros((altura, largura))

    for agents, (x, y) in model.grid.coord_iter():
        if agents:
            agente = agents[0]
            matriz[y, x] = agente.agua_acumulada

    return matriz

def plotar_grid(model):
    matriz = grid_para_matriz(model)

    plt.figure(figsize=(6, 6))
    plt.imshow(matriz, cmap="Blues", origin="lower")
    plt.colorbar(label="Água acumulada")
    plt.title("Simulação de Inundação")
    plt.show()
