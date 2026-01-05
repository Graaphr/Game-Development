from Utils.Hitbox import is_hover_circle
from Utils.Draw import draw_smooth_circle
import pygame, Config

class AddReminderButton:
    def __init__(self, pos, radius, icons):
        self.pos = pos
        self.radius = radius

        size = int(radius * 0.8)

        # Icon cache
        base_plus = pygame.transform.smoothscale(icons["plus"], (size, size))
        self.plus_normal = base_plus
        self.plus_purple = self._recolor(base_plus, (140, 90, 255))
        self.x_icon = pygame.transform.smoothscale(icons["x"], (size, size))

        # Circle cache
        self.border_circle = self._make_circle(radius, (255,255,255))
        self.fill_white    = self._make_circle(radius-4, (255,255,255))
        self.fill_purple   = self._make_circle(radius-4, (140, 90, 255))

    # ===== helpers =====
    def _make_circle(self, r, color):
        surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        draw_smooth_circle(surf, color, (r, r), r)
        return surf

    def _recolor(self, surf, color):
        s = surf.copy()
        arr = pygame.surfarray.pixels3d(s)
        arr[:,:,0] = color[0]
        arr[:,:,1] = color[1]
        arr[:,:,2] = color[2]
        del arr
        return s

    # ===== draw =====
    def draw(self, screen, fonts, mouse_pos):
        hover = is_hover_circle(mouse_pos, self.pos, self.radius)

        is_open = Config.ui_state == Config.UI_ADDING   # 👈 single source of truth

        if is_open:
            fill = self.fill_white
            icon = self.x_icon
        else:
            if hover:
                fill = self.fill_white
                icon = self.plus_purple
            else:
                fill = self.fill_purple
                icon = self.plus_normal

        screen.blit(self.border_circle, self.border_circle.get_rect(center=self.pos))
        screen.blit(fill, fill.get_rect(center=self.pos))
        screen.blit(icon, icon.get_rect(center=self.pos))


    # ===== click =====
    
    def handle_click(self, pos):
        if is_hover_circle(pos, self.pos, self.radius):
            return True
        return False

