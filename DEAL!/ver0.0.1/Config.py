# Config
import random

# Main configuration
VIRTUAL_W = 1920
VIRTUAL_H = 1080

ICON_SIZE = 32
ICON_GAP = 80
BTN_RADIUS = 26

BG = (20, 10, 45)
CARD = (40, 25, 85)
CARD_LIGHT = (65, 45, 120)
TEXT = (255, 255, 255)
SUBTEXT = (200, 190, 255)
ACCENT = (255, 215, 100)

# Sidebar configuration
ANIM_SPEED = 0.2
ICON_ANIM_SPEED = 0.25

# Reminders configuration
scroll_y = 0
SCROLL_SPEED = 30
scroll_vel = 0.0

# Add Reminders Configuration
ADD_BTN_OFFSET_X = 40
ADD_BTN_OFFSET_Y = -140
ADD_BTN_RADIUS = 46

# Char configuration
blink_timer = random.uniform(3, 6)
blink_state = 0

star_normal = 0
star_happy  = 1

star_state = star_normal
star_emotion_timer = 0

size = 600
x = 480

def trigger_star_happy():
    global star_state, star_emotion_timer
    star_state = 1
    star_emotion_timer = 1

# UI States
UI_HOME      = 0
UI_ADDING    = 1
UI_EDIT      = 2
UI_NOTEBOARD = 3
UI_SETTINGS  = 4
UI_NOTE_EDIT = 5



ui_state = UI_HOME
ui_anim_x = 0.0

ADD_PANEL_RECT = (830, 40, 520, 700)









