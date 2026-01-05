import pygame, os, sys

# Pyinstaller Temp Path

def resource_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)


def load_assets(width, height):
    # All Icons
    icons = {
        "calendar": pygame.image.load(resource_path("Assets/Icons/calendar.png")).convert_alpha(),
        "notes": pygame.image.load(resource_path("Assets/Icons/note.png")).convert_alpha(),
        "cart": pygame.image.load(resource_path("Assets/Icons/cart.png")).convert_alpha(),
        "trophy": pygame.image.load(resource_path("Assets/Icons/trophy.png")).convert_alpha(),
        "settings": pygame.image.load(resource_path("Assets/Icons/settings.png")).convert_alpha(),
        "star": pygame.image.load(resource_path("Assets/Icons/star.png")).convert_alpha(),
        "star_done": pygame.image.load(resource_path("Assets/Icons/star_done.png")).convert_alpha(),
        "sparkle": pygame.image.load(resource_path("Assets/Icons/star.png")).convert_alpha(),
        "coin": pygame.image.load(resource_path("Assets/Icons/coin.png")).convert_alpha(),
        "plus": pygame.image.load(resource_path("Assets/Icons/plus.png")).convert_alpha(),
        "x": pygame.image.load(resource_path("Assets/Icons/close.png")).convert_alpha()
    }

    power_white = pygame.image.load(resource_path("Assets/Icons/power_white.png")).convert_alpha()
    power_red   = pygame.image.load(resource_path("Assets/Icons/power_red.png")).convert_alpha()

    bg = pygame.image.load(resource_path("Assets/BG.png")).convert()
    bg = pygame.transform.scale(bg, (width, height))

    character = pygame.image.load(resource_path("Assets/Character/star.png")).convert_alpha()
    character_closed = pygame.image.load(resource_path("Assets/Character/star_closed.png")).convert_alpha()
    character_happy  = pygame.image.load(resource_path("Assets/Character/star_happy.png")).convert_alpha()

    # All Fonts
    fonts = {
        # General
        "normal": pygame.font.SysFont("arial", 18),

        # Calendar
        "calendar_title": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 32),
        "calendar_day":   pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 18),
        "small":          pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 14),

        # Reminder
        "coins":    pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 32),
        "taskcoin": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 18),
        
        # Modal
        "tutorial_title": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 32),
        "tutorial_description": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 18),
        
        # Settings Panel
        "settings_title": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 24),
        "settings_subtitle": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 20),
        "settings_small": pygame.font.Font(resource_path("Assets/Fonts/SpicySale.ttf"), 16),
        
    }

    return icons, power_white, power_red, bg, character, character_closed, character_happy, fonts

# SplashScreen Asset
def load_splash_assets():
    ouro = pygame.image.load(resource_path("Assets/Logo/OuroborozStudioLogo.png")).convert_alpha()
    deal = pygame.image.load(resource_path("Assets/Logo/DealLogo.png")).convert_alpha()
    return ouro, deal

