# Button hitbox
def is_hover_circle(pos, center, radius):
    mx, my = pos
    return (mx - center[0])**2 + (my - center[1])**2 <= radius**2
