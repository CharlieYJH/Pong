import pygame
from pygame.locals import *

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle Constants
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 150
PADDLE_PADDING = 15
PADDLE_VELOCITY = 1.4
PADDLE_COLOR = WHITE

# Screen Constants
SCREENWIDTH = 1280
SCREENHEIGHT = 720
BACKGROUNDCOLOR = BLACK

# Ball Constants
BALL_RADIUS = 7
BALL_START_X = int(SCREENWIDTH/2)
BALL_START_Y = int(SCREENHEIGHT/2)
BALL_XVELOCITY = 1.3
BALL_YVELOCITY = 1.3
BALL_COLOR = WHITE

# Score Constants
SCORE_PADDING = 20
SCORE_FONT = "Consolas"
SCORE_SIZE = 36
SCORE_COLOR = WHITE
SCORE_TEXT = " Score "

#---------------------------------------------------------------------
# Game Window
#   - Used to initalize game window
#---------------------------------------------------------------------
class GameWindow():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (width, height)
    
    # Opens up the game window and returns its surface
    def init(self):
        return pygame.display.set_mode(self.size)
        
#---------------------------------------------------------------------
# Paddle    
#   - Contains information about paddle
#---------------------------------------------------------------------  
class Paddle():

    def __init__(self, width, height, x, y, velocity, color):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.x = x
        self.y = y
        self.velocity = velocity
        self.color = color
    
    def updatePosition(self, windowHeight, up, down):
    
        if (up and self.y >= 0):
            self.y -= self.velocity
        elif (down and self.y + self.height <= windowHeight):
            self.y += self.velocity

#---------------------------------------------------------------------
# Ball
#   - Contains information about ball and updates ball position
#---------------------------------------------------------------------         
class Ball():

    def __init__(self, radius, x, y, x_velocity, y_velocity, color):
        self.radius = radius
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.color = color
        self.inPaddle = False
    
    def updatePosition(self, window, paddle1, paddle2):
        
        # Check if ball has hit a paddle
        if ((self.x - self.radius <= paddle1.x + paddle1.width and self.x - self.radius >= paddle1.x + 2 and self.y <= paddle1.y + paddle1.height and self.y >= paddle1.y)
            or (self.x + self.radius >= paddle2.x and self.x + self.radius <= paddle2.x + paddle2.width - 2 and self.y <= paddle2.y + paddle2.height and self.y >= paddle2.y)):

            # Prevents ball from being trapped in the paddles
            if (not ((self.x - self.x_velocity - self.radius <= paddle1.x + paddle1.width and self.x - self.x_velocity - self.radius >= paddle1.x + 2)
                or (self.x - self.x_velocity + self.radius >= paddle2.x and self.x + self.x_velocity + self.radius <= paddle2.x + paddle2.width - 2))):
  
                self.x_velocity *= -1
        
        # Check if ball has hit screen height or top and bottom of paddle
        if (self.y - self.radius <= 0 or self.y + self.radius >= window.height
            or (self.y + self.radius >= paddle1.y
                and self.y + self.radius <= paddle1.y + 5
                and self.x - self.radius <= paddle1.x + paddle1.width - 5
                and self.x - self.radius >= paddle1.x)
            or (self.y - self.radius <= paddle1.y + paddle1.height
                and self.y - self.radius >= paddle1.y + paddle1.height - 5
                and self.x - self.radius <= paddle1.x + paddle1.width - 5
                and self.x - self.radius >= paddle1.x)
            or (self.y + self.radius >= paddle2.y
                and self.y - self.radius <= paddle2.y + 5
                and self.x + self.radius >= paddle2.x + 5
                and self.x + self.radius <= paddle2.x + paddle2.width)
            or (self.y - self.radius <= paddle2.y + paddle2.height
                and self.y - self.radius >= paddle2.y + paddle2.height - 5
                and self.x + self.radius >= paddle2.x + 5
                and self.x + self.radius <= paddle2.x + paddle2.width)):
                
            self.y_velocity *= -1
        
        self.x += self.x_velocity
        self.y += self.y_velocity

#---------------------------------------------------------------------
# Renderer
#   - Used to render out graphics    
#---------------------------------------------------------------------  
class Renderer():
    
    # Draws a rectangle
    def drawRect(Surface, color, position, size):
        pygame.draw.rect(Surface, color, Rect(position, size))
    
    # Draws a circle
    def drawCircle(Surface, color, position, radius):
        pygame.draw.circle(Surface, color, position, radius)
    
    # Writes text
    def writeText(Surface, text, position):
        Surface.blit(text, position)

#---------------------------------------------------------------------
# Player  
#   - Contains information about player and checks player input   
#---------------------------------------------------------------------   
class Player():
    
    def __init__(self, up, down):
        self.upkey = up
        self.downkey = down
        self.up = False
        self.down = False
        self.score = 0
        
    def checkInput(self):
        keys = pygame.key.get_pressed()
        self.up = keys[self.upkey]
        self.down = keys[self.downkey]

#---------------------------------------------------------------------
# MakeText
#   - Used to create text objects
#---------------------------------------------------------------------        
class MakeText():
    
    # Return text object
    def getText(text):
        return pygame.font.SysFont(SCORE_FONT, SCORE_SIZE).render(text, True, SCORE_COLOR)

#---------------------------------------------------------------------
# CheckWin
#   - Used to check win conditions
#---------------------------------------------------------------------  
class CheckWin():
    
    def check(window, ball, player1, player2):
    
        if (ball.x - ball.radius <= 0):
            player2.score += 1
            return True
            
        elif (ball.x + ball.radius >= window.width):
            player1.score += 1
            return True
            
        else:
            return False

