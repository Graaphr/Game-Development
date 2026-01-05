import pygame, random

class SplashScreen:
    def __init__(self, screen, assets):
        self.screen = screen
        self.w, self.h = screen.get_size()

        ouro_raw, deal_raw = assets

        logo_w = int(self.w * 0.55)
        scale = logo_w / ouro_raw.get_width()
        self.ouro_logo = pygame.transform.smoothscale(
            ouro_raw,
            (logo_w, int(ouro_raw.get_height() * scale))
        )

        deal_w = int(self.w * 0.45)
        scale2 = deal_w / deal_raw.get_width()
        self.deal_logo = pygame.transform.smoothscale(
            deal_raw,
            (deal_w, int(deal_raw.get_height() * scale2))
        )

        self.timer = 0
        self.phase = 0
        self.alpha = 0
        self.fade_black = 0


    def draw_center(self, surf, alpha):
        surf = surf.copy()
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(self.w//2, self.h//2))
        self.screen.blit(surf, rect)


    def update(self, dt):
        self.timer += dt

        if self.phase == 0:
            self.alpha = min(255, self.alpha + 220*dt)
            if self.timer > 2:
                self.phase = 1
                self.timer = 0

        elif self.phase == 1:
            if self.timer > 1.2:
                self.phase = 2
                self.timer = 0

        elif self.phase == 2:
            self.alpha = max(0, self.alpha - 220*dt)
            if self.alpha <= 0:
                self.phase = 3
                self.timer = 0
                
        elif self.phase == 3:
            self.alpha = min(255, self.alpha + 240*dt)
            if self.timer > 2:
                self.phase = 4
                self.timer = 0

        elif self.phase == 4:
            self.fade_black = min(255, self.fade_black + 400*dt)
            if self.fade_black >= 255:
                return True

        return False


    def draw(self):
        if self.phase < 3:
            self.screen.fill((0,0,0))
            self.draw_center(self.ouro_logo, self.alpha)

        elif self.phase == 3:
            self.screen.fill((0,0,0))
            self.draw_center(self.deal_logo, self.alpha)

        elif self.phase >= 4:
            self.screen.fill((0,0,0))
            self.draw_center(self.deal_logo, 255)
            fade = pygame.Surface((self.w,self.h))
            fade.set_alpha(self.fade_black)
            fade.fill((0,0,0))
            self.screen.blit(fade,(0,0))
