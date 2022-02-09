#author : Samuel Malec
#######################
#
#
#
#
#
#
########################
import random
import os
import pygame
import sys
pygame.init()
pygame.font.init()
FPS = 60
WIDTH = 864
HEIGHT = 768
BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
PIPE_GAP = 150
PIPE_DELAY = 1000 #v milisekundach
my_font = pygame.font.SysFont("comicsans",50)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
#putting in the pictures
background = pygame.transform.scale(pygame.image.load("bg.png"),(864,768))
bir1 = pygame.image.load("bird1.png")
bir2 = pygame.image.load("bird2.png")
bir3 = pygame.image.load("bird3.png")
ground = pygame.image.load("ground.png")
pipe_img = pygame.image.load("pipe.png")
again = pygame.transform.scale(pygame.image.load("restart.png"),(180,80))
pygame.display.set_icon(pygame.transform.scale(bir1,(50,20)))
again_rect = pygame.Rect(WIDTH//2-214//2 +15,HEIGHT//2,180,80)
timer = pygame.time.Clock()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Bird():
    def __init__(self, x, y,img):
        self.x = x
        self.y = y
        self.vel = 0
        self.img = img
        self.count = 0
        self.rect = pygame.Rect(self.x,self.y,self.img.get_width(),self.img.get_height())

    def rect_update(self):
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def check_height(self):
        if self.y < 568:
            return True
        return False
    def move(self):
        if self.y < 568:
            self.y += self.vel
            self.vel += 0.5
        self.rect_update()
    def draw_dead(self):
        self.img = pygame.transform.rotate(bir1, 180)
        screen.blit(self.img,(self.x,self.y))
    def draw(self):
        if self.y<568:
            if self.count < 10:
                self.img = bir1
            elif self.count < 20:
                self.img = bir2
            elif self.count < 30:
                self.img = bir3
            else:
                self.count = 0
            self.img = pygame.transform.rotate(self.img,-2*self.vel)
            screen.blit(self.img, (self.x, self.y))
            self.count += 1
        else:
            self.draw_dead()
    def tap(self):
            self.vel = -8

class Pipe():
    def __init__(self,x,y,orient):
        self.x = x
        self.img = pipe_img
        self.y = y
        self.pipe_vel = pipe_vel
        self.orient = orient

        if self.orient == 1:
            self.img = pygame.transform.flip(self.img, False, True)
            self.y = self.y - self.img.get_height() - PIPE_GAP // 2
        if self.orient == -1:
            self.y += PIPE_GAP // 2
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def rect_update(self):
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def move(self):
        self.x -= self.pipe_vel
        self.rect_update()
    def collide(self):
        if self.rect.colliderect(bird.rect):
            return True
        return False

    def draw(self):
        screen.blit(self.img,(self.x,self.y))


    def out(self):
        if self.x<0:
            return True
        return False


def initialize():
    global started,run,x_ground,bird,flying,speed_ground,pipes,last_pipe,lost,pipe_vel,skore
    started = False
    run = True
    x_ground = 0
    bird = Bird(100, HEIGHT//2 -100 ,bir1)
    flying = True
    speed_ground = 5
    pipes = []
    last_pipe = 0
    lost = False
    pipe_vel = 5
    skore = 0



def draw_screen():
    global x_ground,speed_ground,flying
    screen.blit(background,(0,0))
    #after background we need to blit the pipes
    for pipe in pipes[:]:
        if flying==True:
            pipe.move()
        pipe.draw()

    # if we start we want to move the ground to the left, and if we move by more that 36 pixels we want the positon to come to its original place to make it seem like it's moving
    # -----------------------------------------------------------------------------------------------------------
    screen.blit(ground, (x_ground, HEIGHT - 168))
    x_ground -= speed_ground
    if x_ground < -36:
        x_ground = 0

    #-----------------------------------------------------------------------------------------------------------

    #score label
    ltext = my_font.render(f"Skore:{int(skore)}",1,GREEN)
    screen.blit(ltext,(WIDTH//2-100,20))

    if started == False and flying==True:
        text = my_font.render("Left mouseclick to jump",1,BLUE)
        screen.blit(text,(WIDTH//2-200,HEIGHT//2 - 120))

    bird.draw()

    if started == True:
        bird.move()


    # if we hit the ground we stop moving it
    if flying == False and started == False:
        bird.move()
        x_ground = 0
        speed_ground = 0
        text = my_font.render("You lost !",1,RED)
        screen.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-100))
        screen.blit(again,(WIDTH//2-text.get_width()//2 +15,HEIGHT//2))


    pygame.display.update()

#game loop
initialize()

#we can create our one and only instance of class Bird
#by default we give the bird1 image and we will change the image in class methods

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            started = True
            if flying == True:
                bird.tap()
            if flying == False:
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    initialize()


    #we want to check how much time has passed since we last put a pipe on the display. If the time exceeds pipe_delay then we put another one here
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > PIPE_DELAY:
        #we create an instance of pipe class and add it to pipes list
        #the fourth parameter symbolizes the orientation of the pipe so that we dont have to make separate classes for both orientations 1 stands for the upper and -1 for the one down
        y = random.randint(-100,100)
        phorna = Pipe(WIDTH,HEIGHT//2+ y,1)
        pdolna = Pipe(WIDTH,HEIGHT//2+ y,-1)
        pipes.append(phorna)
        pipes.append(pdolna)
        last_pipe = time_now

    if flying==True:
        for pipe in pipes[:]:
            if pipe.collide():
                flying = False
                started = False
            if pipe.out():
                pipes.remove(pipe)
                skore +=0.5

    if bird.check_height()==False:
        flying = False
        started  = False



    draw_screen()
    timer.tick(FPS)


