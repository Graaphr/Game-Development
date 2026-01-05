import json, os
from Utils.AppPath import data_path

PATH = os.path.join(data_path(), "SETTINGS.json")

DEFAULT = {
    "bgm_on": True
}

def load_settings():
    if not os.path.exists(PATH):
        save_settings(DEFAULT)
        return DEFAULT.copy()

    try:
        with open(PATH, "r") as f:
            return json.load(f)
    except:
        return DEFAULT.copy()

def save_settings(data):
    with open(PATH, "w") as f:
        json.dump(data, f, indent=4)
