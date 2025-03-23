import pygame as pg
import random, time
pg.init()

# Window settings
w, h, fps = 400, 600, 60 
is_running, lose = True, False 
screen = pg.display.set_mode((w, h))
pg.display.set_caption('racer')
clock = pg.time.Clock()

#background animation variables
y = 0  #vertical position of the background
ry = 2  #speed at which the background scrolls

#game parameters
step, enemy_step, score, score_coin = 5, 5, 0, 0 

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
        self.rect = self.image.get_rect()  #the rectangle representing the enemy car
        self.rect.center = (random.randint(40, w - 40), 0)  #random initial position

    def update(self):
        global score
        self.rect.move_ip(0, enemy_step)  #move the enemy car downwards
        if self.rect.bottom > h + 90:  #uf the enemy moves off-screen, reset its position
            score += 1  # +score for avoiding the enemy
            self.top = 0
            self.rect.center = (random.randint(30, 350), 0)  #reset enemy to the top with a random horizontal position

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("Player.png")
        self.rect = self.image.get_rect() 
        self.rect.center = (160, 520)

    def update(self):  #кнопки для перемещения машины игрока
        pressed_keys = pg.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pg.K_a]:  #move left if not at the left edge
            self.rect.move_ip(-step, 0)
        if self.rect.right < w and pressed_keys[pg.K_d]:  #right
            self.rect.move_ip(step, 0)
        if self.rect.top > 0 and pressed_keys[pg.K_w]:  #up
            self.rect.move_ip(0, -step)
        if self.rect.bottom < h and pressed_keys[pg.K_s]:  #down
            self.rect.move_ip(0, step)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Coin(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("coin.png") 
        self.image = pg.transform.scale(self.image, (50, 50))  #resize the coin
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, w - 30), random.randint(30, h - 130))

    def draw(self):
        screen.blit(self.image, self.rect)

#game objects
p = Player()
e = Enemy()
c = Coin()  

# sprite groups to manage collisions
enemies = pg.sprite.Group()
enemies.add(e)

coins = pg.sprite.Group()
coins.add(c)


while is_running:
    clock.tick(fps) 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

    #background animation
    screen.blit(pg.transform.scale(bg, (w, h)), (0, y % h))  #draw scrolling background
    screen.blit(pg.transform.scale(bg, (w, h)), (0, -h + (y % h)))
    y += ry 

    #update and draw game objects
    p.update()
    e.update()

    #check for collision between player and enemy
    if pg.sprite.spritecollideany(p, enemies):
        lose = True  #game over if player collides with enemy


    for c in coins:
        c.draw()
        if pg.sprite.collide_rect(p, c):  #check for collision with coin
            c.kill()  #remove coin 
            score_coin += 1  #+score
            new = Coin()  #new coin
            coins.add(new)


    e.draw(screen)
    p.draw(screen)


    while lose:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        screen.blit(game_over, (0, 0))
        pg.display.flip()

    # display score
    counter = score_coins.render(f'Coins: {score_coin}', True, 'white')
    screen.blit(counter, (300, 10))

    pg.display.flip()  # Update the display

pg.quit() 