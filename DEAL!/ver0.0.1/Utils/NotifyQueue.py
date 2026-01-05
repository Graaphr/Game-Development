from collections import deque

queue = deque()

def push(title, message):
    queue.append((title, message))

def pop_all():
    items = list(queue)
    queue.clear()
    return items
