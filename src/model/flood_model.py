import mesa
import random

class CelulaTerreno(mesa.Agent):
    def __init__(self, model, elevacao, infiltracao):
        super().__init__(model)
        self.elevacao = elevacao # altura do terreno
        self.infiltracao = infiltracao  # taxa de infiltração (entre 0 e 1)
        self.agua_acumulada = 0
        self.estado = "seco"

    def step(self):
        self.agua_acumulada += self.model.precipitacao

        self.agua_acumulada -= self.infiltracao * self.agua_acumulada

        vizinhos = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
        )

        for vizinho in vizinhos:
            altura_self = self.elevacao + self.agua_acumulada
            altura_vizinho = vizinho.elevacao + vizinho.agua_acumulada
            if altura_self > altura_vizinho:
                diferenca = altura_self - altura_vizinho
                fluxo = 0.2 * diferenca # 0.2 é um coeficiente de fluxo arbitrário
                fluxo = min(fluxo, self.agua_acumulada)

                self.agua_acumulada -= fluxo
                vizinho.agua_acumulada += fluxo

        if self.agua_acumulada > 5:
            self.estado = "alagado"
        elif self.agua_acumulada > 1:
            self.estado = "molhado"
        else:
            self.estado = "seco"

class Inundacao(mesa.Model):
    def __init__(self, largura, altura, precipitacao):
        super().__init__()
        self.grid = mesa.space.MultiGrid(largura, altura, torus=False)
        self.precipitacao = precipitacao

        for x in range(largura):
            for y in range(altura):
                elevacao = random.uniform(0, 10)  # altura entre 0 e 10 metros
                infiltracao = random.uniform(0, 1)  # taxa de infiltração entre 0 e 1

                agente = CelulaTerreno(self, elevacao, infiltracao)
                self.grid.place_agent(agente, (x, y))

    def step(self):
        self.agents.shuffle_do("step")
