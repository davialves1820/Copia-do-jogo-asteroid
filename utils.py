import random
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color

# Método que carrega uma imagem
def load_sprite(name, with_alpha=True):
    path = f"img/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()
    
# Método que carrega um som
def load_sound(name):
    path = f"sounds/{name}.wav"
    return Sound(path)

# Método que garante que a nave nunca saia da tela
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h) 

# Método que gera uma posição aleatória para o asteroid
def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

# Método que gera o movimento aleatório do asteroid
def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randint(0,360)
    return Vector2(speed, 0).rotate(angle)

# Método que exibe um texto na tela
def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)