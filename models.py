from pygame.math import Vector2
from pygame.transform import rotozoom # Responsável por dimensionar e girar imagens
from utils import load_sprite, load_sound, wrap_position, get_random_velocity

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity) # Vetor que descreve para onde a nave espacial se move a cada quadro

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius
    
UP = Vector2(0, -1)

class Spaceship(GameObject):
    MANEUVERABILITY = 3 # Velocidade que a nave gira
    ACCELERATION = 0.2 # Velocidade a nave se move
    BULLET_SPEED = 3 # Velocidade da bala
    MAX_VELOCITY = 4.5 # Velocidade máxima da nave
    DECELERATE = 0.05 # Desaceleração da nave

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP) # Faz uma cópia do vetor UP
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    # Método que faz a rotação da nave
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle) # Rotaciona a imagem por um determinado angulo
    
    # Método para desenhar a nave pós rotação
    def draw(self, surface):
        angle = self.direction.angle_to(UP) # Calcula o angulo pelo qual o vetor precisa ser rotacionado para apontar na mesma direção que o outro vetor.
        rotated_surface = rotozoom(self.sprite, angle, 1.0) # Rotaciona a imagem, ela pega a imagem original, o angulo de rotação e a escala que deve ser aplicada.
        # Recalcula a posição do blit
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position) # Coloca a imagem na tela.

    # Método para acelerar a nave
    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        if self.velocity.length() > self.MAX_VELOCITY:
            self.velocity = self.velocity.normalize() * self.MAX_VELOCITY

    # Método para desacelerar a nave
    def decelerate(self):
        if self.velocity.length() > 0:
            decel_vector = self.velocity.normalize() * self.DECELERATE
            self.velocity -= decel_vector
            if self.velocity.length() < self.DECELERATE:
                self.velocity = Vector2(0, 0)

    # Método que dispara uma bala
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity # Calcula a velocidade da bala
        bullet = Bullet(self.position, bullet_velocity) # Cria a bala
        self.create_bullet_callback(bullet) 
        self.laser_sound.play()

class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback ,size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        # Define o tamanho do asteroide
        size_to_scale = {
            3: 1, # Grande
            2: 0.5, # Médio
            1: 0.25 # Pequeno
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1,3))

    # Método para dividir o asteroid após a colisão
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.position, self.create_asteroid_callback, self.size -1)
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)
    
    # Método para mover o laser
    def move(self, surface):
        self.position = self.position + self.velocity
