import json, os
from datetime import datetime
from Utils.AppPath import data_path

DATA_PATH = os.path.join(data_path(), "DEAL.json")


def load_all():
    if not os.path.exists(DATA_PATH): return []
    try: return json.load(open(DATA_PATH,"r",encoding="utf8"))
    except: return []

def save_all(d):
    def fix(o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return o

    json.dump(d, open(DATA_PATH,"w",encoding="utf8"),
              indent=2, ensure_ascii=False,
              default=fix)


def mark_reminder_dirty():
    pass
