import pygame, Config
from Utils.Draw import draw_smooth_round_rect, draw_text, draw_smooth_round_rect_outline
from Utils.SettingsStore import load_settings, save_settings

PANEL_W = 520
PANEL_H = 700

TITLE_CLR = (255,255,255)
SECTION_CLR = (220,220,255)
TEXT_CLR = (185,185,220)
DIV_CLR = (255,255,255)

PAD_X = 30
LINE_W = PANEL_W - 60
ROW_H = 36
SEC_GAP = 28

DIV_GAP = 16
SEC_TOP = 22



def draw_divider(surf, x, y):
    pygame.draw.line(surf, DIV_CLR, (x, y), (x + LINE_W, y), 1)

def draw_section(surf, title, items, font, x, y):
    draw_text(surf, title, font, SECTION_CLR, x, y)
    y += SEC_GAP
    for t in items:
        draw_text(surf, t, font, TEXT_CLR, x, y)
        y += ROW_H
    return y


class SettingsPanel:
    def __init__(self, fonts):
        self.font_title = fonts["settings_title"]
        self.font_subtitle = fonts["settings_subtitle"]
        self.font_small = fonts["settings_small"]
        self.anim = 0
        self.rect = pygame.Rect(0, 0, PANEL_W, PANEL_H)
        cfg = load_settings()
        self.bgm_on = cfg.get("bgm_on", True)
        
        self.cached_surface = None
        self.cached_dirty = True
        
        self.credits_scroll = 0
        self.credits_cache = None
        self.credits_h = 0
        self.credits_view_h = 0
        self.credits_top = 0
        self.credits_max = 0




    def toggle_bgm(self):
        self.bgm_on = not self.bgm_on

        if self.bgm_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        save_settings({"bgm_on": self.bgm_on})
        self.cached_dirty = True


            
    def update(self, dt):
        if Config.ui_state == Config.UI_SETTINGS:
            self.anim = min(self.anim + dt * 5, 1)
        else:
            self.anim = max(self.anim - dt * 5, 0)


    def handle(self, e):
        if self.anim < 0.95: return
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = e.pos
            lx = mx - self.rect.x
            ly = my - self.rect.y

            if self.toggle_rect.collidepoint(lx, ly):
                self.toggle_bgm()
                
        if e.type == pygame.MOUSEWHEEL:
            self.credits_scroll -= e.y * 24
            self.credits_scroll = max(0, min(self.credits_scroll, self.credits_max))


                
    def build_cache(self):
        base = pygame.Surface((PANEL_W, PANEL_H), pygame.SRCALPHA)
        panel_rect = pygame.Rect(0,0,PANEL_W,PANEL_H)

        draw_smooth_round_rect(base, panel_rect, (48,32,96), 26)
        draw_smooth_round_rect_outline(base, panel_rect, (255,255,255), 26, 4)

        cx = PAD_X
        y = 26

        # TITLE
        draw_text(base,"SETTINGS", self.font_title, TITLE_CLR, cx, y)
        y += 44
        draw_divider(base, cx, y)
        y += DIV_GAP+SEC_TOP

        # AUDIO
        y = draw_section(base, "AUDIO", ["Background Music"], self.font_small, cx, y)

        self.toggle_rect = pygame.Rect(PANEL_W-80, y-ROW_H-10, 50, 30)

        y += DIV_GAP
        draw_divider(base, cx, y)
        y += DIV_GAP+SEC_TOP

        # VERSION
        version_h = 90
        version_y = PANEL_H - version_h
        draw_divider(base, cx, version_y-16)
        draw_section(base, "VERSION", ["DEAL v1.0.0"], self.font_subtitle, cx, version_y)

        # CREDITS (SCROLLABLE)
        self.credits_top = y
        self.credits_view_h = (version_y-16) - y

        credits_surf = pygame.Surface((LINE_W, 2000), pygame.SRCALPHA)
        cy = 0
        cy = draw_section(credits_surf, "CREDITS", [], self.font_title, 0, cy)
        cy += DIV_GAP
        cy = draw_section(credits_surf, "DESIGN",
            ["Terra Faqih satria Madjid","Alya Ghaitsa Salsabila","Bella Fadhilla K.E.","Rivo Nyawan Situmorang","Rizky Eko Pratama", "Hasanun Nisa"],
            self.font_small, 0, cy)
        cy += DIV_GAP
        cy = draw_section(credits_surf, "CODE", ["Terra Faqih satria Madjid"], self.font_small, 0, cy)
        cy += DIV_GAP
        cy = draw_section(credits_surf, "MUSIC", ["PIXABAY Free Music Library"], self.font_small, 0, cy)

        self.credits_cache = credits_surf.subsurface((0,0,LINE_W,cy))
        self.credits_h = cy
        self.credits_scroll = 0
        self.credits_max = max(0, cy - self.credits_view_h)

        self.base_cache = base
        self.cached_dirty = False

    def draw(self, surf):
        if self.anim <= 0: return
        if self.cached_dirty or not hasattr(self, "base_cache"):
            self.build_cache()

        ease = 1 - (1 - self.anim) ** 3
        x = surf.get_width() - PANEL_W * ease
        y = surf.get_height()//2 - PANEL_H//2
        self.rect.topleft = (x, y)

        surf.blit(self.base_cache, (x, y))

        # ===== draw credits scroll =====
        view = pygame.Rect(0, self.credits_scroll, LINE_W, self.credits_view_h)
        surf.blit(self.credits_cache, (x+PAD_X, y+self.credits_top), view)


        # ===== draw toggle realtime =====
        tx = x + self.toggle_rect.x
        ty = y + self.toggle_rect.y
        abs_toggle = pygame.Rect(tx, ty, 50, 30)

        draw_smooth_round_rect(surf, abs_toggle,
            (120,90,220) if self.bgm_on else (70,70,90), 20)

        knob_x = abs_toggle.right-25 if self.bgm_on else abs_toggle.left+5
        knob = pygame.Rect(knob_x, abs_toggle.centery-10, 20, 20)
        draw_smooth_round_rect(surf, knob, (255,255,255), 15)









