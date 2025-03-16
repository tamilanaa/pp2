import pygame
import time

pygame.init()
 
screen = pygame.display.set_mode((800, 600)) 
CENTER = (800 // 2, 600 // 2)  

pygame.display.set_caption("Clock :)") 

background = pygame.image.load("clock.png")  
minute_hand = pygame.image.load("rhand.png") 
second_hand = pygame.image.load("lhand.png")   

background = pygame.transform.scale(background, (800, 600))
minute_hand = pygame.transform.scale(minute_hand, (250, 300))  
second_hand = pygame.transform.scale(second_hand, (250, 350))  


def rotate_hand(image, angle, pivot):

    rotated_image = pygame.transform.rotate(image, angle)  
    rect = rotated_image.get_rect(center = pivot)  

    return rotated_image, rect 


running = True
while running:
    screen.fill((255, 255, 255))  
    screen.blit(background, (0, 0))  

    current_time = time.localtime()
    minutes = current_time.tm_min 
    seconds = current_time.tm_sec  

    minute_angle = - (minutes * 6)  
    second_angle = - (seconds * 6)  

    rotated_minute, min_rect = rotate_hand(minute_hand, minute_angle, CENTER)
    rotated_second, sec_rect = rotate_hand(second_hand, second_angle, CENTER)

    screen.blit(rotated_minute, min_rect.topleft)
    screen.blit(rotated_second, sec_rect.topleft)

    pygame.display.update()  


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 