_callbacks = []

def on_reminder_changed(func):
    _callbacks.append(func)

def emit_reminder_changed():
    for cb in _callbacks:
        cb()
