# Version 3
# Changes:
# Redoing everything because I got bored
# Actually coding completely object orientated because I feel like it
# Update, refusing to use global variables was a horrible idea. I'm going back to global variables.
# Changed event.get() to event.pump()
# First created: 24/6/2022
# Last editted: 25/6/2022

# Import all modules
import pygame, sys, random, os

# Constant objects and values
FPS = 60
CLOCK = pygame.time.Clock()
# Initiate screen, in a retro mode
SCREEN = pygame.display.set_mode(flags=pygame.FULLSCREEN,depth=8,vsync=0)
SCREENW, SCREENH = SCREEN.get_width(), SCREEN.get_height()
# Path to this folder
PATH=os.path.dirname(os.path.realpath(__file__))
# Initiate audio
pygame.mixer.pre_init(44100, 8, 1, 4096)
pygame.mixer.init()
# Preload hit noise
HITNOISE = pygame.mixer.Sound(PATH+'\HitNoise.wav')
# Font size
FONTSIZE = 32

# Player class
class Player(pygame.sprite.Sprite):
    __slots__ = 'img', 'rect', 'vel'

    def __init__(self, img, vel):
        # Construct sprite
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.rect = img.get_rect()
        self.rect.centerx = SCREENW/2; self.rect.centery = SCREENH/2
        self.vel = vel

    def update(self, key):
        ## Movement
        up = key[pygame.K_w] or key[pygame.K_UP]
        left = key[pygame.K_a] or key[pygame.K_LEFT]
        down = key[pygame.K_s] or key[pygame.K_DOWN]
        right = key[pygame.K_d] or key[pygame.K_RIGHT]

        playerMove = pygame.math.Vector2(0,0)
        # Move player in that direction if it is within the game borders
        if up == True and self.rect.top > 0:
            playerMove[1] -= self.vel
        if left == True and self.rect.left > 0:
            playerMove[0] -= self.vel
        if down == True and self.rect.bottom < SCREENH:
            playerMove[1] += self.vel
        if right == True and self.rect.right < SCREENW:
            playerMove[0] += self.vel

        # If player moved at all
        if playerMove != (0,0):
            # Limit player speed to maximum velocity
            playerMove.scale_to_length(self.vel)

            # Move player
            self.rect = self.rect.move(playerMove)

        # Render player
        SCREEN.blit(self.img, self.rect)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    __slots__ = 'img', 'rect', 'vector', 'vel'

    def __init__(self, img, rect, initPos, vector, vel):
        # Initiate sprite
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.rect = rect
        self.rect.x=initPos[0]; self.rect.y=initPos[1]
        self.vector = vector # Direction vector
        self.vel = vel# Velocity to scale direction vector to

    def update(self, projectiles):
        # Collision with other projectiles
        for projectile in projectiles:
            # Projectile can not collide with itself :)
            if projectile != self:
                # Check if the balls collide
                if pygame.sprite.collide_rect(self, projectile) == True:
                    self.vector[0] = -(projectile.rect.x-self.rect.x)
                    self.vector[1] = -(projectile.rect.y-self.rect.y)
                    # Play hit noise
                    HITNOISE.play()
                    break # Do not check for more collisions

        # Check if direction vector is not nowhere
        if self.vector != (0,0):
            # Flip movement when hitting game border
            if self.rect.left < 0:
                self.vector[0] = -self.vector[0]
                self.rect.left = 0

            if self.rect.right > SCREENW:
                self.vector[0] = -self.vector[0]
                self.rect.right = SCREENW

            if self.rect.top < 0:
                self.vector[1] = -self.vector[1]
                self.rect.top = 0

            if self.rect.bottom > SCREENH:
                self.vector[1] = -self.vector[1]
                self.rect.bottom = SCREENH

            # Make sure projectile is travelling at correct speed
            self.vector.scale_to_length(self.vel)

            # Move projectile
            self.rect = self.rect.move(self.vector)

        # Blit projectile
        SCREEN.blit(self.img, self.rect)

def main():
    # Initialise text module first
    pygame.font.init() # you have to call this at the start, if you want to use this module
    comicSans = pygame.font.SysFont('Comic Sans MS', FONTSIZE)

    # Initiate pygame
    pygame.init()

    # Preload projectile image
    projImg = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(open(PATH+'\Bullet.png'))),(FONTSIZE,FONTSIZE))
    projRect = projImg.get_rect()

    # Preload player image
    playerImg = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(open(PATH+'\Player.png'))),(FONTSIZE,FONTSIZE))

    # Add a projectile
    projectileGroup = pygame.sprite.Group()
    projectileGroup.add(Projectile(projImg, projRect, (1,1), pygame.math.Vector2(5,5), 10))

    player = Player(playerImg, 10)

    while True:
        # Run this otherwise code stops taking inputs
        pygame.event.pump()

        # Get mouse position in every frame
        mousePos = pygame.mouse.get_pos()

        # Get keys pressed
        key = pygame.key.get_pressed()

        # If escape is pressed, exit game
        if key[pygame.K_ESCAPE]: sys.exit()

        # If spacebar is pressed, add more projectiles
        if key[pygame.K_SPACE]:
            projectileGroup.add(
                Projectile(
                    # Image
                    projImg,
                    # Rect
                    projRect,
                    # Mouse position
                    mousePos,
                    # Random direction
                    pygame.math.Vector2(random.randint(-10,10),random.randint(-10,10)),
                    # Random velocity
                    (random.random()*10) + 4
                )
            )

        # If r is pressed, empty projectileGroup
        if key[pygame.K_r]:
            projectileGroup.empty()

        # Clean screen
        SCREEN.fill('black')

        # Update all projectiles
        projectileGroup.update(projectileGroup.sprites()+[player])

        # Update player
        player.update(key)

        # Print FPS
        txt = comicSans.render(str(round(CLOCK.get_fps())), True, 'white')
        SCREEN.blit(txt, (SCREENW-(2*FONTSIZE),0))

        # Print numProjectiles
        txt = comicSans.render(str(len(projectileGroup.sprites())), True, 'white')
        SCREEN.blit(txt, (SCREENW-(3*FONTSIZE),SCREENH-(1.5*FONTSIZE)))

        # Print controls
        txt = comicSans.render('WASD to move',True,'white')
        SCREEN.blit(txt, (0,0))

        txt = comicSans.render('SPACEBAR to spawn balls',True,'white')
        SCREEN.blit(txt, (0,FONTSIZE))

        txt = comicSans.render('R to reset',True,'white')
        SCREEN.blit(txt, (0,2*FONTSIZE))

        # Update screen
        pygame.display.flip()

        # Run at set FPS
        CLOCK.tick(FPS)

main()