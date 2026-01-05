import json, os, time
from Utils.NotifyQueue import push
from Utils.AppPath import data_path

DATA = os.path.join(data_path(), "DEAL.json")


_cache = []
_last_mtime = 0
_last_check = 0


def load():
    global _cache, _last_mtime
    try:
        mtime = os.path.getmtime(DATA)
        if mtime != _last_mtime:
            with open(DATA, "r", encoding="utf8") as f:
                _cache = json.load(f)
                _last_mtime = mtime
        return _cache
    except:
        return _cache


def save(data):
    try:
        with open(DATA, "w", encoding="utf8") as f:
            json.dump(data, f, indent=2)
    except:
        pass


def check_reminders():
    global _last_check
    if time.time() - _last_check < 2:
        return
    _last_check = time.time()

    data = load()
    now_ts = int(time.time())
    today = time.strftime("%Y-%m-%d")


    dirty = False

    for r in data:
        r.setdefault("_last_check_ts", 0)

        sch = r.get("schedule", {})
        base_time = sch.get("time")
        rtype = sch.get("type", "one_time")
        if not base_time:
            continue

        base_date = today if rtype == "daily" else sch.get("date")
        if not base_date:
            continue

        base_ts = int(time.mktime(time.strptime(f"{base_date} {base_time}", "%Y-%m-%d %H:%M")))

        for mins in sorted(r.get("notify", [0]), reverse=True):
            fire_ts = base_ts - mins * 60
            key = f"_fired_{mins}_{base_date}"

            if now_ts >= fire_ts and not r.get(key):
                r[key] = True

                label = "SEKARANG" if mins == 0 else f"{mins} menit lagi"
                push("Reminder", f"{r['title']} ({label})")
                dirty = True






    if dirty:
        save(data)




