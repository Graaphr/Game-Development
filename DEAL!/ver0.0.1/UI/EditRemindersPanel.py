import pygame, Config
from Utils.ReminderStore import load_all, save_all
from Utils.Draw import draw_text, draw_smooth_round_rect, draw_smooth_round_rect_outline

BOX_BG   = (55,35,110)
BOX_LINE = (140,110,220)
TXT      = (255,255,255)
SUB      = (200,190,255)
ACCENT   = (255,215,100)
DANGER   = (200,60,80)

REPEAT_MODES = ["Once", "Daily", "Weekly", "Monthly", "Yearly"]

def _make_rect(size, color, radius, thickness=0):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        if thickness:
            draw_smooth_round_rect_outline(surf, surf.get_rect(), color, radius, thickness)
        else:
            draw_smooth_round_rect(surf, surf.get_rect(), color, radius)
        return surf

class EditReminderPanel:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.anim = 0.0
        self.reminder_id = None

        self.fields = {
            "Title": "",
            "Description": "",
            "Date (YYYY-MM-DD)": "",
            "Time (HH:MM)": "",
            "Repeat": "Once",
            "Notify (10,2,0)": "10,2,0",
            "Reward": "50"
        }
        self.order = list(self.fields.keys())
        self.active = 0

        self.btn_save = pygame.Rect(0,0,160,48)
        self.btn_del  = pygame.Rect(0,0,160,48)

        # BUILD UI
        self.panel_bg  = _make_rect(self.rect.size, (40,25,85), 28)
        self.panel_out = _make_rect(self.rect.size, (140,110,220), 28, 3)

        self.field_bg  = _make_rect((self.rect.w-80,42), BOX_BG, 16)
        self.field_out = _make_rect((self.rect.w-80,42), BOX_LINE, 16, 3)
        self.field_act = _make_rect((self.rect.w-80,42), ACCENT, 16, 3)

        self.btn_bg   = _make_rect(self.btn_save.size, ACCENT, 18)
        self.btn_out  = _make_rect(self.btn_save.size, (255,255,255), 18, 2)
        self.del_bg   = _make_rect(self.btn_del.size, DANGER, 18)
        self.del_out  = _make_rect(self.btn_del.size, (255,255,255), 18, 2)

    def update(self, dt):
        target = 1 if Config.ui_state == Config.UI_EDIT else 0
        self.anim += (target - self.anim) * min(dt * 8, 1)

    def open(self, reminder):
        self.reminder_id = reminder["id"]
        self.fields["Title"] = reminder.get("title","")
        self.fields["Description"] = reminder.get("desc","")
        self.fields["Date (YYYY-MM-DD)"] = reminder.get("schedule",{}).get("date","")
        self.fields["Time (HH:MM)"] = reminder.get("time","")
        self.fields["Repeat"] = reminder.get("repeat","Once")
        self.fields["Notify (10,2,0)"] = ",".join(str(n) for n in reminder.get("notify",[10,2,0]))
        self.fields["Reward"] = str(reminder.get("count",0))
        self.active = 0

    def draw(self, screen, font):
        x,y,w,h = self.rect
        x += int((1 - self.anim) * w)

        screen.blit(self.panel_bg,(x,y))
        screen.blit(self.panel_out,(x,y))
        draw_text(screen,"EDIT REMINDER",font,TXT,x+40,y+26)

        iy = y+90
        for i,k in enumerate(self.order):
            pos=(x+40,iy)
            screen.blit(self.field_bg,pos)
            screen.blit(self.field_act if i==self.active else self.field_out,pos)
            draw_text(screen,k,font,SUB,pos[0]+12,pos[1]-24)
            draw_text(screen,str(self.fields[k] or ""),font,TXT,pos[0]+14,pos[1]+10)
            iy+=70

        self.btn_save.center = (x+w//2-90, y+h-70)
        self.btn_del.center  = (x+w//2+90, y+h-70)

        screen.blit(self.btn_bg,self.btn_save.topleft)
        screen.blit(self.btn_out,self.btn_save.topleft)
        draw_text(screen,"SAVE",font,(60,40,10),self.btn_save.centerx,self.btn_save.centery,True)

        screen.blit(self.del_bg,self.btn_del.topleft)
        screen.blit(self.del_out,self.btn_del.topleft)
        draw_text(screen,"DELETE",font,(255,255,255),self.btn_del.centerx,self.btn_del.centery,True)

    def handle(self,event):
        if not (0.05 < self.anim <= 1): return
        key = self.order[self.active]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active = (self.active+1)%len(self.order)
            elif key=="Repeat" and event.key in (pygame.K_LEFT,pygame.K_RIGHT):
                i = REPEAT_MODES.index(self.fields["Repeat"])
                self.fields["Repeat"] = REPEAT_MODES[(i+(1 if event.key==pygame.K_RIGHT else -1))%len(REPEAT_MODES)]
            elif event.key==pygame.K_BACKSPACE:
                self.fields[key] = self.fields[key][:-1]
            elif len(event.unicode)==1 and key!="Repeat":
                if not isinstance(self.fields[key], str):
                    self.fields[key] = str(self.fields[key])
                self.fields[key] += event.unicode


        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.btn_save.collidepoint(event.pos): self._save()
            if self.btn_del.collidepoint(event.pos): self._delete()

    def _save(self):
        data = load_all()
        for r in data:
            if r["id"] == self.reminder_id:

                # UPDATE SCHEDULE
                new_date = self.fields["Date (YYYY-MM-DD)"]

                r["schedule"]["type"] = "one_time"
                r["schedule"]["date"] = new_date
                r["schedule"]["time"] = self.fields["Time (HH:MM)"]


                # UPDATE BASIC
                r["title"]  = self.fields["Title"]
                r["desc"]   = self.fields["Description"]
                r["repeat"] = self.fields["Repeat"]
                raw = str(self.fields["Notify (10,2,0)"])
                r["notify"] = sorted({
                    min(1440, int(x.strip()))
                    for x in raw.split(",") if x.strip().isdigit()
                }, reverse=True)


                # HARD RESET FIRED STATUS
                for k in list(r.keys()):
                    if k.startswith("_fired_"):
                        del r[k]

                for n in r["notify"]:
                    r[f"_fired_{n}_{new_date}"] = False

                r["_last_day"] = None
                r["_done"] = False
                r["next_show"] = None


        save_all(data)
        Config.ui_state = Config.UI_HOME


    def _delete(self):
        save_all([r for r in load_all() if r["id"]!=self.reminder_id])
        Config.ui_state = Config.UI_HOME

edit_panel = EditReminderPanel((830, 40, 520, 700))
