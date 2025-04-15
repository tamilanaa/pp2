import pygame as pg 
from random import randint, randrange, choice
from rarara import init_db, get_or_create_user, save_game

pg.init() 

# game variables
w, h, fps, level, step = 800, 800, 10, 0, 40 
screen = pg.display.set_mode((w, h))
isRunning, lose = True, False 
clock = pg.time.Clock() 
score = pg.font.SysFont("Verdana", 20) 
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
    def __init__(self, is_temporary=False):
        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)
        self.weight = 3 if is_temporary else choice([1, 2])
        self.is_temporary = is_temporary
        self.image = goldenapple_img if is_temporary else apple_img 
        self.timer = 30 if is_temporary else None

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        if self.is_temporary and self.timer:
            self.timer -= 1
            if self.timer <= 0:
                return False
        return True

    def draw2(self):
        self.x = randrange(0, w, step)
        self.y = randrange(0, h, step)

class Snake:
    def __init__(self):
        self.speed = step
        self.body = [[360, 360]]
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.color = (25, 51, 0)

    def move(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
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

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]

        self.body[0][0] += self.dx
        self.body[0][1] += self.dy

    def draw(self):
        for part in self.body:
            pg.draw.rect(screen, self.color, (part[0], part[1], step, step))

    def collideFood(self, food_list):
        for food in food_list[:]:
            if self.body[0][0] == food.x and self.body[0][1] == food.y:
                self.score += food.weight
                self.body.append([1000, 1000])
                food_list.remove(food)

    def selfCollide(self):
        global isRunning, lose
        if self.body[0] in self.body[1:]:
            isRunning = False
            lose = True

    def checkFood(self, food_list):
        for food in food_list:
            if [food.x, food.y] in self.body:
                food.draw2()

    def collideWall(self, walls):
        global isRunning, lose
        for wall in walls:
            if self.body[0][0] == wall.x and self.body[0][1] == wall.y:
                isRunning = False
                lose = True

class Wall:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pic = pg.image.load("wall.png") 
        self.pic = pg.transform.scale(self.pic, (step, step))

    def draw(self):
        screen.blit(self.pic, (self.x, self.y))

# Initialize DB and user
init_db()
username, level = get_or_create_user()

# Game objects
s = Snake()
foods = [Food(), Food(is_temporary=True)]
level_up_done = False

# Game loop
while isRunning:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            isRunning = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                save_game(username, s.score, level)
                print("paused. click on any button to continue.")
                paused = True
                while paused:
                    for e in pg.event.get():
                        if e.type == pg.KEYDOWN:
                            paused = False

    screen.blit(background, (0, 0))

#срзпаняет уровни
    if s.score >= (level + 1) * 5 and not level_up_done:
        level += 1
        if level > 2:
            level = 0
            fps = 10
        else:
            fps += 2
        foods = [Food(), Food(is_temporary=True)]
        level_up_done = True
        save_game(username, s.score, level)
    elif s.score < (level + 1) * 5:
        level_up_done = False

    # Load walls
    walls = []
    myWalls = open(f'wall{level}.txt', 'r').readlines()
    for i, line in enumerate(myWalls):
        for j, each in enumerate(line):
            if each == "+":
                walls.append(Wall(j * step, i * step))  

    # Update food
    for food in foods[:]:
        if not food.update():
            foods.remove(food)
        else:
            food.draw()

    if len(foods) < 2:
        foods.append(Food(is_temporary=choice([True, False])))

    s.draw()
    s.move(events)
    s.collideFood(foods)
    s.selfCollide()
    s.checkFood(foods)
    s.collideWall(walls)

    counter = score.render(f'Score - {s.score}', True, 'white')
    screen.blit(counter, (550, 50))

    for wall in walls:
        wall.draw()
    
    pg.display.flip()

# Game over
screen.blit(gameover, (w//2 - gameover.get_width()//2, h//2 - gameover.get_height()//2))
pg.display.flip()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
