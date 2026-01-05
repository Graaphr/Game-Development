import pygame
from Utils.Draw import draw_smooth_round_rect, draw_smooth_round_rect_outline


NOTE_COLORS = [
    (255,240,160), (255,200,200), (200,230,255),
    (210,255,210), (230,210,255), (255,230,200)
]

class NoteEditorPanel:
    def __init__(self, rect, board, fonts):
        self.rect = pygame.Rect(rect)
        self.board = board

        self.note = None
        self.active = False
        self.text = ""
        self.font = fonts["calendar_day"]

        
        self.overlay = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
        self.overlay.fill((0,0,0,160))
        
        self.text_cache = []
        self.text_dirty = True

    def rebuild_text_cache(self):
        self.text_cache = []
        y = self.rect.y + 20
        for line in self.text.split("\n"):
            self.text_cache.append(self.font.render(line, True, (245,240,220)))


    def open(self, note):
        self.note = note
        self.text = note.text
        self.text_dirty = True
        self.active = True

        
    def close(self, save=True):
        if save and self.note:
            self.note.text = self.text
            self.note.dirty = True
            self.note.text_surface = None
            self.board.mark_dirty()
            self.board.save()
        self.active = False
        self.note = None



    def handle(self, event):
        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:

            # CTRL + S = SAVE
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                if self.note:
                    self.note.text = self.text
                    self.note.dirty = True
                    self.note.text_surface = None
                    self.board.mark_dirty()
                    self.board.save()
                return True

            # ESC = CLOSE TANPA SAVE
            if event.key == pygame.K_ESCAPE:
                self.active = False
                self.note = None
                return True

            # ENTER = BARIS BARU
            if event.key == pygame.K_RETURN:
                self.text += "\n"
                self.text_dirty = True
                return True

            # BACKSPACE
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.text_dirty = True
                return True

            # CHAR INPUT
            if len(event.unicode) == 1:
                self.text += event.unicode
                self.text_dirty = True
                return True

        return False



    def draw(self, screen):
        if not self.active:
            return

        # Overlay
        screen.blit(self.overlay, (0,0))

        # Panel
        draw_smooth_round_rect(screen, self.rect, (40,25,85), 22)
        draw_smooth_round_rect_outline(screen, self.rect, (255,255,255), 22, 4)

        # Text
        if self.text_dirty:
            self.rebuild_text_cache()
            self.text_dirty = False

        y = self.rect.y + 20
        for surf in self.text_cache:
            screen.blit(surf, (self.rect.x+20, y))
            y += 30


        # COLOR PICKER
        x = self.rect.x + 30
        y = self.rect.bottom - 60

        for c in NOTE_COLORS:
            r = pygame.Rect(x, y, 36, 36)
            draw_smooth_round_rect(screen, r, c, 10)
            draw_smooth_round_rect_outline(screen, r, (255,255,255), 10, 4)

            if r.collidepoint(pygame.mouse.get_pos()):
                draw_smooth_round_rect_outline(screen, r, (255,215,120), 10, 4)

                if pygame.mouse.get_pressed()[0] and self.note:
                    self.note.color = c
                    self.note.dirty = True
                    self.note.text_surface = None
                    self.board.mark_dirty()


            x += 46
