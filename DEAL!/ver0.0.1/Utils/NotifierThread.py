# Utils/NotifierThread.py
import threading, time
from Utils.Notifier import check_reminders
from Utils.NotifyQueue import pop_all
from plyer import notification

class NotifierThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = True

    def run(self):
        while self.running:
            check_reminders()

            for title, msg in pop_all():
                notification.notify(
                    title=title,
                    message=msg,
                    timeout=10,
                    app_name="DEAL"
                )

            time.sleep(1)

    def stop(self):
        self.running = False
