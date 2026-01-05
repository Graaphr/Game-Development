# Utils/Tray.py
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image
import win32gui
import win32con

tray_icon = None
hwnd = None
tray_running = False


def hide_window():
    global hwnd
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


def show_window():
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)


def create_tray(on_restore, on_exit):
    global tray_icon, tray_running

    # DO NOTHING if tray already exists
    if tray_running:
        return

    tray_running = True

    def run_tray():
        global tray_icon
        image = Image.open("Assets/icon.png")

        menu = (
            item("Open DEAL", lambda icon, item: on_restore()),
            item("Exit", lambda icon, item: on_exit()),
        )

        tray_icon = pystray.Icon(
            "DEAL",
            image,
            "DEAL",
            menu
        )
        tray_icon.run()

    threading.Thread(target=run_tray, daemon=True).start()


def stop_tray():
    global tray_icon, tray_running

    if tray_icon:
        tray_icon.stop()
        tray_icon = None

    tray_running = False
