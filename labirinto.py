import pygame 
from random import choice

# Definição da resolução da janela e do tamanho de cada célula (TILE).
RES = WIDTH, HEIGHT = 1200, 900  # Dimensão da janela em pixels.
TILE = 50                       # Tamanho de cada célula em pixels.
cols, rows = WIDTH // TILE, HEIGHT // TILE  # Número de colunas e linhas na grade.

# Inicialização do módulo Pygame e configuração da tela e do relógio.
pygame.init()
sc = pygame.display.set_mode(RES)  # Cria uma janela com a resolução especificada.
clock = pygame.time.Clock()        # Relógio para controlar os frames por segundo.

# Classe que representa cada célula do labirinto.
class Cell:
    def __init__(self, x, y):
        # Coordenadas da célula na grade.
        self.x, self.y = x, y  
        
        # Dicionário para armazenar o estado das paredes (True = presente, False = removida).
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # Indicador de visitação: se a célula já foi visitada no algoritmo.
        self.visited = False
    
    def draw_current_cell(self):
        # Desenha a célula atual (em destaque) com uma cor diferenciada.
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#f70067'),
                         (x + 2, y + 2, TILE - 2, TILE - 2))
    
    def draw(self):
        # Desenha a célula e suas paredes.
        x, y = self.x * TILE, self.y * TILE
        
        # Preenche a célula se ela foi visitada.
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e1e1e'),
                             (x, y, TILE, TILE))
        
        # Desenha as paredes da célula com base no estado do dicionário `walls`.
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x, y), (x + TILE, y), 3)  # Parede superior.
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 3)  # Parede direita.
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 3)  # Parede inferior.
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x, y + TILE), (x, y), 3)  # Parede esquerda.
            
    def check_cell(self, x, y):
        # Verifica se a célula nas coordenadas (x, y) está dentro da grade.
        find_index = lambda x, y: x + y * cols  # Fórmula para encontrar o índice no array 1D.
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False  # Retorna False se a célula estiver fora dos limites.
        return grid_cells[find_index(x, y)]  # Retorna a célula correspondente no array.

    def check_neighbors(self):
        # Verifica os vizinhos não visitados da célula atual.
        neighbors = []
        
        # Obtém os vizinhos nas direções (topo, direita, baixo, esquerda).
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        
        # Adiciona os vizinhos não visitados à lista.
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        
        # Retorna um vizinho aleatório ou False se não houver vizinhos disponíveis.
        return choice(neighbors) if neighbors else False   
    
# Função para remover paredes entre duas células adjacentes.
def remove_walls(current, next):
    dx = current.x - next.x  # Diferença nas coordenadas x.
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y  # Diferença nas coordenadas y.
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False 

# Criação de todas as células na grade como objetos `Cell`.
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

# Define a célula inicial e inicializa a pilha para backtracking.
current_cell = grid_cells[0]
stack = []

# Lista de cores para a trilha e valor inicial da cor.
colors, color = [], 40

# Loop principal do programa.
while True:
    sc.fill(pygame.Color('#a6d5e2'))  # Preenche o fundo com uma cor padrão.
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fecha o programa se o evento de saída for acionado.
            exit()
            
    [cell.draw() for cell in grid_cells]  # Desenha todas as células.
    current_cell.visited = True  # Marca a célula atual como visitada.
    current_cell.draw_current_cell()  # Destaca a célula atual.
    
    # Desenha as células na pilha (trilha do caminho percorrido).
    [pygame.draw.rect(sc, colors[i], 
                      (cell.x * TILE + 2, cell.y * TILE + 2,
                       TILE - 4, TILE - 4), border_radius=8) for i,
                       cell in enumerate(stack)] 
    
    # Verifica e seleciona o próximo vizinho.
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True  # Marca o próximo vizinho como visitado.
        stack.append(current_cell)  # Adiciona a célula atual à pilha.
        colors.append((min(color, 255), 0, 103))  # Define a cor para a trilha.
        color += 1  # Incrementa a tonalidade da cor.
        remove_walls(current_cell, next_cell)  # Remove as paredes entre as células.
        current_cell = next_cell  # Move para a próxima célula.
    elif stack: 
        current_cell = stack.pop()  # Volta para a célula anterior na pilha.
        
    pygame.display.flip()  # Atualiza a tela.
    clock.tick(30)  # Limita o FPS a 30.
