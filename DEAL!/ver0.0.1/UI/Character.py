import pygame

_char_cache = {}

def get_character_sprite(img, size):
    key = (img, size)

    if key not in _char_cache:
        _char_cache[key] = pygame.transform.smoothscale(img, (size, size))

    return _char_cache[key]

def draw_character(surface, img, center, size):
    sprite = get_character_sprite(img, size)
    surface.blit(sprite, sprite.get_rect(center=center))
