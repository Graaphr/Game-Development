import json, os, time
from datetime import date
from Utils.EventBus import emit_reminder_changed
from Utils.AppPath import data_path

DATA = os.path.join(data_path(), "DEAL.json")


def save_new(fields):
    if os.path.exists(DATA):
        with open(DATA, "r", encoding="utf8") as f:
            data = json.load(f)
    else:
        data = []

    new_id = max((item.get("id", 0) for item in data), default=0) + 1
    now_ts = int(time.time())

    reward = int(fields.get("Reward", 1))
    notify_list = [int(x.strip()) for x in fields.get("Notify (10,2,0)", "").split(",") if x.strip().isdigit()]

    date_str = fields.get("Date (YYYY-MM-DD)", date.today().isoformat())

    fired_flags = {f"_fired_{n}_{date_str}": False for n in notify_list}

    data.append({
        "id": new_id,
        "title": fields.get("Title", ""),
        "desc": fields.get("Description", ""),
        "count": reward,

        "schedule": {
            "type": "one_time",
            "date": date_str,
            "time": fields.get("Time (HH:MM)", "00:00")
        },

        "repeat": fields.get("Repeat","Once"),
        "next_show": None,

        "notify": notify_list,
        "_last_check_ts": now_ts,
        "_last_day": None,
        **fired_flags
    })

    with open(DATA, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    emit_reminder_changed()

