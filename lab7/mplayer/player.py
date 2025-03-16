import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("♫")

background = pygame.image.load("background.jpg") 
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

MUSIC_FOLDER = "music"
music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
current_track = 0

font = pygame.font.SysFont("Courier", 18)
button_font = pygame.font.SysFont("Consolas", 18)  


def draw_text(text, x, y, color = (255, 255, 255)):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def play_music():
    global current_track
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_track]))
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def next_track():
    global current_track
    current_track = (current_track + 1) % len(music_files)
    play_music()

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(music_files)
    play_music()

def toggle_pause():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

button_width = 100
button_height = 50

play_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 100, button_width, button_height)
prev_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, button_width, button_height)
next_rect = pygame.Rect(WIDTH // 2 + 50, HEIGHT - 100, button_width, button_height)

running = True
paused = False

while running:
    screen.blit(background, (0, 0))
    draw_text(f"Playing: {music_files[current_track]}", 20, 20)

    pygame.draw.rect(screen, (50, 50, 50), prev_rect)
    pygame.draw.rect(screen, (50, 50, 50), play_rect)
    pygame.draw.rect(screen, (50, 50, 50), next_rect)

    screen.blit(button_font.render("Previous", True, (255, 255, 255)), (prev_rect.x + 15, prev_rect.y + 15))
    screen.blit(button_font.render("Play/Pause", True, (255, 255, 255)), (play_rect.x + 10, play_rect.y + 15))
    screen.blit(button_font.render("Next", True, (255, 255, 255)), (next_rect.x + 30, next_rect.y + 15))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                toggle_pause()
                paused = not paused
            elif prev_rect.collidepoint(event.pos):
                prev_track()
            elif next_rect.collidepoint(event.pos):
                next_track()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_pause()
                paused = not paused
            elif event.key == pygame.K_LEFT:
                prev_track()
            elif event.key == pygame.K_RIGHT:
                next_track()

pygame.quit()
