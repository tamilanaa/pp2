import pygame as pg 
from random import randint, randrange
pg.init() 

# Game variables
w, h, fps, level, step = 800, 800, 10, 0, 40 
screen = pg.display.set_mode((w, h))
isRunning, lose = True, False 
clock = pg.time.Clock() 
score = pg.font.SysFont("Verdana", 20) #font
surf = pg.Surface((390, 390), pg.SRCALPHA)
background = pg.image.load("back.jpg")
background = pg.transform.scale(background, (w, h))
gameover = pg.image.load("gameover.png")
gameover = pg.transform.scale(gameover, (390, 390)) 

class Food:
    """Class representing the food that the snake eats."""
    def __init__(self):

        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)
        self.pic = pg.image.load("apple.png") 
        self.pic = pg.transform.scale(self.pic, (30, 30))  #resize the apple

    def draw(self):
        # Draw the food
        screen.blit(self.pic, (self.x, self.y))

    def draw2(self):
        #random location for food
        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)

class Snake:
    """Class representing the snake."""
    def __init__(self):
        self.speed = step
        self.body = [[360, 360]]
        self.dx = 0
        self.dy = 0  
        self.score = 0 
        self.color = (25, 51, 0)

    def move(self, events):
        # Handle keyboard events to move the snake
        for event in events:
            if event.type == pg.KEYDOWN:  # Check for key press
                # Control the snake's direction, avoiding moving backward into itself
                if event.key == pg.K_LEFT and self.dx == 0:
                    self.dx = -self.speed
                    self.dy = 0
                if event.key == pg.K_RIGHT and self.dx == 0:
                    self.dx = self.speed
                    self.dy = 0
                if event.key == pg.K_UP and self.dy == 0:
                    self.dx = 0
                    self.dy = -self.speed
                if event.key == pg.K_DOWN and self.dy == 0:
                    self.dx = 0
                    self.dy = self.speed

        # Move the snake's body by shifting each part to the position of the part ahead of it
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

        # Move the snake's head based on the current direction (dx, dy)
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def draw(self):
        #snake's body 
        for part in self.body:
            pg.draw.rect(screen, self.color, (part[0], part[1], step, step))

    def collideFood(self, f: Food):
        #check if the snake's head has collided with the food
        if self.body[0][0] == f.x and self.body[0][1] == f.y:
            self.score += 1
            self.body.append([1000, 1000])  #add a new part to the snake's body

    def selfCollide(self):
        #check if the head has collided with its own body
        global isRunning
        if self.body[0] in self.body[1:]:
            lose = True

    def checkFood(self, f: Food):

        if [f.x, f.y] in self.body:
            f.draw2()  #reposition the apple if it overlaps with the snake

class Wall:

    def __init__(self, x, y):
        self.x, self.y = x, y  # wall's position
        self.pic = pg.image.load("wall.png") 

    def draw(self):
        #draw the wall at its position
        screen.blit(self.pic, (self.x, self.y))


s = Snake()
f = Food()

#main game loop
while isRunning:
    clock.tick(fps)
    events = pg.event.get()  #get events
    for event in events:
        if event.type == pg.QUIT:
            isRunning = False

    screen.blit(background, (0, 0))  #background

    #draw walls based on the current level
    myWalls = open(f'wall{level}.txt', 'r').readlines()  
    walls = []
    for i, line in enumerate(myWalls):
        for j, each in enumerate(line):
            if each == "+":  #walls are "+" in the text file
                walls.append(Wall(j * step, i * step))  

    #call methods to draw and move snake etc
    f.draw()
    s.draw()
    s.move(events)
    s.collideFood(f)
    s.selfCollide()
    s.checkFood(f)

    #show the score on the screen
    counter = score.render(f'Score - {s.score}', True, 'white')
    screen.blit(counter, (550, 50))

    #levelup after collecting 3 food items
    if s.score == 3:
        level += 1
        level %= 4  #back to level 0 after level 3
        fps += 2  # increase game speed
        s.score = 0  #reset score for the new level

    for wall in walls:
        wall.draw()
        if f.x == wall.x and f.y == wall.y:  #not letting the apple to spawn on a wall
            f.draw2()
        if s.body[0][0] == wall.x and s.body[0][1] == wall.y:  #loose if snake hits a wall
            lose = True

    #Game over loop
    while lose:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                isRunning = False
                lose = False   

        surf.blit(gameover, (0, 0))  #Display game over
        screen.blit(surf, (200, 200))
        cntr = score.render(f'Your score is {s.score}', True, 'white')
        screen.blit(cntr, (320, 480))
        l = score.render(f'Your level is {level}', True, 'white')
        screen.blit(l, (320, 510))
        pg.display.flip()

    pg.display.flip()

pg.quit() 
