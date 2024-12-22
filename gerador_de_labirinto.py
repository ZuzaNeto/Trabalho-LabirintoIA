import pygame
from random import choice
import json

# Definição das dimensões da tela e do tamanho de cada célula (TILE).
RES = WIDTH, HEIGHT = 1200, 900  # Resolução da tela em pixels.
TILE = 50                       # Dimensão de cada célula.
cols, rows = WIDTH // TILE, HEIGHT // TILE  # Número de colunas e linhas da grade.

# Inicialização do Pygame e criação da janela.
pygame.init()
sc = pygame.display.set_mode(RES)  # Configura a janela com as dimensões especificadas.
pygame.display.set_caption('Maze generator')  # Define o título da janela.
clock = pygame.time.Clock()  # Objeto para controlar o FPS.

# Classe que representa cada célula do labirinto.
class Cell:
    def __init__(self, x, y):
        # Coordenadas da célula na grade.
        self.x, self.y = x, y  
        
        # Dicionário para controlar as paredes da célula (True = parede presente).
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # Indica se a célula já foi visitada.
        self.visited = False
    
    def draw_current_cell(self):
        # Desenha a célula atual com uma cor especial.
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#f70067'),
                         (x + 2, y + 2, TILE - 2, TILE - 2))
        
    def draw(self):
        # Desenha a célula e suas paredes.
        x, y = self.x * TILE, self.y * TILE
        
        # Se a célula foi visitada, preenche com uma cor.
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#3eb489'),
                             (x, y, TILE, TILE))
        
        # Desenha as paredes com base no estado do dicionário `walls`.
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x, y), (x + TILE, y), 6)  # Parede superior.
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 6)  # Parede direita.
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x + TILE, y + TILE),
                             (x, y + TILE), 6)  # Parede inferior.
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x, y + TILE), (x, y), 6)  # Parede esquerda.
            
    def check_cell(self, x, y):
        # Verifica se a célula nas coordenadas (x, y) está dentro da grade.
        find_index = lambda x, y: x + y * cols  # Calcula o índice da célula no array 1D.
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False  # Retorna False se a célula estiver fora dos limites.
        return grid_cells[find_index(x, y)]  # Retorna a célula correspondente.

    def check_neighbors(self):
        # Verifica os vizinhos não visitados da célula atual.
        neighbors = []
        
        # Obtém as células vizinhas nas direções (topo, direita, baixo, esquerda).
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        
        # Adiciona vizinhos não visitados à lista.
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
    if dx == 1:  # Próxima célula está à esquerda.
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:  # Próxima célula está à direita.
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y  # Diferença nas coordenadas y.
    if dy == 1:  # Próxima célula está acima.
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:  # Próxima célula está abaixo.
        current.walls['bottom'] = False
        next.walls['top'] = False 

# Função para reiniciar o estado do jogo.
def reset_game_state():
    global grid_cells, current_cell, stack, colors, color, maze_array
    # Recria todas as células e redefine os estados iniciais.
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]  # Define a célula inicial.
    stack = []  # Pilha para backtracking.
    colors, color = [], 40  # Reseta a trilha de cores.

# Inicializa o estado do jogo.
reset_game_state()

# Loop principal do programa.
while True:
    sc.fill(pygame.Color('#a6d5e2'))  # Preenche o fundo da tela com uma cor.

    # Verifica eventos do Pygame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fecha o programa ao clicar no "X".
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game_state()  # Reinicia o jogo ao pressionar a barra de espaço.

    # Desenha todas as células e destaca a célula atual.
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    # Desenha a trilha do caminho percorrido.
    [pygame.draw.rect(sc, colors[i], 
                      (cell.x * TILE + 2, cell.y * TILE + 2,
                       TILE - 1, TILE - 1), border_radius=8) for i,
                       cell in enumerate(stack)] 
    
    # Verifica e seleciona o próximo vizinho.
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)  # Adiciona a célula atual à pilha.
        colors.append((min(color, 255), 0, 103))  # Atualiza a cor da trilha.
        color += 1
        remove_walls(current_cell, next_cell)  # Remove paredes entre as células.
        current_cell = next_cell  # Avança para a próxima célula.
    elif stack: 
        current_cell = stack.pop()  # Retrocede para a célula anterior.

    # Gera um array com os dados do labirinto e salva em um arquivo JSON.
    maze_array = [{'x': cell.x, 'y': cell.y, 'walls': cell.walls} for cell in grid_cells]
    file_path = 'walls_data.json'
    with open(file_path, 'w') as json_file:
        json.dump(maze_array, json_file)  # Salva os dados do labirinto.

    pygame.display.flip()  # Atualiza a tela.
    clock.tick()  # Controla a taxa de atualização (FPS).
