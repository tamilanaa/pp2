import pygame as pg 
from random import randint, randrange, choice
pg.init() 

# game variables
w, h, fps, level, step = 800, 800, 10, 0, 40 
screen = pg.display.set_mode((w, h))
isRunning, lose = True, False 
clock = pg.time.Clock() 
score = pg.font.SysFont("Verdana", 20) #font for score display
surf = pg.Surface((390, 390), pg.SRCALPHA)
background = pg.image.load("back.jpg")
background = pg.transform.scale(background, (w, h))
gameover = pg.image.load("gameover.png")
gameover = pg.transform.scale(gameover, (390, 390)) 
apple_img = pg.image.load("apple.png") 
apple_img = pg.transform.scale(apple_img, (30, 30))
goldenapple_img = pg.image.load("goldenapple.png") 
goldenapple_img = pg.transform.scale(goldenapple_img, (30, 30))

class Food:
    """food that snake eats"""
    def __init__(self, is_temporary=False):
        self.x = randrange(0, w, step) # random x position
        self.y = randrange(0, h, step) # random y position
        self.weight = 3 if is_temporary else choice([1, 2]) # golden apple gives 3 points
        self.is_temporary = is_temporary # is it golden apple
        self.image = goldenapple_img if is_temporary else apple_img 
        self.timer = 30 if is_temporary else None # timer for golden apple

    def draw(self):
        # draw food on screen
        screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        # update golden apple timer
        if self.is_temporary and self.timer:
            self.timer -= 1
            if self.timer <= 0:
                return False # remove expired golden apple
        return True

    def draw2(self):
        # move food to new random position
        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)

class Snake:
    """the snake player controls"""
    def __init__(self):
        self.speed = step # moves one step at a time
        self.body = [[360, 360]] # starting position
        self.dx = 0 # x direction
        self.dy = 0 # y direction
        self.score = 0 # player score
        self.color = (25, 51, 0) # snake color

    def move(self, events):
        # handle keyboard input
        for event in events:
            if event.type == pg.KEYDOWN:
                # change direction based on key pressed
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

        # move body segments
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

        # move head
        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def draw(self):
        # draw snake on screen
        for part in self.body:
            pg.draw.rect(screen, self.color, (part[0], part[1], step, step))

    def collideFood(self, food_list):
        # check if snake ate food
        for food in food_list[:]:
            if self.body[0][0] == food.x and self.body[0][1] == food.y:
                self.score += food.weight # add points
                self.body.append([1000, 1000]) # grow snake
                food_list.remove(food) # remove eaten food

    def selfCollide(self):
        # check if snake hit itself
        global isRunning, lose
        if self.body[0] in self.body[1:]:
            isRunning = False
            lose = True

    def checkFood(self, food_list):
        # check if food spawned inside snake
        for food in food_list:
            if [food.x, food.y] in self.body:
                food.draw2() # move food to new position

    def collideWall(self, walls):
        # check if snake hit wall
        global isRunning, lose
        for wall in walls:
            if self.body[0][0] == wall.x and self.body[0][1] == wall.y:
                isRunning = False
                lose = True

class Wall:
    """walls that block snake"""
    def __init__(self, x, y):
        self.x, self.y = x, y # wall position
        self.pic = pg.image.load("wall.png") 
        self.pic = pg.transform.scale(self.pic, (step, step)) # resize to match snake

    def draw(self):
        # draw wall on screen
        screen.blit(self.pic, (self.x, self.y))

s = Snake()
foods = [Food(), Food(is_temporary=True)] # start with two foods

# main game loop
while isRunning:
    clock.tick(fps) # control game speed
    events = pg.event.get() # get player input
    for event in events:
        if event.type == pg.QUIT:
            isRunning = False

    screen.blit(background, (0, 0)) # draw background

    # level progression
    if s.score >= (level + 1) * 5: # level up every 5 points
        level += 1
        if level > 2: # if passed level 2
            level = 0 # return to level 0
            fps = 10 # reset speed
        else:
            fps += 2 # increase speed
        foods = [Food(), Food(is_temporary=True)] # refresh food

    # load walls for current level
    myWalls = open(f'wall{level}.txt', 'r').readlines()  
    walls = []
    for i, line in enumerate(myWalls):
        for j, each in enumerate(line):
            if each == "+": # + represents wall
                walls.append(Wall(j * step, i * step))  

    # update and draw food
    for food in foods[:]:
        if not food.update(): # update timers
            foods.remove(food) # remove expired food
        else:
            food.draw() # draw food
    
    # keep 2 foods on screen
    if len(foods) < 2:
        foods.append(Food(is_temporary=choice([True, False])))
    
    # update game state
    s.draw()
    s.move(events)
    s.collideFood(foods)
    s.selfCollide()
    s.checkFood(foods)
    s.collideWall(walls)

    # display score
    counter = score.render(f'Score - {s.score}', True, 'white')
    screen.blit(counter, (550, 50))

    # draw walls
    for wall in walls:
        wall.draw()
    
    pg.display.flip() # update screen

# game over screen
screen.blit(gameover, (w//2 - gameover.get_width()//2, h//2 - gameover.get_height()//2))
pg.display.flip()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()