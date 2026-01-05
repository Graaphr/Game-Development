# ui/Sidebar.py
import pygame
from Config import ICON_SIZE, ICON_GAP, ANIM_SPEED, ICON_ANIM_SPEED
from Utils.Draw import (
    draw_smooth_circle,
    draw_smooth_round_rect,
    draw_smooth_round_rect_outline
)
from Utils.Hitbox import is_hover_circle

_icon_cache = {}
_tinted_cache = {}

def get_icon(name, size):
    key = (name, size)
    if key not in _icon_cache:
        _icon_cache[key] = pygame.transform.smoothscale(
            Sidebar._raw_icons[name], (size, size)
        )
    return _icon_cache[key]

def get_tinted_icon(name, size):
    key = (name, size)
    if key not in _tinted_cache:
        base = get_icon(name, size).copy()
        base.fill((140, 90, 255), special_flags=pygame.BLEND_RGBA_MULT)
        _tinted_cache[key] = base
    return _tinted_cache[key]


class Sidebar:
    def __init__(self, x, y, icons, order):
        Sidebar._raw_icons = icons
        self.x = x
        self.y = y
        self.icons = icons
        self.order = order

        self.active = 0
        self.circle_y = y + 50
        self.circle_target_y = self.circle_y

        self.scales = [1.0 for _ in order]
        self.targets = [1.0 for _ in order]

    def handle_click(self, pos):
        for i in range(len(self.order)):
            cx = self.x + 40
            cy = self.y + 50 + i * ICON_GAP

            if is_hover_circle(pos, (cx, cy), 26):
                self.active = i
                self.circle_target_y = cy

                import Config
                if i == 1:
                    Config.ui_state = Config.UI_NOTEBOARD
                elif i == 4: 
                    Config.ui_state = Config.UI_SETTINGS
                else:
                    Config.ui_state = Config.UI_HOME


                for j in range(len(self.targets)):
                    self.targets[j] = 1.0

                self.scales[i] = 1.35
                self.targets[i] = 1.2

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, 80, 420)

        draw_smooth_round_rect(
            screen,
            rect,
            (0, 0, 0, 35),
            radius=40
        )

        draw_smooth_round_rect_outline(
            screen,
            rect,
            (255, 255, 255, 180),
            radius=40,
            thickness=2
        )

        self.circle_y += (self.circle_target_y - self.circle_y) * ANIM_SPEED
        draw_smooth_circle(
            screen,
            (255, 255, 255),
            (self.x + 40, int(self.circle_y)),
            50
        )

        for i in range(len(self.scales)):
            self.scales[i] += (self.targets[i] - self.scales[i]) * ICON_ANIM_SPEED

        for i, name in enumerate(self.order):
            cx = self.x + 40
            cy = self.y + 50 + i * ICON_GAP

            size = int(ICON_SIZE * self.scales[i])
            if i == self.active:
                icon = get_tinted_icon(name, size)
            else:
                icon = get_icon(name, size)

            if i == self.active:
                tinted = icon.copy()
                tinted.fill((140, 90, 255), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted, tinted.get_rect(center=(cx, cy)))
            else:
                screen.blit(icon, icon.get_rect(center=(cx, cy)))
