import pygame as pg
import random
pg.init()

#window settings
w, h, fps = 400, 600, 60 
is_running, lose = True, False 
screen = pg.display.set_mode((w, h))
pg.display.set_caption('racer')
clock = pg.time.Clock()

#background animation variables
y = 0  # vertical position of the background
ry = 2  #speed at which the background scrolls

# Game parameters
step, enemy_step, score, score_coin = 5, 5, 0, 0 
coins_needed_for_speed_increase = 5  # increase enemy speed after collecting this many coins
speed_increment = 1  #how much enemy speed increases

#images and fonts
game_over = pg.image.load("gameover.jpg")
bg = pg.image.load("track.png")
game_over = pg.transform.scale(game_over, (w, h))
score_font = pg.font.SysFont("Verdana", 20)
score_coins = pg.font.SysFont("Verdana", 20)


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, w - 40), 0)

    def update(self):
        global score, enemy_step
        self.rect.move_ip(0, enemy_step)  # Move the enemy car downward
        if self.rect.bottom > h + 90:
            score += 1  # Increase score for avoiding the enemy
            self.rect.center = (random.randint(30, 350), 0)  # Reset position

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self): #keys for movement of the player's car
        pressed_keys = pg.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pg.K_a]:
            self.rect.move_ip(-step, 0)
        if self.rect.right < w and pressed_keys[pg.K_d]:
            self.rect.move_ip(step, 0)
        if self.rect.top > 0 and pressed_keys[pg.K_w]:
            self.rect.move_ip(0, -step)
        if self.rect.bottom < h and pressed_keys[pg.K_s]:
            self.rect.move_ip(0, step)

    def draw(self, surface):
        surface.blit(self.image, self.rect) #draw the sptire (lpayer)


class Coin(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("coin.png")
        self.weight = random.choice([20, 40, 60])  #assign random weights to coins
        size = self.weight  #set size based on weight
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, w - 30), random.randint(30, h - 130))

    def draw(self):
        screen.blit(self.image, self.rect)


# game objects (player and enemy)
p = Player()
e = Enemy()

#sprite groups to manage collisions
enemies = pg.sprite.Group()
enemies.add(e)
coins = pg.sprite.Group()
coins.add(Coin())  #start with one coin

while is_running:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

    #Background animation
    screen.blit(pg.transform.scale(bg, (w, h)), (0, y % h))
    screen.blit(pg.transform.scale(bg, (w, h)), (0, -h + (y % h))) #bckg moves up
    y += ry #move bckg on so pixels per framerate

    #update game objects
    p.update()
    e.update()

    #check for collision between player and enemy
    if pg.sprite.spritecollideany(p, enemies):
        lose = True  #loose if collides

    for c in coins:
        c.draw()
        if pg.sprite.collide_rect(p, c):  #check if player collides -> collects the coin
            score_coin += c.weight // 10  #add score based on coin weight
            c.kill()  #remove collected coin from the screen
            coins.add(Coin())  #add a new randomly generated coin

    #increase enemy speed if player collects enough coins
    if score_coin >= coins_needed_for_speed_increase:
        enemy_step += speed_increment  #increase enemy speed
        coins_needed_for_speed_increase += 5  #next increase needs more coins

    #draw enemy and player on the screen
    e.draw(screen)
    p.draw(screen)

    #if looses:
    while lose:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        screen.blit(game_over, (0, 0)) #display the gameover
        pg.display.flip()

    #display coin score
    counter = score_coins.render(f'Coins: {score_coin}', True, 'white')
    screen.blit(counter, (300, 10))

    pg.display.flip() 

pg.quit()