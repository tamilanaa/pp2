import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    draw_mode = "line"
    points = []
    shapes = []  

    line_button = pygame.Rect(10, 10, 80, 40)
    circle_button = pygame.Rect(100, 10, 80, 40)
    rect_button = pygame.Rect(190, 10, 80, 40)
    eraser_button = pygame.Rect(280, 10, 80, 40)

    red_button = pygame.Rect(400, 10, 40, 40)
    green_button = pygame.Rect(450, 10, 40, 40)
    blue_button = pygame.Rect(500, 10, 40, 40)
    black_button = pygame.Rect(550, 10, 40, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if line_button.collidepoint(event.pos):
                    draw_mode = "line"
                elif circle_button.collidepoint(event.pos):
                    draw_mode = "circle"
                elif rect_button.collidepoint(event.pos):
                    draw_mode = "rectangle"
                elif eraser_button.collidepoint(event.pos):
                    draw_mode = "eraser"

                elif red_button.collidepoint(event.pos):
                    mode = 'red'
                elif green_button.collidepoint(event.pos):
                    mode = 'green'
                elif blue_button.collidepoint(event.pos):
                    mode = 'blue'
                elif black_button.collidepoint(event.pos):
                    mode = 'black'

                elif event.pos[1] > 60 and draw_mode in ["circle", "rectangle"]:
                    shapes.append((draw_mode, mode, event.pos))


            if event.type == pygame.MOUSEMOTION and event.buttons[0] and event.pos[1] > 60:
                points.append((event.pos, mode if draw_mode == "line" else 'white'))

 
        screen.fill((255, 255, 255))

        draw_button(screen, line_button, "Line", draw_mode == "line")
        draw_button(screen, circle_button, "Circle", draw_mode == "circle")
        draw_button(screen, rect_button, "Rect", draw_mode == "rectangle")
        draw_button(screen, eraser_button, "Eraser", draw_mode == "eraser")

        pygame.draw.rect(screen, (204, 0, 0), red_button)
        pygame.draw.rect(screen, (76, 153, 0), green_button)
        pygame.draw.rect(screen, (0, 102, 205), blue_button)
        pygame.draw.rect(screen, (0, 0, 0), black_button)


        for shape, color, pos in shapes:
            if shape == "circle":
                pygame.draw.circle(screen, color_picker(color), pos, 30, 2)
            elif shape == "rectangle":
                pygame.draw.rect(screen, color_picker(color), (pos[0] - 30, pos[1] - 20, 60, 40), 2)

        for pos, color_mode in points:
            pygame.draw.circle(screen, color_picker(color_mode), pos, radius)

        pygame.display.flip()
        clock.tick(60)


def draw_button(screen, rect, text, active):
    color = (200, 200, 200) if active else (150, 150, 150)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    font = pygame.font.Font(None, 24)
    text_surf = font.render(text, True, (0, 0, 0))
    screen.blit(text_surf, (rect.x + 10, rect.y + 10))


def color_picker(color_mode):
    colors = {'blue': (0, 102, 205), 'red': (204, 0, 0), 'green': (76, 153, 0), 'black': (0, 0, 0)}
    return colors.get(color_mode, (255, 255, 255))


main()
