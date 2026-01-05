import pygame, json, os, Config
from datetime import datetime, timedelta
from Utils.Draw import draw_text, draw_smooth_round_rect, draw_smooth_round_rect_outline, draw_smooth_circle
from Config import scroll_y, scroll_vel, trigger_star_happy
from .EditRemindersPanel import edit_panel
from Utils.ReminderStore import load_all, save_all
from Utils.AppPath import data_path

DATA_PATH = os.path.join(data_path(), "DEAL.json")


HITBOX = {}

PLAYER_PATH = os.path.join(data_path(), "PLAYER.json")

def load_player():
    if not os.path.exists(PLAYER_PATH):
        return {"coins": 0}
    try:
        return json.load(open(PLAYER_PATH,"r",encoding="utf8"))
    except:
        return {"coins": 0}

def save_player(p):
    json.dump(p, open(PLAYER_PATH,"w",encoding="utf8"), indent=2)


pending_remove = set()
completed_anim = {}
claim_anim = {}
coin_popups = []
sparkles = []

_coin_cache = None
_star_cache = None
_star_yellow_cache = None

# ===================================================

def calc_next_show(r):
    now = datetime.now()
    return {
        "Daily":   now + timedelta(days=1),
        "Weekly":  now + timedelta(weeks=1),
        "Monthly": now.replace(month=now.month%12+1),
        "Yearly":  now.replace(year=now.year+1)
    }.get(r.get("repeat","Once"))

# ===================================================

def get_visible():
    now = datetime.now()
    data = load_all()
    visible = []

    for r in data:
        rid = r["id"]

        if rid in claim_anim or rid in pending_remove:
            visible.append(r)
            continue

        if r.get("_done"):
            if r["repeat"] == "Once":
                continue
            if r.get("next_show") and now < datetime.fromisoformat(r["next_show"]):
                continue
            r["_done"] = False
            r["next_show"] = None

        visible.append(r)

    return visible

# ===================================================

def handle_reminder_scroll(event, offset=0):
    global scroll_vel
    if event.type == pygame.MOUSEWHEEL:
        mx,my = pygame.mouse.get_pos()
        mx -= offset
        if 820 <= mx <= 1360 and 480 <= my <= 780:
            scroll_vel += event.y * 160

# ===================================================

def handle_reminder_click(event, fonts, offset=0):
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return

    mx,my = pygame.mouse.get_pos()
    mx -= offset

    full = load_all()

    for r in get_visible():
        rid = r["id"]
        hb = HITBOX.get(rid)
        if not hb: 
            continue

        if hb["star"].collidepoint(mx,my):
            trigger_star_happy()

            for x in full:
                if x["id"] == rid:
                    x["_done"] = True
                    x["next_show"] = calc_next_show(x)
                    break
            save_all(full)

            player = load_player()
            player["currency"] = player.get("currency",0) + r["count"]
            save_player(player)

            claim_anim[rid] = 0

            card = hb["card"]
            
            coin_popups.append({
                "x": card.right-50,
                "y": card.centery,
                "alpha": 255,
                "vy": -160,
                "surf": fonts["coins"].render(f'+{r["count"]}', True, (255,255,255))
            })

            for i in range(4):
                sparkles.append({
                    "x": card.x+12, "y": card.centery,
                    "vx": 80+i*40, "vy": -100-i*40, "life": 0.5
                })
            return

        if hb["card"].collidepoint(mx,my):
            Config.ui_state = Config.UI_EDIT
            edit_panel.open(r)
            return



# ===================================================

