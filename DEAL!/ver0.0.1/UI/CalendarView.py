# Calendar
import calendar
import pygame
from datetime import datetime
from Utils.Draw import draw_text, draw_gradient_rect, draw_smooth_round_rect, draw_smooth_round_rect_outline, draw_smooth_hline, draw_smooth_circle
from Config import TEXT, SUBTEXT

_calendar_cache = {}
_cached_month = None
_today_cache = {}


def build_calendar_surface(fonts, year, month):
    surf = pygame.Surface((500, 420), pygame.SRCALPHA)
    panel = pygame.Rect(0, 0, 500, 420)

    # Panel
    draw_smooth_round_rect(surf, panel, (0,0,0,120), 40)
    draw_smooth_round_rect_outline(surf, panel, (255,255,255), 40, 3)

    # Header
    header = pygame.Rect(26, 28, 450, 60)
    draw_gradient_rect(surf, header, (110,150,255), (210,140,255), 28)

    month_name = datetime(year, month, 1).strftime("%B").upper()
    draw_text(surf, f"{month_name} {year}", fonts["calendar_title"], (255,255,255),
              header.centerx, header.centery, center=True)

    # Weekday
    days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    start_x = 40
    start_y = header.bottom + 20
    cell_w = (500 - 80)//7
    cell_h = 54

    for i, d in enumerate(days):
        draw_text(surf, d, fonts["small"], SUBTEXT,
                  start_x + i*cell_w + cell_w//2, start_y, True)

    cal = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(year, month)
    grid_y = start_y + 26

        # Cache today position
    for r, week in enumerate(cal):
        y = grid_y + r*cell_h
        draw_smooth_hline(surf, (255,255,255,80), start_x, y, cell_w*7, 1)

        for c, d in enumerate(week):
            if d:
                x = start_x + c*cell_w + cell_w//2
                y_center = y + cell_h//2

                # draw number (default)
                draw_text(surf, str(d), fonts["calendar_day"], TEXT, x, y_center, True)

                # cache today position
                _today_cache[(year, month, d)] = (x, y_center)



    return surf

def draw_today_marker(screen, now, fonts, offset):
    key = (now.year, now.month, now.day)
    if key not in _today_cache:
        return

    base_x = 840 + offset
    base_y = 40

    x, y = _today_cache[key]

    draw_smooth_circle(screen, (255,255,255), (base_x + x, base_y + y), 18)
    draw_text(screen, str(now.day), fonts["calendar_day"],
              (140, 90, 255), base_x + x, base_y + y, True)





def draw_calendar(screen, fonts, offset=0):
    global _cached_month, _calendar_cache

    now = datetime.now()
    key = (now.year, now.month)

    if _cached_month != key:
        _calendar_cache[key] = build_calendar_surface(fonts, now.year, now.month)
        _cached_month = key

    screen.blit(_calendar_cache[key], (840 + offset, 40))

    # Today circle (only dynamic part)
    draw_today_marker(screen, now, fonts, offset)
    
def get_clicked_date(mouse_pos, offset):
    now = datetime.now()
    key = (now.year, now.month)
    if key not in _calendar_cache:
        return None

    start_x = 840 + offset + 40
    start_y = 40 + 28 + 60 + 20 + 26   # panel + header + spacing

    cell_w = (500 - 80)//7
    cell_h = 54

    cal = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(now.year, now.month)

    mx, my = mouse_pos
    for r, week in enumerate(cal):
        for c, d in enumerate(week):
            if not d: continue
            x = start_x + c*cell_w
            y = start_y + r*cell_h
            if pygame.Rect(x,y,cell_w,cell_h).collidepoint(mx,my):
                return f"{now.year}-{now.month:02}-{d:02}"
    return None


