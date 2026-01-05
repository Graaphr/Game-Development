import pygame, Config
from Utils.ReminderWriter import save_new
from Utils.Draw import draw_text, draw_smooth_round_rect, draw_smooth_round_rect_outline
from datetime import datetime
from UI.TutorialOverlay import TutorialOverlay
from Utils.AppPath import asset_path

BOX_BG   = (55,35,110)
BOX_LINE = (140,110,220)
TXT      = (255,255,255)
SUB      = (200,190,255)
ACCENT   = (255,215,100)

REPEAT_MODES = ["Once", "Daily", "Weekly", "Monthly", "Yearly"]

class AddReminderPanel:
    def __init__(self, rect, fonts):
        self.rect = pygame.Rect(rect)

        self.fields = {
            "Title": "",
            "Description": "",
            "Date (YYYY-MM-DD)": datetime.now().strftime("%Y-%m-%d"),
            "Time (HH:MM)": "",
            "Repeat": "Once",
            "Notify (10,2,0)": "10,2,0",
            "Reward": "50"
        }
        self.order = list(self.fields.keys())
        self.active = 0

        self.btn_save = pygame.Rect(0,0,160,48)

        # ==== CACHE STATIC SHAPES ====
        self.panel_bg   = self._make_rect(self.rect.size, (40,25,85), 28)
        self.panel_out  = self._make_rect(self.rect.size, (140,110,220), 28, 3)

        self.field_bg   = self._make_rect((self.rect.w-80,42), BOX_BG, 16)
        self.field_out  = self._make_rect((self.rect.w-80,42), BOX_LINE, 16, 3)
        self.field_act  = self._make_rect((self.rect.w-80,42), ACCENT, 16, 3)

        self.btn_bg     = self._make_rect(self.btn_save.size, ACCENT, 18)
        self.btn_out    = self._make_rect(self.btn_save.size, (255,255,255), 18, 2)
        
        self.info_btn = pygame.Rect(0,0,32,32)
        
        self.tutorial = TutorialOverlay(fonts)

        self.ico_info = pygame.image.load(asset_path("Icons/info.png")).convert_alpha()
        self.ico_info_white = pygame.image.load(asset_path("Icons/info_white.png")).convert_alpha()
        
        self.ico_navigating    = pygame.image.load(asset_path("UI/navigating.png")).convert_alpha()
        self.ico_select   = pygame.image.load(asset_path("UI/select.png")).convert_alpha()
        
        self.ico_title    = pygame.image.load(asset_path("UI/title.png")).convert_alpha()
        self.ico_description   = pygame.image.load(asset_path("UI/description.png")).convert_alpha()
        self.ico_date  = pygame.image.load(asset_path("UI/date.png")).convert_alpha()
        self.ico_time   = pygame.image.load(asset_path("UI/time.png")).convert_alpha()
        self.ico_repeat   = pygame.image.load(asset_path("UI/repeat.png")).convert_alpha()
        self.ico_notify  = pygame.image.load(asset_path("UI/notify.png")).convert_alpha()
        self.ico_reward = pygame.image.load(asset_path("UI/reward.png")).convert_alpha()
        
        self.ico_finish  = pygame.image.load(asset_path("UI/task_done.png")).convert_alpha()
        self.ico_edit = pygame.image.load(asset_path("UI/edit_reminder.png")).convert_alpha()

        self.info_hover = False

        self.tutorial.add(self.ico_navigating,"Navigating","TAB",
            "Use TAB to navigate between inputs")
        
        self.tutorial.add(self.ico_select,"Select","LEFT/RIGHT",
            "Use LEFT/RIGHT to switch between repeat types")
        
        self.tutorial.add(self.ico_title,"Title","Text",
            "The title of your task reminder")

        self.tutorial.add(self.ico_description,"Description","Text",
            "Notes of your task reminder")

        self.tutorial.add(self.ico_date,"Date","YYYY-MM-DD",
            "The date of the task")

        self.tutorial.add(self.ico_time,"Time","HH:MM",
            "The time of the task")

        self.tutorial.add(self.ico_repeat,"Repeat","Once, Daily, Etc",
            "When the reminder will be called")

        self.tutorial.add(self.ico_notify,"Notify","Minutes",
            "Notification given before task (in minutes)")

        self.tutorial.add(self.ico_reward,"Reward","Number",
            "The amount of reward for finishing task")
        
        self.tutorial.add(self.ico_finish,"Task Done","LEFT CLICK",
            "Click the star icon on your reminders")
        
        self.tutorial.add(self.ico_edit,"Edit Task","LEFT CLICK",
            "Click your reminders card")

        



    # ===== helpers =====
    def _make_rect(self, size, color, radius, thickness=0):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        if thickness:
            draw_smooth_round_rect_outline(surf, surf.get_rect(), color, radius, thickness)
        else:
            draw_smooth_round_rect(surf, surf.get_rect(), color, radius)
        return surf

    # ================= DRAW =================
    def draw(self, screen, font, offset_x=0):
        x,y,w,h = self.rect
        x += offset_x

        # PANEL
        screen.blit(self.panel_bg, (x,y))
        screen.blit(self.panel_out, (x,y))
        draw_text(screen,"ADD REMINDER",font,TXT,x+40,y+26)
        
        # INFO
        self.info_btn.topleft = (x + w - 46, y + 18)
        ico = self.ico_info_white if self.info_hover else self.ico_info
        screen.blit(pygame.transform.smoothscale(ico,(36,36)),
                    (self.info_btn.centerx-18, self.info_btn.centery-18))


        iy = y + 90
        for i,k in enumerate(self.order):
            pos = (x+40, iy)

            screen.blit(self.field_bg, pos)
            screen.blit(self.field_act if i==self.active else self.field_out, pos)

            draw_text(screen,k,font,SUB,pos[0]+12,pos[1]-24)
            draw_text(screen,self.fields[k],font,TXT,pos[0]+14,pos[1]+10)

            iy += 70

        self.btn_save.center = (x + w//2, y + h - 70)

        screen.blit(self.btn_bg, self.btn_save.topleft)
        screen.blit(self.btn_out, self.btn_save.topleft)

        draw_text(screen,"SAVE",font,(60,40,10),
                  self.btn_save.centerx, self.btn_save.centery, True)
        
        self.tutorial.draw(screen)


    # ================= HANDLE =================
    def handle(self,event):
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.tutorial.active:
            self.tutorial.active = False
            return

        
            # === INFO BUTTON (HARUS SEBELUM MODAL LOCK)
        if event.type == pygame.MOUSEMOTION:
            self.info_hover = self.info_btn.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.info_btn.collidepoint(event.pos):
                self.tutorial.toggle()
                return


        # === MODAL LOCK
        self.tutorial.handle(event)
        if self.tutorial.active:
            return


        key = self.order[self.active]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active = (self.active+1) % len(self.order)

            elif key == "Repeat" and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                i = REPEAT_MODES.index(self.fields["Repeat"])
                self.fields["Repeat"] = REPEAT_MODES[(i + (1 if event.key==pygame.K_RIGHT else -1)) % len(REPEAT_MODES)]

            elif event.key == pygame.K_BACKSPACE:
                self.fields[key] = self.fields[key][:-1]

            elif len(event.unicode)==1 and key != "Repeat":
                self.fields[key] += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_save.collidepoint(event.pos):
                save_new(self.fields)
                Config.ui_state = Config.UI_HOME


