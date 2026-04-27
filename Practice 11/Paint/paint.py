"""
Practice 11 - Paint

Controls:
- B = brush
- R = rectangle
- C = circle
- E = eraser
- Q = square
- T = right triangle
- Y = equilateral triangle
- H = rhombus
- Click a color box to change color
- ESC closes the program
"""

import math
import pygame

pygame.init()

# Window settings
WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Verdana", 18)
small_font = pygame.font.SysFont("Verdana", 13)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (90, 90, 90)
LIGHT_GRAY = (210, 210, 210)
RED = (220, 30, 30)
GREEN = (30, 180, 30)
BLUE = (30, 30, 220)
YELLOW = (255, 220, 0)
PURPLE = (150, 60, 200)

# Tools
TOOL_BRUSH   = "brush"
TOOL_RECT    = "rectangle"
TOOL_CIRCLE  = "circle"
TOOL_ERASER  = "eraser"
TOOL_SQUARE  = "square"
TOOL_RTRI    = "right tri"
TOOL_ETRI    = "equil tri"
TOOL_RHOMBUS = "rhombus"

current_tool  = TOOL_BRUSH
current_color = BLUE
brush_size    = 8

# Persistent drawing surface
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# State for drawing
drawing     = False
start_pos   = None
current_pos = None
last_pos    = None

# Color palette — positioned below the "Colors:" label
palette = [
    (BLACK,  pygame.Rect(20,  25, 30, 30)),
    (RED,    pygame.Rect(60,  25, 30, 30)),
    (GREEN,  pygame.Rect(100, 25, 30, 30)),
    (BLUE,   pygame.Rect(140, 25, 30, 30)),
    (YELLOW, pygame.Rect(180, 25, 30, 30)),
    (PURPLE, pygame.Rect(220, 25, 30, 30)),
]

# Tool buttons in two clean rows
tool_buttons = {
    TOOL_BRUSH:   pygame.Rect(310,  8, 85, 32),
    TOOL_RECT:    pygame.Rect(405,  8, 100, 32),
    TOOL_CIRCLE:  pygame.Rect(515,  8, 85, 32),
    TOOL_ERASER:  pygame.Rect(610,  8, 85, 32),
    TOOL_SQUARE:  pygame.Rect(310, 48, 85, 32),
    TOOL_RTRI:    pygame.Rect(405, 48, 100, 32),
    TOOL_ETRI:    pygame.Rect(515, 48, 100, 32),
    TOOL_RHOMBUS: pygame.Rect(625, 48, 90, 32),
}


