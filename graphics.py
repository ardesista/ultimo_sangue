import pygame

SCREEN_WIDTH            = 1280 # px
SCREEN_HEIGHT           = 720 # px
FONT_SIZE               = 24 # px

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sysfont = pygame.font.SysFont(None, FONT_SIZE)

def draw_circle(x, y, color, radius, line_width=0):
    pygame.draw.circle(screen, color, (x, y), radius, line_width)

def draw_line(x, y, color, x2, y2):
    pygame.draw.aaline(screen, color, (x, y), (x2, y2))

def draw_equi_triangle(x, y, color, side, line_width=0):
    h2 = .5 * 3**.5 * side
    pygame.draw.polygon(screen, color, [ (x, y - .65 * h2), (x - .5 * side, y + .35 * h2), (x + .5 * side, y + .35 * h2) ], line_width)

def draw_rect(x, y, color, width, height, line_width=0):
    pygame.draw.rect(screen, color, pygame.Rect(x - .5 * width, y - .5 * height, width, height), line_width)

def draw_text(x, y, color, text, background=None):
    img = sysfont.render(text, True, color, background)
    img_size = img.get_size()
    screen.blit(img, (x - img_size[0] // 2, y - img_size[1] // 2))

def quit_requested():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return True
    return False