def draw_reminders(screen, fonts, assets, dt, offset=0):
    HITBOX.clear()

    global scroll_y, scroll_vel, _coin_cache, _star_cache, _star_yellow_cache

    if _coin_cache is None:
        _coin_cache = pygame.transform.smoothscale(assets["coin"], (26,26))
    if _star_cache is None:
        _star_cache = pygame.transform.smoothscale(assets["star"], (50,50))
    if _star_yellow_cache is None:
        _star_yellow_cache = pygame.transform.smoothscale(assets["star_done"], (50,50))

    VIEWPORT = pygame.Rect(820 + offset, 480, 560, 260)
    screen.set_clip(VIEWPORT)

    reminders = get_visible()
    
    # SCROLL PHYSICS
    scroll_y += scroll_vel * dt
    scroll_vel *= 0.86
    if abs(scroll_vel) < 1:
        scroll_vel = 0

    # VISUAL ANCHOR
    TOP_Y = 500
    VIEW_H = 260
    CARD_H = 84
    BOTTOM_PADDING = 24
    CONTENT_H = len(reminders) * CARD_H + BOTTOM_PADDING


    # KILL SCROLL IF SHORT CONTENT
    if CONTENT_H <= VIEW_H:
        scroll_y = 0
    else:
        MIN_SCROLL = VIEW_H - CONTENT_H

        if scroll_y > 0:
            scroll_y = 0
            scroll_vel = 0
        elif scroll_y < MIN_SCROLL:
            scroll_y = MIN_SCROLL
            scroll_vel = 0

    y = TOP_Y + scroll_y

    for r in reminders:
        rid = r["id"]

        if rid in claim_anim:
            claim_anim[rid] += dt*2.4
            if claim_anim[rid] >= 1:
                pending_remove.add(rid)
                completed_anim[rid] = 0
                del claim_anim[rid]

        if rid in pending_remove:
            completed_anim[rid] += dt*2.4

        anim = completed_anim.get(rid,0)
        xoff = int(anim * 760)

        card = pygame.Rect(840 + xoff + offset, y, 500, 64)
        star = pygame.Rect(card.x, card.centery-21, 42, 42)

        HITBOX[r["id"]] = {
            "card": card,
            "star": star
        }


        draw_smooth_round_rect(screen, card, (255,255,255,18), 40)
        draw_smooth_round_rect_outline(screen, card, (255,255,255), 40, 2)

        star_center = star.center
        draw_smooth_circle(screen, (255,255,255), star_center, 38)

        if rid in claim_anim or rid in pending_remove:
            screen.blit(_star_yellow_cache, _star_yellow_cache.get_rect(center=star_center))
        else:
            screen.blit(_star_cache, _star_cache.get_rect(center=star_center))

        draw_text(screen, r["title"], fonts["calendar_day"], (255,255,255),
                card.x+90, card.centery-fonts["calendar_day"].get_height()//2)

        cx = card.right - 50
        screen.blit(_coin_cache, (cx, card.centery-13))
        draw_text(screen, str(r["count"]), fonts["taskcoin"], (255,255,255),
                cx-20, card.centery-fonts["taskcoin"].get_height()//2)

        if rid in pending_remove and anim >= 1:
            pending_remove.remove(rid)
            completed_anim.pop(rid)

        y += 84


    # FLOATING COINS
    for p in coin_popups[:]:
        p["y"] += p["vy"] * dt
        p["alpha"] -= 320 * dt
        if p["alpha"] <= 0:
            coin_popups.remove(p)
            continue
        surf = p["surf"]
        surf.set_alpha(int(p["alpha"]))
        screen.blit(surf,(p["x"]+offset,p["y"]))

    # SPARKLES
    for s in sparkles[:]:
        s["x"] += s["vx"] * dt
        s["y"] += s["vy"] * dt
        s["life"] -= dt
        if s["life"] <= 0:
            sparkles.remove(s)
            continue
        screen.blit(assets["sparkle"],(int(s["x"]+offset),int(s["y"])))
        
    screen.set_clip(None)

# ===================================================

_reminder_cache = None
_reminder_dirty = True

def load_reminders():
    global _reminder_cache, _reminder_dirty

    if not _reminder_dirty and _reminder_cache is not None:
        return _reminder_cache

    if not os.path.exists(DATA_PATH):
        _reminder_cache = []
        return _reminder_cache

    try:
        data = json.load(open(DATA_PATH,"r",encoding="utf-8"))
    except:
        data = []

    now = datetime.now()
    visible = []
    changed = False

    for r in data:
        next_show = r.get("next_show")
        if next_show:
            if datetime.fromisoformat(next_show) <= now:
                r["next_show"] = None
                visible.append(r)
                changed = True
        else:
            visible.append(r)

    if changed:
        json.dump(data, open(DATA_PATH,"w",encoding="utf-8"), indent=2)

    _reminder_cache = visible
    _reminder_dirty = False
    return visible
