# Main.py
import pygame, math, random, pygame.display, Config, os, sys

from AssetsScript import load_assets, load_splash_assets

from UI.Sidebar import Sidebar
from UI.Character import draw_character
from UI.CalendarView import draw_calendar, get_clicked_date
from UI.Reminders import draw_reminders, handle_reminder_scroll, handle_reminder_click, load_reminders
from UI.QuitButton import draw_quit_button
from UI.AddRemindersButton import AddReminderButton
from UI.AddRemindersPanel import AddReminderPanel
from UI.EditRemindersPanel import edit_panel
from UI.NoteBoard import NoteBoard
from UI.NoteEditorPanel import NoteEditorPanel
from UI.SplashScreen import SplashScreen
from UI.SettingsPanel import SettingsPanel

from Utils.Hitbox import is_hover_circle
from Utils.Tray import create_tray, stop_tray, hide_window, show_window
from Utils.NotifierThread import NotifierThread
from Utils.EventBus import on_reminder_changed
from Utils.AppPath import asset_path
from Utils.SettingsStore import load_settings

def resource_path(rel):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, rel)


notifier = NotifierThread()
notifier.start()

in_tray = False

reminders = []

def reload_reminders():
    global reminders
    reminders = load_reminders()
    
on_reminder_changed(reload_reminders)

def restore_app():
    global in_tray
    stop_tray()
    show_window()
    in_tray = False
    pygame.mixer.music.unpause()


def exit_app():
    notifier.stop()
    stop_tray()
    pygame.quit()
    exit()




pygame.init()
pygame.mixer.init()

cfg = load_settings()

pygame.mixer.music.load(resource_path("Assets/Sounds/Music/BGM/bgm_main.mp3"))
pygame.mixer.music.set_volume(0.1)

pygame.display.set_icon(pygame.image.load(asset_path("icon.png")))
pygame.display.set_caption("DEAL")

pygame.event.set_allowed([
    pygame.QUIT,
    pygame.KEYDOWN,
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEWHEEL,
    pygame.MOUSEMOTION
])


info = pygame.display.Info()
screen = pygame.display.set_mode(
    (info.current_w, info.current_h),
    pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED | pygame.DOUBLEBUF,
    vsync=1
)

pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED | pygame.DOUBLEBUF
WIDTH, HEIGHT = screen.get_size()
clock = pygame.time.Clock()
ui_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


icons, power_white, power_red, background, character, character_closed, character_happy, fonts = load_assets(WIDTH, HEIGHT)

sidebar = Sidebar(40, HEIGHT // 2 - 220, icons,
                  ["calendar", "notes", "cart", "trophy", "settings"])

add_btn = AddReminderButton((80, 80), 46, icons)

add_panel = AddReminderPanel(Config.ADD_PANEL_RECT, fonts)

settings_panel = SettingsPanel(fonts)



power_white = pygame.transform.smoothscale(power_white, (42, 42))
power_red   = pygame.transform.smoothscale(power_red, (42, 42))

QUIT_BTN_CENTER = (80, 680)
QUIT_BTN_RADIUS = 46

panel_offset = WIDTH
ui_offset = 0


noteboard = NoteBoard(None, fonts)
note_editor = NoteEditorPanel((460,220,600,360), noteboard, fonts)
noteboard.editor = note_editor

splash_assets = load_splash_assets()
splash = SplashScreen(screen, splash_assets)
splash_clock = pygame.time.Clock()

while True:
    dt = splash_clock.tick(60) / 1000
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); exit()

    if splash.update(dt):
        cfg = load_settings()

        pygame.mixer.music.play(-1, fade_ms=1200)

        if not cfg.get("bgm_on", True):
            pygame.mixer.music.pause()

        break

    splash.draw()
    pygame.display.flip()




