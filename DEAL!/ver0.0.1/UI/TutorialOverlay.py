import pygame
from Utils.Draw import draw_smooth_round_rect, draw_smooth_round_rect_outline

CARD_W = 560
CARD_H = 440

class TutorialOverlay:
    def __init__(self, fonts):
        self.active = False
        self.font_title = fonts["tutorial_title"]
        self.font_desc = fonts["tutorial_description"]
        self.cards = []
        self.index = 0

        self.card_rect = pygame.Rect(0,0,CARD_W,CARD_H)
        self.prev_btn = pygame.Rect(0,0,36,36)
        self.next_btn = pygame.Rect(0,0,36,36)

    def add(self, icon, title, control, desc):
        self.cards.append((icon, title, control, desc))

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.index = 0

    def _draw_dot(self, screen, x, y, alpha):
        s = pygame.Surface((18,18), pygame.SRCALPHA)
        pygame.draw.circle(s, (255,255,255,alpha), (9,9), 7)
        pygame.draw.circle(s, (255,255,255,alpha//3), (9,9), 9, 2)
        screen.blit(s, (x-7, y-7))



    def draw(self, screen):
        if not self.active or not self.cards:
            return

        w, h = screen.get_size()
        self.card_rect.center = (w//2, h//2)

        # Overlay
        dim = pygame.Surface((w,h), pygame.SRCALPHA)
        dim.fill((0,0,0,160))
        screen.blit(dim, (0,0))

        # Card
        icon, title, ctrl, desc = self.cards[self.index]

        draw_smooth_round_rect(screen, self.card_rect, (65,20,80), 36)
        draw_smooth_round_rect_outline(screen, self.card_rect, (255,255,255), 36, 4)

        title_surf = self.font_title.render(title, True, (255,230,200))
        ctrl_surf  = self.font_desc.render("[" + ctrl + "]", True, (255,215,140))
        desc_surf  = self.font_desc.render(desc, True, (235,225,255))

        cx = self.card_rect.centerx
        y  = self.card_rect.y + 48

        # Title (TOP)
        screen.blit(title_surf, title_surf.get_rect(center=(cx, y)))
        y += title_surf.get_height() + 14

        # Icon
        if icon:
            max_w = self.card_rect.width - 80
            max_h = 230


            iw, ih = icon.get_size()
            scale = min(max_w/iw, max_h/ih, 1)

            icon = pygame.transform.smoothscale(icon, (int(iw*scale), int(ih*scale)))
            screen.blit(icon, icon.get_rect(center=(cx, y + max_h//2)))
            y += max_h + 26



        # Control
        screen.blit(ctrl_surf, ctrl_surf.get_rect(center=(cx, y)))
        y += ctrl_surf.get_height() + 8

        # Description
        screen.blit(desc_surf, desc_surf.get_rect(center=(cx, y)))


        # Navigation
        gap = 54
        btn_r = 28

        self.prev_btn.center = (self.card_rect.left - gap, self.card_rect.centery)
        self.next_btn.center = (self.card_rect.right + gap, self.card_rect.centery) 

        draw_smooth_round_rect(screen,
            pygame.Rect(self.prev_btn.centerx-18, self.prev_btn.centery-18, 36, 36),
            (255,255,255), 18)

        draw_smooth_round_rect(screen,
            pygame.Rect(self.next_btn.centerx-18, self.next_btn.centery-18, 36, 36),
            (255,255,255), 18)

        cx, cy = self.prev_btn.center
        pygame.draw.polygon(screen, (80,20,100), [
            (cx+6, cy-8),
            (cx-8, cy),
            (cx+6, cy+8)
        ])

        cx, cy = self.next_btn.center
        pygame.draw.polygon(screen, (80,20,100), [
            (cx-6, cy-8),
            (cx+8, cy),
            (cx-6, cy+8)
        ])



        # Dot
        dots_y = self.card_rect.bottom + 28
        start_x = self.card_rect.centerx - (len(self.cards)-1)*16

        for i in range(len(self.cards)):
            alpha = 255 if i == self.index else 80
            self._draw_dot(screen, start_x + i*32, dots_y, alpha)

            
    def handle(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.prev_btn.collidepoint(event.pos):
                self.index = (self.index - 1) % len(self.cards)
            elif self.next_btn.collidepoint(event.pos):
                self.index = (self.index + 1) % len(self.cards)
