import pygame
import numpy as np

class Game(object):
    
    def __init__(self, ancho_juego, alto_juego):
        pygame.display.set_caption('Snake')
        self.ancho_juego = ancho_juego
        self.alto_juego = alto_juego
        self.display_juego = pygame.display.set_mode((ancho_juego, alto_juego+100))
        self.fondo = pygame.image.load('fondo.png')
        self.fondo = pygame.transform.scale(self.fondo, (ancho_juego, alto_juego))
        self.collision = False
        self.score = 0
        self.font = pygame.font.SysFont('Ubuntu',  20)
        
    def display_ui(self, record):
        self.display_juego.fill((255, 255, 255))
        pygame.draw.rect(self.display_juego, (200, 200, 200), (0, self.alto_juego, self.ancho_juego, 100))
        self.display_juego.blit(self.fondo, (0, 0))

        score_txt = self.font.render('RESULTADO: ', True, (0, 0, 0))
        score_num = self.font.render(str(self.score), True, (0, 0, 0))
        record_txt = self.font.render('MEJOR: ', True, (0, 0, 0))
        record_num = self.font.render(str(record), True, (0, 0, 0))
        
        self.display_juego.blit(score_txt, (45, self.alto_juego + 30))
        self.display_juego.blit(score_num, (170, self.alto_juego + 30))
        self.display_juego.blit(record_txt, (270, self.alto_juego + 30))
        self.display_juego.blit(record_num, (350, self.alto_juego + 30))

    def obtener_record(self, score, record):
        return max(score, record)
    
class Player(object):
    
    def __init__(self):
        self.x = 100
        self.y = 100
        self.position = [[self.x, self.y]]
        self.n_manzanas = 1
        self.comida = False
        self.imagen = pygame.image.load('cuerpo_serpiente.png')
        self.imagen = pygame.transform.scale(self.imagen, (20, 20))
        self.cambio_x = 20
        self.cambio_y = 0
        self.direccion = [20, 0]

    def cambiar_direccion(self, nueva_direccion):
        if (self.direccion[0] + nueva_direccion[0] == 0 and
            self.direccion[1] + nueva_direccion[1] == 0):
            return
        self.direccion = nueva_direccion

    def refrescar_position(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.n_manzanas > 1:
                for i in range(self.n_manzanas - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
                    
            self.position[-1][0] = x
            self.position[-1][1] = y
            
    def hacer_movimiento(self, game, food):
        if self.comida:
            self.position.append([self.x, self.y])
            self.comida = False
            self.n_manzanas += 1

        self.cambio_x, self.cambio_y = self.direccion
        self.x += self.cambio_x
        self.y += self.cambio_y

        if self.x < 0 or self.x > game.ancho_juego - 20 \
                or self.y < 0 or self.y > game.alto_juego - 20 \
                or [self.x, self.y] in self.position:
            game.collision = True

        food.comer(self, game)
        self.refrescar_position(self.x, self.y)
        
    def display_jugador(self, x, y, game):
        self.position[-1][0] = x
        self.position[-1][1] = y
        
        if not game.collision:
            for i in range(self.n_manzanas):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.display_juego.blit(self.imagen, (x_temp, y_temp))
                
class Food(object):
    
    def __init__(self):
        self.x_food = 200
        self.y_food = 200
        self.imagen = pygame.image.load('comida.png')
        self.imagen = pygame.transform.scale(self.imagen, (20, 20))
        
    def comida_coor(self, game, player):
        x_rand = np.random.choice(list(range(0, game.ancho_juego, 20)))
        self.x_food = x_rand
        y_rand = np.random.choice(list(range(0, game.alto_juego, 20)))
        self.y_food = y_rand
        
    def display_comida(self, x, y, game):
        game.display_juego.blit(self.imagen, (x, y))
        
    def comer(self, player, game):
        if player.x == self.x_food and player.y == self.y_food:
            self.comida_coor(game, player)
            player.comida = True
            game.score += 1
        

    
def run():
    pygame.init()
    record = 0
    clock = pygame.time.Clock()

    game = Game(420, 420)
    player = Player()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.cambiar_direccion([-20, 0])
                elif event.key == pygame.K_RIGHT:
                    player.cambiar_direccion([20, 0])
                elif event.key == pygame.K_UP:
                    player.cambiar_direccion([0, -20])
                elif event.key == pygame.K_DOWN:
                    player.cambiar_direccion([0, 20])

        if not game.collision:
            player.hacer_movimiento(game, food)

        record = game.obtener_record(game.score, record)
        game.display_ui(record)
        player.display_jugador(player.x, player.y, game)
        food.display_comida(food.x_food, food.y_food, game)

        pygame.display.update()
        clock.tick(7)
    
if __name__ == '__main__':
    run()