running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(background, (0, 0))
    
    dt_anim = min(clock.tick(120) / 1000, 1/60)

    for event in pygame.event.get():

        # Kunci Modal
        if Config.ui_state == Config.UI_ADDING:

            # Bolehkan Tutup / Exit / Tambah
            if event.type == pygame.MOUSEBUTTONDOWN:
                if add_btn.handle_click(event.pos):
                    Config.ui_state = Config.UI_HOME
                    continue

                if is_hover_circle(event.pos, QUIT_BTN_CENTER, QUIT_BTN_RADIUS):
                    running = False
                    continue

            add_panel.handle(event)
            continue


        # EXIT
        if event.type == pygame.QUIT:
            running = False
            continue

        # Modal Tutorial Pengingat
        if noteboard.tutorial.active:
            noteboard.tutorial.handle(event)
            continue

        # Modal Tutorial Note
        if note_editor.active:
            note_editor.handle(event)
            continue

        # EXIT ketika tidak ada modal (ESCAPE)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not in_tray:
            hide_window()
            create_tray(restore_app, exit_app)
            in_tray = True
            pygame.mixer.music.pause()
            continue

        # NoteBoard
        if Config.ui_state == Config.UI_NOTEBOARD:
            noteboard.handle(event)

        # Home
        handle_reminder_click(event, fonts, ui_offset)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if add_btn.handle_click(event.pos):
                Config.ui_state = (
                    Config.UI_HOME if Config.ui_state == Config.UI_ADDING
                    else Config.UI_ADDING
                )



        if Config.ui_state == Config.UI_ADDING:
            add_panel.handle(event)

        if Config.ui_state == Config.UI_EDIT:
            edit_panel.handle(event)
            
        if Config.ui_state == Config.UI_SETTINGS:
            settings_panel.handle(event)


        if sidebar.active == 0:
            handle_reminder_scroll(event, ui_offset)

        # Sidebar / Quit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_hover_circle(event.pos, QUIT_BTN_CENTER, QUIT_BTN_RADIUS):
                running = False
            else:
                clicked = sidebar.handle_click(event.pos)
                if clicked == 1:
                    Config.ui_state = Config.UI_NOTEBOARD
                elif clicked == 0:
                    Config.ui_state = Config.UI_HOME
                elif clicked == 4:
                    Config.ui_state = Config.UI_SETTINGS





    if in_tray:
        clock.tick(5)
        continue

    if Config.star_state != Config.star_happy:

        Config.blink_timer -= dt_anim

        if Config.blink_state == 0 and Config.blink_timer <= 0:
            Config.blink_state = 1
            Config.blink_timer = 0.12

        elif Config.blink_state == 1 and Config.blink_timer <= 0:
            Config.blink_state = 0
            Config.blink_timer = random.uniform(3, 7)
        
    if Config.star_state == Config.star_happy:
        Config.star_emotion_timer -= dt_anim
        if Config.star_emotion_timer <= 0:
            Config.star_state = Config.star_normal


    # Animasi Panel Tambah Pengingat
    if Config.ui_state == Config.UI_ADDING:
        panel_offset = max(panel_offset - 36, 0)
    else:
        panel_offset = min(panel_offset + 36, WIDTH)

    
    if Config.star_state == Config.star_happy:
        active_sprite = character_happy
    else:
        active_sprite = character_closed if Config.blink_state == 1 else character

    draw_character(ui_layer, active_sprite, (Config.x, HEIGHT // 2), int(Config.size))

    add_btn.draw(ui_layer, fonts, mouse_pos)
    sidebar.draw(ui_layer)
    draw_quit_button(ui_layer, mouse_pos, QUIT_BTN_CENTER, QUIT_BTN_RADIUS,
                     power_white, power_red)
    settings_panel.update(dt_anim)


    if sidebar.active == 0:

        if Config.ui_state == Config.UI_HOME:
            ui_offset = max(ui_offset - 24, 0)
        else:
            ui_offset = min(ui_offset + 24, WIDTH)

        draw_calendar(ui_layer, fonts, ui_offset)
        draw_reminders(ui_layer, fonts, icons, dt_anim, ui_offset)

        # Animasi Panel Edit
        edit_panel.update(dt_anim)
        if edit_panel.anim > 0.01:
            edit_panel.draw(ui_layer, fonts["calendar_day"])


    if panel_offset < WIDTH:
        add_panel.draw(ui_layer, fonts["calendar_day"], panel_offset)

        

    screen.blit(ui_layer, (0, 0))
    ui_layer.fill((0,0,0,0))
    
    settings_panel.draw(screen)
    
    if Config.ui_state == Config.UI_NOTEBOARD:
        noteboard.draw(screen)
        
    note_editor.draw(screen)


    
    if noteboard.dirty:
        noteboard.save()
        noteboard.dirty = False
    
    pygame.display.flip()

pygame.quit()