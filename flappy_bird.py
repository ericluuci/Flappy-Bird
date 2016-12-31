# Eric Lu

import pygame
from pygame import *
import sys
from random import randint

# Debug Constants
SHOW_HITBOX = False

class GameApp:

    def __init__(self):

        # Sets variables
        self.reset()

        # Creates window and title
        pygame.init()
        self.screen = pygame.display.set_mode((900, 500))
        pygame.display.set_caption('Flappy Bird - Eric Lu')

        # Loads background image
        self.back = pygame.image.load('background.png')

        # Loads bird image   
        self.bird = pygame.image.load('bird.png')
        self.bird = pygame.transform.scale(self.bird,(80, 80))

        # Loads pipe image
        self.pipe_bot = pygame.image.load('pipe.png')
        self.pipe_top = pygame.transform.rotate(self.pipe_bot, 180)

        # Loads music
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.play(-1)

        # Creates a clock
        self.clock = pygame.time.Clock()

    def reset(self):

        self.back_x1 = 0 # Background 1's position
        self.back_x2 = 900 # Background 2's position
        
        self.bird_x = 50 # Bird's X Position (CONSTANT)
        self.bird_y = 175 # Bird's Y Position
        self.bird_angle = 0.0 # Bird's Angle
        self.bird_yvel = 0.0 # Bird's Velocity

        self.pipe_x1 = 400 # Pipe 1's X Position
        self.pipe_y1 = randint(170, 400) # Pipe 1's Y Position
        self.pipe_x2 = 910 # Pipe 2's X Position
        self.pipe_y2 = randint(170, 400) # Pipe 1's Y Position

        self.start = True # Shows Start Menu
        self.points = 0 # Player's Score
        self.hit = False # Whether the bird has been hit

    def renderStart(self):

        self.drawBackground(False)
        
        title_font = pygame.font.SysFont('Cooper Black', 72)
        title1 = title_font.render('Flappy Bird', 1, (255, 255, 0))
        title2 = title_font.render('Flappy Bird', 1, (0, 0, 0))
        self.screen.blit(title2, (243, 103))
        self.screen.blit(title1, (240, 100))

        subtitle_font = pygame.font.SysFont('Cooper Black', 52)
        subtitle1 = subtitle_font.render('Press SPACE to start!', 1, (255, 255, 0))
        subtitle2 = subtitle_font.render('Press SPACE to start!', 1, (0, 0, 0))
        self.screen.blit(subtitle2, (163, 403))
        self.screen.blit(subtitle1, (160, 400))

        self.screen.blit(self.bird,(self.bird_x, self.bird_y))

    def drawBackground(self, end):

        if (end == False):

            # Constantly moves background left
            self.back_x1 -= 4
            self.back_x2 -= 4

            # Resets the background
            if (self.back_x1 < -900):
            
                self.back_x1 = 0
                self.back_x2 = 900

        self.screen.blit(self.back, (self.back_x1, 0))
        self.screen.blit(self.back, (self.back_x2, 0))

    def drawBird(self):

        # Constantly changes the bird's velocity downwards
        self.bird_yvel += 0.3
        self.bird_y += self.bird_yvel

        # Constantly changes the bird's angle
        self.bird_angle -= 1.5

        # Bird's maximum angle
        if (self.bird_angle <= -90):
            self.bird_angle = -90

        bird2 = pygame.transform.rotate(self.bird, self.bird_angle)
        
        self.screen.blit(bird2, (self.bird_x, self.bird_y))

    def drawPipes(self, end):

        if (end == False):

            # Constantly moves the pipes left
            self.pipe_x1 -= 4
            self.pipe_x2 -= 4

            # Generates random heights for the pipe
            if (self.pipe_x1 <= -138):
                self.pipe_y1 = randint(170, 490)
                self.pipe_x1 = 900

            if (self.pipe_x2 <= -138):
                self.pipe_y2 = randint(170, 490)
                self.pipe_x2 = 900

        self.screen.blit(self.pipe_bot, (self.pipe_x1, self.pipe_y1))
        self.screen.blit(self.pipe_top, (self.pipe_x1, self.pipe_y1 - 165 - 793))

        self.screen.blit(self.pipe_bot, (self.pipe_x2, self.pipe_y2))
        self.screen.blit(self.pipe_top, (self.pipe_x2, self.pipe_y2 - 165 - 793))

    def drawPoints(self):

        # Increments points after passing a pipe
        if (self.pipe_x1 + 138 <= 5 or self.pipe_x2 + 138 <= 5):
            self.points += 1

        points_font = pygame.font.SysFont('Cooper Black', 20)
        points1 = points_font.render('Points : ' + str(self.points), 1, (255, 255, 0))
        points2 = points_font.render('Points : ' + str(self.points), 1, (0, 0, 0))
        self.screen.blit(points2, (782, 8))
        self.screen.blit(points1, (780, 6))

    def testCollision(self):

        # Bird's Hitbox
        #(self.bird_x+30, self.bird_y+20) (self.bird_x+80, self.bird_y+20)
        #                     +----------+
        #                     |          |
        #                     |          |
        #                     |          |
        #                     |          |
        #                     |          |
        #                     |          |
        #                     +----------+
        #(self.bird_x+30, self.bird_y+60) (self.bird_x+80, self.bird_y+60)

        # Top Pipe##'s Hitbox
        #(self.pipe_x##, self.pipe_y## - 165 - 793)
        #                           +   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           +---+
        #(self.pipe_x##, self.pipe_y## - 165) (self.pipe_x##+138, self.pipe_y## - 165)
        

        # Bottom Pipe##'s Hitbox
        #(self.pipe_x##, self.pipe_y##) (self.pipe_x##+138, self.pipe_y## )
        #                           +---+
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           |   |
        #                           +   |
        # (self.pipe_x##, self.pipe_y##+793)

        # Show Hitboxes
        if (SHOW_HITBOX):
            
            color =  (255, 255, 0)

            # Bird Hitbox
            pygame.draw.line(self.screen, color, (self.bird_x+30, self.bird_y+20), (self.bird_x+80, self.bird_y+20)) # TL - TR
            pygame.draw.line(self.screen, color, (self.bird_x+30, self.bird_y+60), (self.bird_x+80, self.bird_y+60)) # BL - BR
            pygame.draw.line(self.screen, color, (self.bird_x+80, self.bird_y+20), (self.bird_x+80, self.bird_y+60)) # TR - BR

            # Top Pipe 1 Hitbox
            pygame.draw.line(self.screen, color, (self.pipe_x1, self.pipe_y1-165-793), (self.pipe_x1, self.pipe_y1-165)) # TL - BL
            pygame.draw.line(self.screen, color, (self.pipe_x1, self.pipe_y1-165), (self.pipe_x1+138, self.pipe_y1-165)) # BL - BR

            # Bottom Pipe 1 Hitbox
            pygame.draw.line(self.screen, color, (self.pipe_x1, self.pipe_y1), (self.pipe_x1+138, self.pipe_y1)) # TL - TR
            pygame.draw.line(self.screen, color, (self.pipe_x1, self.pipe_y1), (self.pipe_x1, self.pipe_y1+793)) # TL - BL

            # Top Pipe 2 Hitbox
            pygame.draw.line(self.screen, color, (self.pipe_x2, self.pipe_y2-165-793), (self.pipe_x2, self.pipe_y2-165)) # TL - BL
            pygame.draw.line(self.screen, color, (self.pipe_x2, self.pipe_y2-165), (self.pipe_x2+138, self.pipe_y2-165)) # BL - BR

            # Bottom Pipe 2 Hitbox
            pygame.draw.line(self.screen, color, (self.pipe_x2, self.pipe_y2), (self.pipe_x2+138, self.pipe_y2)) # TL - TR
            pygame.draw.line(self.screen, color, (self.pipe_x2, self.pipe_y2), (self.pipe_x2, self.pipe_y2+793)) # TL - BL

        # Top of the Window
        if (self.bird_y+20 <= 0):
            return True

        # Bottom of the Window
        if (self.bird_y+60 >= 500):
            return True

        # Pipe 1 - Left Side
        if (abs(self.bird_x+80 - self.pipe_x1) <= 2 and
            (self.bird_y+80 >= self.pipe_y1 or self.bird_y+20 <= self.pipe_y1 - 165)):
            return True

        # Pipe 1 - Up/Down Side
        if ((self.bird_x+80 >= self.pipe_x1 and self.bird_x+80 <= self.pipe_x1+138) or (self.bird_x+30 >= self.pipe_x1 and self.bird_x+30 <= self.pipe_x1+138)):

            # Up Side
            if (self.bird_y+20 <= self.pipe_y1 - 165):
                return True
            # Down Side
            if (self.bird_y+60  >= self.pipe_y1):
                return True

        # Pipe 2 - Left Side
        if (abs(self.bird_x+80 - self.pipe_x2) <= 2 and
            (self.bird_y+80 >= self.pipe_y2 or self.bird_y+20 <= self.pipe_y2 - 165)):
            return True

        # Pipe 2 - Up/Down Side
        if ((self.bird_x+80 >= self.pipe_x2 and self.bird_x+80 <= self.pipe_x2+138) or (self.bird_x+30 >= self.pipe_x2 and self.bird_x+30 <= self.pipe_x2+138)):

            # Up Side
            if (self.bird_y+20 <= self.pipe_y2 - 165):
                return True
            # Down Side
            if (self.bird_y+60  >= self.pipe_y2):
                return True

    def renderMid(self):

        self.drawBackground(False)
        self.drawPipes(False)
        self.drawBird()
        self.drawPoints()
        self.hit = self.testCollision()

    def drawEndGame(self):

        game_over_font = pygame.font.SysFont('Cooper Black', 52)
        game_over1 = game_over_font.render('GAME OVER!', 1, (255, 255, 0))
        game_over2 = game_over_font.render('GAME OVER!', 1, (0, 0, 0))
        self.screen.blit(game_over2, (263, 173))
        self.screen.blit(game_over1, (260, 170))

        reset_font = pygame.font.SysFont('Cooper Black', 52)
        reset1 = reset_font.render("Press SPACE to start!", 1, (255, 255, 0))
        reset2 = reset_font.render("Press SPACE to start!", 1, (0, 0, 0))
        self.screen.blit(reset2, (163, 403))
        self.screen.blit(reset1, (160, 400))

    def renderEnd(self):

        self.drawBackground(True)
        self.drawPipes(True)
        self.drawBird()
        self.drawPoints()
        self.drawEndGame()
        
    def mainloop(self):

        while True:
            
            self.clock.tick(60)

            for event in pygame.event.get():

                pressed = pygame.key.get_pressed()

                if (event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]):
                    pygame.quit()
                    sys.exit()
                    
                # Resets the game
                if (self.hit == True and pressed[pygame.K_SPACE]):
                    self.reset()

                if (self.hit != True):
                
                    # Start menu
                    if (self.start == True and pressed[pygame.K_SPACE]):
                        self.start = False

                    # The bird flies upward
                    if (self.start == False and (pressed[pygame.K_SPACE] or pressed [pygame.K_w] or pressed[pygame.K_UP])):
                        self.bird_yvel = -7
                        self.bird_angle = 45
                
            if (self.start):
                self.renderStart()
            elif (self.hit):
                self.renderEnd()
            else:
                self.renderMid()

            pygame.display.update()
            
if __name__ == '__main__':
    GameApp().mainloop()