def draw_toolbar():
    """Draw toolbar with color palette, tool buttons, and hotkey hints."""
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Colors label
    color_label = small_font.render("Colors:", True, BLACK)
    screen.blit(color_label, (20, 8))

    # Draw color boxes
    for color, rect in palette:
        pygame.draw.rect(screen, color, rect)
        border = 3 if color == current_color else 1
        pygame.draw.rect(screen, BLACK, rect, border)

    # Draw tool buttons
    for tool_name, rect in tool_buttons.items():
        btn_color = YELLOW if current_tool == tool_name else WHITE
        pygame.draw.rect(screen, btn_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        label = small_font.render(tool_name.capitalize(), True, BLACK)
        screen.blit(label, (
            rect.x + rect.width  // 2 - label.get_width()  // 2,
            rect.y + rect.height // 2 - label.get_height() // 2,
        ))

    # Hotkey help text at the bottom of toolbar
    help_text = small_font.render(
        "B=brush  R=rect  C=circle  E=eraser  Q=square  T=right-tri  Y=equil-tri  H=rhombus",
        True, GRAY
    )
    screen.blit(help_text, (10, 78))


def draw_line(surface, color, start, end, width):
    """Draw a smooth freehand line by stamping circles between two points."""
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    if iterations == 0:
        pygame.draw.circle(surface, color, start, width)
        return
    for i in range(iterations + 1):
        p = i / iterations
        x = int(start[0] + (end[0] - start[0]) * p)
        y = int(start[1] + (end[1] - start[1]) * p)
        pygame.draw.circle(surface, color, (x, y), width)


def toolbar_hit(pos):
    """Return True if the mouse position is inside the toolbar."""
    return pos[1] < TOOLBAR_HEIGHT


def canvas_position(pos):
    """Convert screen coordinates to canvas coordinates."""
    return pos[0], pos[1] - TOOLBAR_HEIGHT


def apply_toolbar_click(pos):
    """Handle color and tool selection clicks on the toolbar."""
    global current_color, current_tool
    for color, rect in palette:
        if rect.collidepoint(pos):
            current_color = color
            return
    for tool_name, rect in tool_buttons.items():
        if rect.collidepoint(pos):
            current_tool = tool_name
            return


def right_triangle_points(start, end):
    """
    Right triangle with the right angle at bottom-left:
      A = bottom-left  (right angle)
      B = top-left
      C = bottom-right
    """
    x1, y1 = start
    x2, y2 = end
    left   = min(x1, x2)
    right  = max(x1, x2)
    top    = min(y1, y2)
    bottom = max(y1, y2)
    return [(left, bottom), (left, top), (right, bottom)]


def equilateral_triangle_points(start, end):
    """
    Equilateral triangle with base from start to end.
    Apex is placed above the midpoint at height = side * sqrt(3) / 2.
    """
    x1, y1 = start
    x2, y2 = end
    side = math.hypot(x2 - x1, y2 - y1)
    if side == 0:
        return [start, start, start]
    h  = side * math.sqrt(3) / 2
    dx = (x2 - x1) / side
    dy = (y2 - y1) / side
    # Perpendicular direction (rotated 90° counter-clockwise)
    px = -dy
    py =  dx
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    apex = (int(mx - px * h), int(my - py * h))
    return [(x1, y1), (x2, y2), apex]


def rhombus_points(start, end):
    """
    Rhombus with vertices at the midpoints of the bounding box sides.
    """
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return [
        (cx, y1),  # top
        (x2, cy),  # right
        (cx, y2),  # bottom
        (x1, cy),  # left
    ]


def square_rect(start, end):
    """
    Force a rectangle into a perfect square using the shorter dimension.
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = min(abs(dx), abs(dy))
    sx = start[0] + (side if dx >= 0 else -side)
    sy = start[1] + (side if dy >= 0 else -side)
    return pygame.Rect(
        min(start[0], sx),
        min(start[1], sy),
        side, side,
    )


def draw_preview():
    """Render the canvas and show a live preview of the shape being drawn."""
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if not (drawing and start_pos and current_pos):
        return

    preview = canvas.copy()

    if current_tool == TOOL_RECT:
        r = pygame.Rect(
            min(start_pos[0], current_pos[0]),
            min(start_pos[1], current_pos[1]),
            abs(current_pos[0] - start_pos[0]),
            abs(current_pos[1] - start_pos[1]),
        )
        pygame.draw.rect(preview, current_color, r, 2)

    elif current_tool == TOOL_CIRCLE:
        r = pygame.Rect(
            min(start_pos[0], current_pos[0]),
            min(start_pos[1], current_pos[1]),
            abs(current_pos[0] - start_pos[0]),
            abs(current_pos[1] - start_pos[1]),
        )
        pygame.draw.ellipse(preview, current_color, r, 2)

    elif current_tool == TOOL_SQUARE:
        r = square_rect(start_pos, current_pos)
        pygame.draw.rect(preview, current_color, r, 2)

    elif current_tool == TOOL_RTRI:
        pts = right_triangle_points(start_pos, current_pos)
        pygame.draw.polygon(preview, current_color, pts, 2)

    elif current_tool == TOOL_ETRI:
        pts = equilateral_triangle_points(start_pos, current_pos)
        pygame.draw.polygon(preview, current_color, pts, 2)

    elif current_tool == TOOL_RHOMBUS:
        pts = rhombus_points(start_pos, current_pos)
        pygame.draw.polygon(preview, current_color, pts, 2)

    screen.blit(preview, (0, TOOLBAR_HEIGHT))


def commit_shape():
    """Permanently draw the finished shape onto the canvas."""
    if not start_pos or not current_pos:
        return

    if current_tool == TOOL_RECT:
        r = pygame.Rect(
            min(start_pos[0], current_pos[0]),
            min(start_pos[1], current_pos[1]),
            abs(current_pos[0] - start_pos[0]),
            abs(current_pos[1] - start_pos[1]),
        )
        pygame.draw.rect(canvas, current_color, r, 2)

    elif current_tool == TOOL_CIRCLE:
        r = pygame.Rect(
            min(start_pos[0], current_pos[0]),
            min(start_pos[1], current_pos[1]),
            abs(current_pos[0] - start_pos[0]),
            abs(current_pos[1] - start_pos[1]),
        )
        pygame.draw.ellipse(canvas, current_color, r, 2)

    elif current_tool == TOOL_SQUARE:
        r = square_rect(start_pos, current_pos)
        pygame.draw.rect(canvas, current_color, r, 2)

    elif current_tool == TOOL_RTRI:
        pts = right_triangle_points(start_pos, current_pos)
        pygame.draw.polygon(canvas, current_color, pts, 2)

    elif current_tool == TOOL_ETRI:
        pts = equilateral_triangle_points(start_pos, current_pos)
        pygame.draw.polygon(canvas, current_color, pts, 2)

    elif current_tool == TOOL_RHOMBUS:
        pts = rhombus_points(start_pos, current_pos)
        pygame.draw.polygon(canvas, current_color, pts, 2)


def main():
    global drawing, start_pos, current_pos, last_pos, current_tool

    while True:
        pressed   = pygame.key.get_pressed()
        alt_held  = pressed[pygame.K_LALT]  or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return

                # Keyboard shortcuts
                if event.key == pygame.K_b:
                    current_tool = TOOL_BRUSH
                elif event.key == pygame.K_r:
                    current_tool = TOOL_RECT
                elif event.key == pygame.K_c:
                    current_tool = TOOL_CIRCLE
                elif event.key == pygame.K_e:
                    current_tool = TOOL_ERASER
                elif event.key == pygame.K_q:
                    current_tool = TOOL_SQUARE
                elif event.key == pygame.K_t:
                    current_tool = TOOL_RTRI
                elif event.key == pygame.K_y:
                    current_tool = TOOL_ETRI
                elif event.key == pygame.K_h:
                    current_tool = TOOL_RHOMBUS

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if toolbar_hit(event.pos):
                    apply_toolbar_click(event.pos)
                else:
                    drawing     = True
                    start_pos   = canvas_position(event.pos)
                    current_pos = start_pos
                    last_pos    = start_pos

                    if current_tool == TOOL_BRUSH:
                        pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                    elif current_tool == TOOL_ERASER:
                        pygame.draw.circle(canvas, WHITE, start_pos, brush_size * 2)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                if current_tool not in (TOOL_BRUSH, TOOL_ERASER):
                    commit_shape()
                drawing     = False
                start_pos   = None
                current_pos = None
                last_pos    = None

            if event.type == pygame.MOUSEMOTION and drawing:
                if not toolbar_hit(event.pos):
                    current_pos = canvas_position(event.pos)
                    if current_tool == TOOL_BRUSH and last_pos:
                        draw_line(canvas, current_color, last_pos, current_pos, brush_size)
                    elif current_tool == TOOL_ERASER and last_pos:
                        draw_line(canvas, WHITE, last_pos, current_pos, brush_size * 2)
                    last_pos = current_pos

        draw_toolbar()
        draw_preview()
        pygame.display.flip()
        clock.tick(60)


main()