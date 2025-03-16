import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
RADIUS = 25
VEL = 20 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball")

x, y = WIDTH // 2, HEIGHT // 2 

running = True
while running:
    pygame.time.delay(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x - RADIUS - VEL >= 0:
        x -= VEL
    if keys[pygame.K_RIGHT] and x + RADIUS + VEL <= WIDTH:
        x += VEL
    if keys[pygame.K_UP] and y - RADIUS - VEL >= 0:
        y -= VEL
    if keys[pygame.K_DOWN] and y + RADIUS + VEL <= HEIGHT:
        y += VEL
    
    screen.fill((255, 255, 255))  
    pygame.draw.circle(screen, (255, 0, 0), (x, y), RADIUS) 
    pygame.display.update()
    
pygame.quit()
