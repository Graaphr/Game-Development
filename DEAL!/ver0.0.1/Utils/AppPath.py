import os, sys

def app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(__file__))

def data_path():
    base = app_path()
    data = os.path.join(base, "Data")
    os.makedirs(data, exist_ok=True)
    return data

def asset_path(name):
    import os, sys
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "Assets", name)
