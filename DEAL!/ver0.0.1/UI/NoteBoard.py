import pygame, uuid, json, os
from Utils.Draw import draw_smooth_round_rect, draw_smooth_round_rect_outline
from UI.NoteEditorPanel import NOTE_COLORS as COLORS
from UI.TutorialOverlay import TutorialOverlay
from Utils.AppPath import asset_path


SAVE_FILE = "Data/NOTES.json"
NOTE_SIZE = (220, 160)
NOTE_COLOR = (255,240,160)

class StickyNote:
    def __init__(self, pos, text="Double click to edit...", color=NOTE_COLOR, uid=None):
        self.id = uid or str(uuid.uuid4())
        self.rect = pygame.Rect(pos, NOTE_SIZE)
        self.text = text
        self.color = color
        self.grab_offset = (0,0)
        
        self.surface = None
        self.dirty = True
        self.text_surface = None


    def to_dict(self):
        return dict(id=self.id, x=self.rect.x, y=self.rect.y, text=self.text, color=self.color)

    @staticmethod
    def from_dict(d):
        return StickyNote((d["x"], d["y"]), d["text"], tuple(d["color"]), d.get("id"))
    
    def build_surface(self, font):
        w, h = self.rect.size
        surf = pygame.Surface((w+6, h+6), pygame.SRCALPHA)

        body = pygame.Rect(3,3,w,h)
        shadow = pygame.Rect(6,7,w,h)

        draw_smooth_round_rect(surf, shadow, (0,0,0,70), 14)
        draw_smooth_round_rect(surf, body, self.color, 14)
        draw_smooth_round_rect_outline(surf, body, (255,255,255), 14, 4)
        pygame.draw.circle(surf, (200,40,40), (w//2+3, 13), 6)

        self._render_text_block(surf, font, body)
        self.surface = surf.convert_alpha()
        self.dirty = False
        
    def _render_text_block(self, surf, font, body):
        pad = 12
        x = body.x + pad
        y = body.y + 28
        max_w = body.width - pad*2
        max_h = body.height - 40

        lines = self._wrap_lines(font, self.text, max_w)

        for i, line in enumerate(lines):
            if y + font.get_height() > body.y + max_h:
                dots = font.render("...", True, (40,30,20))
                surf.blit(dots, (x, y))
                return

            txt = font.render(line, True, (40,30,20))
            surf.blit(txt, (x, y))
            y += font.get_height() + 2
            
    def _wrap_lines(self, font, text, max_w):
        result = []
        for raw in text.split("\n"):
            words = raw.split(" ")
            line = ""

            for w in words:
                test = line + (" " if line else "") + w
                if font.size(test)[0] <= max_w:
                    line = test
                else:
                    if line:
                        result.append(line)
                    line = w
            if line:
                result.append(line)
        return result
    
class NoteBoard:
    def __init__(self, editor, fonts):
        self.notes = []
        self.editor = editor
        self.dragging = None

        self.last_click_time = 0
        self.last_clicked_note = None
        
        self.last_right_click_time = 0
        self.last_right_clicked_note = None
        
        self.DOUBLE_CLICK_DELAY = 300

        self.board_rect = pygame.Rect(180,20,1160,720)
        self.font = fonts["calendar_day"]

        self.dirty = False
        self.load()
        
        self.board_surface = pygame.Surface(self.board_rect.size, pygame.SRCALPHA)
        draw_smooth_round_rect(self.board_surface, self.board_surface.get_rect(), (47,12,53), 28)
        draw_smooth_round_rect_outline(self.board_surface, self.board_surface.get_rect(), (255,255,255), 28, 4)

        self.info_btn = pygame.Rect(self.board_rect.right-46, self.board_rect.y+16, 32, 32)
        self.tutorial = TutorialOverlay(fonts)

        self.ico_info   = pygame.image.load(asset_path("Icons/info.png")).convert_alpha()
        self.ico_info_white = pygame.image.load(asset_path("Icons/info_white.png")).convert_alpha() 
        
        self.ico_add    = pygame.image.load(asset_path("UI/note_add.png")).convert_alpha()
        self.ico_drag   = pygame.image.load(asset_path("UI/drag.png")).convert_alpha()
        self.ico_color  = pygame.image.load(asset_path("UI/color.png")).convert_alpha()
        self.ico_edit   = pygame.image.load(asset_path("UI/edit.png")).convert_alpha()
        self.ico_save   = pygame.image.load(asset_path("UI/save.png")).convert_alpha()
        self.ico_exit   = pygame.image.load(asset_path("UI/exit.png")).convert_alpha()
        self.ico_delete = pygame.image.load(asset_path("UI/delete.png")).convert_alpha()

        
        self.tutorial.add(self.ico_add,
            "Add Note",
            "LEFT CLICK",
            "Click an empty area on the board")

        self.tutorial.add(self.ico_drag,
            "Move Note",
            "DRAG",
            "Hold left click and drag the note")

        self.tutorial.add(self.ico_color,
            "Change Color",
            "SCROLL",
            "Hover over a note and scroll")

        self.tutorial.add(self.ico_edit,
            "Edit Note",
            "2x LEFT CLICK",
            "Open the note editor")

        self.tutorial.add(self.ico_save,
            "Save Changes",
            "CTRL + S",
            "Save your note content")

        self.tutorial.add(self.ico_exit,
            "Exit Editor",
            "ESC",
            "Close the note editor")

        self.tutorial.add(self.ico_delete,
            "Delete Note",
            "2x RIGHT CLICK",
            "Permanently remove the note")

        
        self.info_hover = False



    # -------------------- DATA --------------------

    def mark_dirty(self):
        self.dirty = True
        
    def cycle_color(self, note):
        try:
            i = COLORS.index(note.color)
            note.color = COLORS[(i + 1) % len(COLORS)]
        except:
            note.color = COLORS[0]

        note.dirty = True
        note.text_surface = None
        self.mark_dirty()

    def create_note(self, pos):
        self.notes.append(StickyNote(pos))
        self.mark_dirty()
    
    


    # -------------------- INPUT --------------------

    
    def handle(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.info_btn.collidepoint(event.pos):
                self.tutorial.toggle()
                return
        
        self.tutorial.handle(event)
        if self.tutorial.active:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.info_hover = self.info_btn.collidepoint(event.pos)

        if self.editor.active:
            return

        # DRAG
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_left_click(event.pos)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._handle_drag(event.pos)

        # OFF DRAG
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._handle_right_click(event.pos)
        




        # SCROLL COLOR
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4,5):
            for n in reversed(self.notes):
                if n.rect.collidepoint(event.pos):
                    self.cycle_color(n)
                    return


    def _handle_left_click(self, pos):
        now = pygame.time.get_ticks()

        for note in reversed(self.notes):
            if note.rect.collidepoint(pos):

                if note == self.last_clicked_note and now - self.last_click_time < self.DOUBLE_CLICK_DELAY:
                    self.editor.open(note)
                    self.last_clicked_note = None
                    return

                self.dragging = note
                note.grab_offset = (note.rect.x-pos[0], note.rect.y-pos[1])
                self.last_clicked_note = note
                self.last_click_time = now
                return

        if self.board_rect.collidepoint(pos):
            self.create_note(pos)


    def _handle_drag(self, pos):
        ox, oy = self.dragging.grab_offset
        nx = max(self.board_rect.left, min(pos[0]+ox, self.board_rect.right - self.dragging.rect.width))
        ny = max(self.board_rect.top,  min(pos[1]+oy, self.board_rect.bottom - self.dragging.rect.height))
        self.dragging.rect.topleft = (nx, ny)
        
    def _handle_right_click(self, pos):
        if self.dragging:
            self.dragging = None
            self.mark_dirty()
            self.last_right_clicked_note = None
            return

        now = pygame.time.get_ticks()

        for note in reversed(self.notes):
            if note.rect.collidepoint(pos):

                # DELETE
                if note == self.last_right_clicked_note and now - self.last_right_click_time < self.DOUBLE_CLICK_DELAY:
                    self.notes.remove(note)
                    self.last_right_clicked_note = None
                    self.mark_dirty()
                    self.save()
                    return

            
                self.last_right_clicked_note = note
                self.last_right_click_time = now
                return




    # -------------------- DRAW --------------------
    
    def draw(self, screen):
        screen.blit(self.board_surface, self.board_rect.topleft)


        for n in self.notes:
            if n.dirty or not n.surface:
                n.build_surface(self.font)

            screen.blit(n.surface, (n.rect.x-3, n.rect.y-3))
            
        ICON_I_SIZE = 36

        ico = self.ico_info_white if self.info_hover else self.ico_info
        screen.blit(pygame.transform.smoothscale(ico, (ICON_I_SIZE, ICON_I_SIZE)),
                    (self.info_btn.centerx-ICON_I_SIZE//2, self.info_btn.centery-ICON_I_SIZE//2))

        self.tutorial.draw(screen)


    # -------------------- SAVE / LOAD --------------------

    def save(self):
        os.makedirs("Data", exist_ok=True)
        with open(SAVE_FILE, "w", encoding="utf8") as f:
            json.dump([n.to_dict() for n in self.notes], f, indent=2)

    def load(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf8") as f:
                for d in json.load(f):
                    self.notes.append(StickyNote.from_dict(d))
        except:
            open(SAVE_FILE, "w").write("[]")