#---------------------------------------------------------------------
# Reset
#   - Used to reset round and game
#---------------------------------------------------------------------            
class Reset():
    
    def resetPos(window, paddle1, paddle2, ball):
    
        paddle1.y = window.height/2 - paddle1.height/2
        paddle2.y = window.height/2 - paddle2.height/2
        ball.x = BALL_START_X
        ball.y = BALL_START_Y
        ball.x_velocity = BALL_XVELOCITY
        ball.y_velocity = BALL_YVELOCITY

#---------------------------------------------------------------------
# Update
#   - Updates screen each cycle
#---------------------------------------------------------------------               
class Update():

    def updateScreen(window, paddle1, paddle2, ball, scoreText, score1, score2):
        
        # Rectangles for updating paddle location on screen
        paddle1Box = Rect((0, 0), (paddle1.width + PADDLE_PADDING, window.height))
        paddle2Box = Rect((paddle2.x, 0), (paddle2.width + PADDLE_PADDING, window.height))
        
        # Take into account speed of ball when updating its location on screen
        # Need a larger rectangle to clear ball location if it's moving faster
        effectiveBallRadx = int(abs(ball.radius*ball.x_velocity)) if (int(abs(ball.radius*ball.x_velocity)) >= ball.radius) else ball.radius
        effectiveBallRady = int(abs(ball.radius*ball.y_velocity)) if (int(abs(ball.radius*ball.y_velocity)) >= ball.radius) else ball.radius
        
        # Rectangle for updating ball location on screen
        ballBox = Rect((ball.x - effectiveBallRadx - 4, ball.y - effectiveBallRady - 4), (2*effectiveBallRadx + 6, 2*effectiveBallRady + 6))
        
        # Rectangle for updating score display location on screen
        scoreBox = Rect((window.width//2 - scoreText.get_width()//2 - score1.get_width(), SCORE_PADDING), (score1.get_width() + scoreText.get_width() + score2.get_width(), scoreText.get_height()))
        
        # Update screen
        pygame.display.update([paddle1Box, paddle2Box, ballBox, scoreBox])

#---------------------------------------------------------------------
# Game
#   - Main game engine
#---------------------------------------------------------------------          
class Game():

    # Initialize game objects
    def __init__(self):
        
        # Game window and surface object
        self.window = GameWindow(SCREENWIDTH, SCREENHEIGHT)
        self.gameBox = self.window.init()
        
        # Paddle objects
        self.paddle1 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_PADDING, self.window.height/2 - PADDLE_HEIGHT/2, PADDLE_VELOCITY, PADDLE_COLOR) 
        self.paddle2 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, self.window.width - PADDLE_PADDING - PADDLE_WIDTH, self.window.height/2 - PADDLE_HEIGHT/2, PADDLE_VELOCITY, PADDLE_COLOR)
        
        # Ball object
        self.ball = Ball(BALL_RADIUS, BALL_START_X, BALL_START_Y, BALL_XVELOCITY, BALL_YVELOCITY, BALL_COLOR)
        
        # Player objects
        self.player1 = Player(K_w, K_s)
        self.player2 = Player(K_UP, K_DOWN)
        
    def run(self):
        
        # Check if user has quit the game by closing window
        for event in pygame.event.get():
            if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                return False
        
        # Fill background
        self.gameBox.fill(BACKGROUNDCOLOR)
        
        # Draw paddles and balls
        Renderer.drawRect(self.gameBox, self.paddle1.color, (self.paddle1.x, self.paddle1.y), self.paddle1.size)
        Renderer.drawRect(self.gameBox, self.paddle2.color, (self.paddle2.x, self.paddle2.y), self.paddle2.size)
        Renderer.drawCircle(self.gameBox, self.ball.color, (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        
        # Get text objects for score
        scoreText = MakeText.getText(SCORE_TEXT)
        score1 = MakeText.getText(str(self.player1.score))
        score2 = MakeText.getText(str(self.player2.score))
        
        # Write out text
        Renderer.writeText(self.gameBox, scoreText, (self.window.width//2 - scoreText.get_width()//2, SCORE_PADDING))
        Renderer.writeText(self.gameBox, score1, (self.window.width//2 - scoreText.get_width()//2 - score1.get_width(), SCORE_PADDING))
        Renderer.writeText(self.gameBox, score2, (self.window.width//2 + scoreText.get_width()//2, SCORE_PADDING))
        
        # Check user input
        self.player1.checkInput()
        self.player2.checkInput()
        
        # Check win condition
        win = CheckWin.check(self.window, self.ball, self.player1, self.player2)
        
        if (not win):
            self.paddle1.updatePosition(self.window.height, self.player1.up, self.player1.down)
            self.paddle2.updatePosition(self.window.height, self.player2.up, self.player2.down)
            self.ball.updatePosition(self.window, self.paddle1, self.paddle2)
            
        else:
            Reset.resetPos(self.window, self.paddle1, self.paddle2, self.ball)
        
        # Update only parts needed to speed up runtime
        Update.updateScreen(self.window, self.paddle1, self.paddle2, self.ball, scoreText, score1, score2)
        
        return True

def main():

    pygame.init()
    pongGame = Game()
    
    if (pongGame):
        running = True
    else:
        running = False
    
    while(running):
        running = pongGame.run()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()