import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 600

# Colors
color_red = (255, 69, 0)
color_blue = (70, 130, 180)
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_yellow = (255, 215, 0)

#assigning colors to keys
colors = {
    pygame.K_1: color_black,
    pygame.K_2: color_red,
    pygame.K_3: color_blue,
    pygame.K_4: color_yellow
}

picked_color = color_black  # default color

# preparing the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(color_white)
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(color_white)

pygame.display.set_caption("tamilana's paint")
clock = pygame.time.Clock()

LMB_pressed = False
THICKNESS = 5 #default thickness

curr_x = curr_y = prev_x = prev_y = 0
running = True

# default tool
current_tool = 'brush'

# function to calculate rectangle dimensions
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

# function to calculate square dimensions
def calculate_square(x1, y1, x2, y2):
    side = min(abs(x2 - x1), abs(y2 - y1))
    return pygame.Rect(min(x1, x2), min(y1, y2), side, side)

# function to calculate equilateral triangle points
def calculate_eq_triangle(x1, y1, x2, y2):
    side_length = math.dist((x1, y1), (x2, y2))
    height = (math.sqrt(3) / 2) * side_length
    return [(x1, y2), (x2, y2), ((x1 + x2) / 2, y2 - height)]

# function to calculate right triangle points
def calculate_right_triangle(x1, y1, x2, y2):
    return [(x1, y1), (x1, y2), (x2, y2)]

# function to calculate rhombus points
def calculate_rhombus(x1, y1, x2, y2):
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    dx, dy = abs(x2 - x1) // 2, abs(y2 - y1) // 2
    return [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key in colors:
                picked_color = colors[event.key]
            
            #assigning tools to keys
            tools = {
                pygame.K_l: 'line',
                pygame.K_r: 'rectangle',
                pygame.K_e: 'eraser',
                pygame.K_c: 'circle',
                pygame.K_s: 'square',
                pygame.K_y: 'right triangle',
                pygame.K_t: 'equilateral triangle',
                pygame.K_h: 'rhombus',
                pygame.K_b: 'brush'
            }
            if event.key in tools:
                current_tool = tools[event.key]
            
            # thickness
            if event.key == pygame.K_EQUALS:
                THICKNESS = min(50, THICKNESS + 1)
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)
        
        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMB_pressed = True
            prev_x, prev_y = event.pos
            curr_x, curr_y = event.pos  # initialize current position
        
        # mouse movement
        if event.type == pygame.MOUSEMOTION and LMB_pressed:
            curr_x, curr_y = event.pos
            screen.blit(base_layer, (0, 0))  # clear the screen

            # draw whatever is needed inckuding the picked color, shape(tool), and thickness
            if current_tool == 'rectangle':
                pygame.draw.rect(screen, picked_color, calculate_rect(prev_x, prev_y, curr_x, curr_y), THICKNESS)
            elif current_tool == 'square':
                pygame.draw.rect(screen, picked_color, calculate_square(prev_x, prev_y, curr_x, curr_y), THICKNESS)
            elif current_tool == 'circle':
                radius = int(math.hypot(curr_x - prev_x, curr_y - prev_y))
                pygame.draw.circle(screen, picked_color, (prev_x, prev_y), radius, THICKNESS)
            elif current_tool == 'equilateral triangle':
                pygame.draw.polygon(screen, picked_color, calculate_eq_triangle(prev_x, prev_y, curr_x, curr_y), THICKNESS)
            elif current_tool == 'right triangle':
                pygame.draw.polygon(screen, picked_color, calculate_right_triangle(prev_x, prev_y, curr_x, curr_y), THICKNESS)
            elif current_tool == 'rhombus':
                pygame.draw.polygon(screen, picked_color, calculate_rhombus(prev_x, prev_y, curr_x, curr_y), THICKNESS)
            elif current_tool == 'brush':
                pygame.draw.line(screen, picked_color, (prev_x, prev_y), (curr_x, curr_y), THICKNESS)
                pygame.draw.line(base_layer, picked_color, (prev_x, prev_y), (curr_x, curr_y), THICKNESS)
                prev_x, prev_y = curr_x, curr_y
            elif current_tool == 'line':
                pygame.draw.line(screen, picked_color, (prev_x, prev_y), (curr_x, curr_y), THICKNESS)
            elif current_tool == 'eraser':
                pygame.draw.line(screen, color_white, (prev_x, prev_y), (curr_x, curr_y), THICKNESS)
                pygame.draw.line(base_layer, color_white, (prev_x, prev_y), (curr_x, curr_y), THICKNESS)
                prev_x, prev_y = curr_x, curr_y
        
        #  mouse button release
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMB_pressed = False
            if current_tool in ['rectangle', 'square', 'circle', 'equilateral triangle', 'right triangle', 'rhombus', 'line']:
                # save the drawn shape to the base layer
                if current_tool == 'rectangle':
                    pygame.draw.rect(base_layer, picked_color, calculate_rect(prev_x, prev_y, curr_x, curr_y), THICKNESS)
                elif current_tool == 'square':
                    pygame.draw.rect(base_layer, picked_color, calculate_square(prev_x, prev_y, curr_x, curr_y), THICKNESS)
                elif current_tool == 'circle':
                    radius = int(math.hypot(curr_x - prev_x, curr_y - prev_y))
                    pygame.draw.circle(base_layer, picked_color, (prev_x, prev_y), radius, THICKNESS)
                elif current_tool == 'equilateral triangle':
                    pygame.draw.polygon(base_layer, picked_color, calculate_eq_triangle(prev_x, prev_y, curr_x, curr_y), THICKNESS)
                elif current_tool == 'right triangle':
                    pygame.draw.polygon(base_layer, picked_color, calculate_right_triangle(prev_x, prev_y, curr_x, curr_y), THICKNESS)
                elif current_tool == 'rhombus':
                    pygame.draw.polygon(base_layer, picked_color, calculate_rhombus(prev_x, prev_y, curr_x, curr_y), THICKNESS)
                elif current_tool == 'line':
                    pygame.draw.line(base_layer, picked_color, (prev_x, prev_y), (curr_x, curr_y), THICKNESS)
            screen.blit(base_layer, (0, 0))
    
    # drawing color palette on screen
    pygame.draw.rect(screen, color_black, (20, 10, 20, 20))
    pygame.draw.rect(screen, color_red, (50, 10, 20, 20))
    pygame.draw.rect(screen, color_blue, (80, 10, 20, 20))
    pygame.draw.rect(screen, color_yellow, (110, 10, 20, 20))

    # display current tool and thickness
    font = pygame.font.SysFont(None, 24)
    tool_text = font.render(f"Tool: {current_tool}", True, color_black)
    thickness_text = font.render(f"Thickness: {THICKNESS}", True, color_black)
    screen.blit(tool_text, (20, 40))
    screen.blit(thickness_text, (20, 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()