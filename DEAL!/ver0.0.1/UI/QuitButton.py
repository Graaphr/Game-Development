# Quit button
import pygame
from Utils.Draw import draw_smooth_circle
from Utils.Hitbox import is_hover_circle

_btn_cache = {}

def build_quit_surface(radius, icon, bg_color):
    size = (radius*2 + 8, radius*2 + 8)
    surf = pygame.Surface(size, pygame.SRCALPHA)
    center = size[0]//2, size[1]//2

    draw_smooth_circle(surf, (255,255,255), center, radius + 4)
    draw_smooth_circle(surf, bg_color, center, radius)
    surf.blit(icon, icon.get_rect(center=center))
    return surf


def draw_quit_button(screen, mouse_pos, center, radius, icon_white, icon_red):
    hovered = is_hover_circle(mouse_pos, center, radius)

    key = ("hover" if hovered else "normal", radius)

    if key not in _btn_cache:
        if hovered:
            _btn_cache[key] = build_quit_surface(radius, icon_red, (255,255,255))
        else:
            _btn_cache[key] = build_quit_surface(radius, icon_white, (255,50,50))

    surf = _btn_cache[key]
    screen.blit(surf, surf.get_rect(center=center))
    return hovered
