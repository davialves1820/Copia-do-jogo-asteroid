import pygame
from src.utils import load_sprite, get_random_position, print_text
from src.models import Spaceship, Asteroid

class Game:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""   
        self.bullets = []
        self.spaceship = Spaceship((400,300), self.bullets.append)
        
        self.asteroids = []
        # Gera posições aletórias que cumpram a regra do distanciamento minimo
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    # Loop do jogo
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    # Inicialização do pygame
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Game")

    # Manipulação dos dados de entrada
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spaceship.shoot()
        
        is_key_pressed = pygame.key.get_pressed()

        # Verifica se a nave está viva
        if self.spaceship:
            # Faz a rotação da nave
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            
            # Acelera a nave
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            
            # Desacelera a nave gradualmente
            self.spaceship.decelerate()

    # Lógica do jogo
    def _process_game_logic(self,):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        # Verifica se a nave foi atingida
        if self.spaceship:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(self.spaceship):
                    self.message = "Game Over!"
                    self.spaceship = None
                    break

        
        # Destroi os asteroides atingidos
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        # Remove as balas que sairam da tela
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        if not self.asteroids and self.spaceship:
            self.message = "You won!"


    # Desenho
    def _draw(self):
        self.screen.blit(self.background, (0,0))
        
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    # Retorna os objetos do jogo
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
    