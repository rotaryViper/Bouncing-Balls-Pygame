import pygame
import sys
from random import random
import os
path = os.getenv('LOCALAPPDATA')

# Created 18/6/2022
# Last editted 19/6/2022

# Initialise text module first
pygame.font.init() # you have to call this at the start, if you want to use this module
comicSans = pygame.font.SysFont('Comic Sans MS', 30)

# Initiate audio
pygame.mixer.pre_init(44100, 16, 2, 4096)

pygame.init()

# Constants
FPS = 60
vel = 10
clock = pygame.time.Clock()
velLimit = 6

# Comment out events that are required
# Blocks unnecesary events to improve performance
pygame.event.set_blocked([
    #pygame.QUIT,
    pygame.ACTIVEEVENT,
    pygame.KEYDOWN,
    pygame.KEYUP,
    pygame.MOUSEMOTION,
    #pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
    pygame.JOYAXISMOTION,
    pygame.JOYBALLMOTION,
    pygame.JOYHATMOTION,
    pygame.JOYBUTTONDOWN,
    pygame.JOYBUTTONUP,
    pygame.VIDEORESIZE,
    pygame.VIDEOEXPOSE,
    pygame.USEREVENT
])

# Colours
black = 0, 0, 0
white = 255, 255, 255

# Screen dimensions
screenW, screenH = 1280, 720

# Create screen
screen = pygame.display.set_mode((screenW, screenH),vsync=0)


## Classes
# Preloading ball image
try:
    ballImg = pygame.Surface.convert(pygame.image.load(open(path+'\Discord\\app.ico')))
except:
    ballImg = pygame.Surface.convert(pygame.image.load(open('C:\Windows\Web\\4K\Wallpaper\Windows\img0_1920x1200.jpg')))

class Ball(pygame.sprite.Sprite):
    __slots__ = 'img', 'rect', 'pos', 'velvector', 'vel'

    def __init__(self, img, pos, velvector):
        self.img = pygame.transform.scale(img,(32,32))
        self.rect = self.img.get_rect()
        self.pos = pos
        self.rect.move_ip(pos)
        self.velvector = velvector
        self.vel = (velvector[0]**2+velvector[1]**2)**1/2

    def update(self, ballList):
        # Using a trusty try/except statement to report errors
        try:
            # Initiatize movement
            ballMove = pygame.math.Vector2(0,0)

            # Flip movement when hitting game border
            if self.rect.left < 0:
                self.velvector[0] = -self.velvector[0]
                self.rect.x = 0

            if self.rect.right > screenW:
                self.velvector[0] = -self.velvector[0]
                self.rect.x = screenW - self.rect.width

            if self.rect.top < 0:
                self.velvector[1] = -self.velvector[1]
                self.rect.y = 0

            if self.rect.bottom > screenH:
                self.velvector[1] = -self.velvector[1]
                self.rect.y = screenH - self.rect.height


            # If ball collides with another ball, make them move in different direction
            # False will keep the ball in the ballList, because they should not be destroyed
            
            # Check every ball in the ball list
            for ball in ballList:
                # Ball can not collide with itself :)
                if ball != self:
                    # Check if the balls collide
                    collision = pygame.sprite.collide_circle(self, ball)

                    # If the balls did actually collide
                    if collision == True:
                        self.velvector[0] = -(ball.rect.centerx-self.rect.centerx)
                        self.velvector[1] = -(ball.rect.centery-self.rect.centery)

                else:
                    pass

            # Catch a bug where velocity may become 0, by setting the velocity to some random value
            if self.velvector == [0,0]:
                self.velvector = randVelvector(velLimit)
                #print('Velocity 0 should be fixed now.') # Debugging

            # Make ball move in the same direction, by comparing current location to last direction
            ballMove[0] = self.velvector[0]
            ballMove[1] = self.velvector[1]

            # Limit velvector to original velocity, otherwise the balls will go ballistic after every collision
            ballMove.scale_to_length(self.vel)

            # Move and stamp ball
            self.rect = self.rect.move(ballMove)
            screen.blit(self.img, self.rect)

        # Helpful lines for error debugging
        except Exception as error:
            print(f'Error: {error}')
            ## List of known errors, and fixes
            # velvector may be zero [fixed]


ballList = []
ballList.append(Ball(ballImg, [0,0], [velLimit,velLimit]))

## Functions
def randVelvector(velLimit):
    # Pick random vector
    def randVector(velLimit):
        factor = 0
        # Keep on repeating this code until factor does not equal 0, to the direction the ball travels is random but never stationary
        while factor == 0:
            factor = random()
        return factor * velLimit
    # Find out if the velocity is negative or positive
    def NOrP(num):
        factor = random()
        if factor < 0.5: return -(num)
        else: return num

    return [NOrP(randVector(velLimit)),NOrP(randVector(velLimit))]

# Main code
while True:
    ## Things that are checked in every frame
    # Clean screen with black
    screen.fill((black))
    key = pygame.key.get_pressed()
    # Get mouse position in every frame
    mousePos = pygame.mouse.get_pos()
    spawnBall = False

    # events should use list comprehension, then convert the list in a set
    events = [event.type for event in pygame.event.get()]
    if pygame.QUIT in events: sys.exit()
    if pygame.MOUSEBUTTONDOWN in events: spawnBall = True

    # If player hits space bar, spawn new ball
    if key[pygame.K_SPACE]: spawnBall = True
    if spawnBall == True:ballList.append(Ball(ballImg, list(mousePos), randVelvector(velLimit)))

    # If player hits R, empty the ballList
    if key[pygame.K_r]: ballList = []

    [ball.update(ballList) for ball in ballList]


    # Print mouse cursor location
    mousePosTxt = comicSans.render(str(mousePos), False, white)
    screen.blit(mousePosTxt, (0,0))

    # Print FPS
    FPSTxt = comicSans.render(str(round(clock.get_fps())), False, white)
    screen.blit(FPSTxt, (screenW-50,0))

    # Print number of balls
    BallCountTxt = comicSans.render(str(len(ballList)), False, white)
    screen.blit(BallCountTxt, (screenW-100,screenH-50))

    pygame.display.update()
    # Run at set FPS
    clock.tick(FPS)