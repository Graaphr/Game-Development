# Draw & Smoothify utilities
import pygame

def draw_round_rect(surface, rect, color, radius=18):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_text(surface, text, font, color, x, y, center=False):
    surf = font.render(text, True, color)

    if center:
        rect = surf.get_rect(center=(x, y))
    else:
        rect = surf.get_rect(topleft=(x, y))

    surface.blit(surf, rect)

def draw_smooth_circle(surface, color, center, radius, scale=3):
    temp = pygame.Surface(
        (radius * 2 * scale, radius * 2 * scale),
        pygame.SRCALPHA
    )
    pygame.draw.circle(
        temp,
        color,
        (radius * scale, radius * scale),
        radius * scale
    )
    smooth = pygame.transform.smoothscale(
        temp, (radius * 2, radius * 2)
    )
    surface.blit(smooth, (center[0] - radius, center[1] - radius))
    
def draw_smooth_round_rect(surface, rect, color, radius, scale=3):
    temp = pygame.Surface(
        (rect.width * scale, rect.height * scale),
        pygame.SRCALPHA
    )
    pygame.draw.rect(
        temp,
        color,
        temp.get_rect(),
        border_radius=radius * scale
    )
    smooth = pygame.transform.smoothscale(temp, (rect.width, rect.height))
    surface.blit(smooth, rect.topleft)


def draw_smooth_round_rect_outline(surface, rect, color, radius, thickness=2, scale=3):
    temp = pygame.Surface(
        (rect.width * scale, rect.height * scale),
        pygame.SRCALPHA
    )
    pygame.draw.rect(
        temp,
        color,
        temp.get_rect(),
        width=thickness * scale,
        border_radius=radius * scale
    )
    smooth = pygame.transform.smoothscale(temp, (rect.width, rect.height))
    surface.blit(smooth, rect.topleft)

def draw_gradient_rect(surface, rect, color1, color2, radius, scale=3):
    temp = pygame.Surface(
        (rect.width * scale, rect.height * scale),
        pygame.SRCALPHA
    )

    for x in range(temp.get_width()):
        t = x / temp.get_width()
        r = color1[0] + (color2[0] - color1[0]) * t
        g = color1[1] + (color2[1] - color1[1]) * t
        b = color1[2] + (color2[2] - color1[2]) * t

        pygame.draw.line(
            temp,
            (int(r), int(g), int(b)),
            (x, 0),
            (x, temp.get_height())
        )

    mask = pygame.Surface(temp.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(
        mask,
        (255, 255, 255),
        mask.get_rect(),
        border_radius=radius * scale
    )

    temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    smooth = pygame.transform.smoothscale(
        temp, (rect.width, rect.height)
    )

    surface.blit(smooth, rect.topleft)

    
def draw_smooth_hline(surface, color, x, y, length, thickness=1, scale=3):
    temp = pygame.Surface((length * scale, thickness * scale), pygame.SRCALPHA)
    pygame.draw.rect(temp, color, temp.get_rect())
    smooth = pygame.transform.smoothscale(temp, (length, thickness))
    surface.blit(smooth, (x, y))



