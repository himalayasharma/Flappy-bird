# Imports
import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports (We import all files in pygame.locals)
pygame.font.init()

# Global Variables for the game
FPS = 32 # Frame refresh rate
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {} # This dictionary will contain all our images that will be blitted on the pygame window
GAME_SOUNDS = {} # This dictionary will contain all our game sounds
PLAYER = 'gallery/sprites/bird3.png' # Path of the bird image
BACKGROUND = 'gallery/sprites/bg.jpg' # Path of our background image
WELCOME_BG = 'gallery/sprites/bg_welcome1.jpg'
PIPE = 'gallery/sprites/pipe2.png' # Path of our pipe image

STAT_FONT = pygame.font.SysFont("calibri", 30)

high_score = 0 # Initialize the high score variable with zero

def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    basex = 0

    # GAME LOOP
    while True:
        for event in pygame.event.get():
            # if user clicks on the CROSS BUTTON or presses the ESCAPE key, CLOSE THE GAME
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit() # Quit pygame window
                sys.exit() # Quit the python program

            # If the user presses the SPACE key, START THE GAME
            elif event.type==KEYDOWN and event.key==K_SPACE:
                return # This exits this welcomeScreen() function and moves onto the mainGame() function 
            else:
                SCREEN.blit(GAME_SPRITES['welcome_background'], (0, 0))    
                #SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                #SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                #SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update() # Until this command is executed none of the images will be visible on the game window
                FPSCLOCK.tick(FPS) # This will restrict the frame rate to 32 FPS (and will not allow the while loop to run insanely fast)


def mainGame(high_score):
    score = 0 # Initialize the score variable with zero
    playerx = int(SCREENWIDTH/5) # x coordinate of bird in starting position
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) # y corrdinate of bird in starting position
    #playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe() # Get the 1st pair of upper and lower pipes
    newPipe2 = getRandomPipe() # Get the 2nd pair of upper and lower pipes

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -5 # Pipes move backward with this velocity

    playerVelY = -15 # As soon as the game starts the bird jumps up with this velocity
    playerMaxVelY = 10 # This is MAX FALLING TERMINAL VELOCITY OF THE BIRD
    playerMinVelY = -8
    playerAccY = 1 # The is the ACCELERATION DUE TO GRAVITY

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    # GAME LOOP
    while True:
        for event in pygame.event.get():
            # if user clicks on the CROSS BUTTON or presses the ESCAPE key, CLOSE THE GAME
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses the SPACE key or UPPER ARROW KEY, START THE GAME
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0: # The the player is within the pygame window
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            if score >= high_score:
                high_score = score
                print(f"Your high score is {high_score}")
            return high_score

        # Check position and increment score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                #GAME_SOUNDS['point'].play()

        text_score = STAT_FONT.render("SCORE: " + str(score), 1, (0, 0, 0))
        text_high_score = STAT_FONT.render("HIGH SCORE: " + str(high_score), 1, (0, 0, 0))

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
    

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        """
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        """
        SCREEN.blit(text_score, (SCREENWIDTH - 10 - text_score.get_width(), 460))
        SCREEN.blit(text_high_score, (SCREENWIDTH - 10 - text_high_score.get_width(), 485))
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):

    bird_mask = pygame.mask.from_surface(GAME_SPRITES['player'])
    top_mask = pygame.mask.from_surface(GAME_SPRITES['pipe'][0])
    bottom_mask = pygame.mask.from_surface(GAME_SPRITES['pipe'][1])

    if playery > GROUNDY - 35  or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    
    """
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    """

    """
     upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]
    """

    # Now we calculate an offset, which tell us how far from each other are these masks.
    top_offset = (round(upperPipes[0]['x'] - playerx), round(upperPipes[0]['y'] - playery))
    bottom_offset = (round(lowerPipes[0]['x'] - playerx), round(lowerPipes[0]['y'] - round(playery)))

    # Now we check if the bird and pipes collide
    b_point = bird_mask.overlap(bottom_mask, bottom_offset) #Tells us the point of collision b/w the bird mask and the bottom pipe
    t_point = bird_mask.overlap(top_mask, top_offset) #Tells us the point of collision b/w the bird mask and the top pipe

    if t_point or b_point:
        GAME_SOUNDS['hit'].play()
        return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height() # We calculate the height of the pipe image. (We can take any of the pipes, upper or lower. Here as an eg we have taken the upper one.)
    offset = SCREENHEIGHT/3.2
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset)) # y2 is the y coordinate of the lower pipe
    pipeX = SCREENWIDTH + 10 # We are placing the x coordinates of the pipes 10 pixels outside the screen
    y1 = pipeHeight - y2 + offset # y1 is the y coordinate of the upper pipe
    pipe = [
        {'x': pipeX, 'y': -y1}, # Upper pipe coordinates in the 1st dictionary
        {'x': pipeX, 'y': y2} # Lower pipe coordinates in the 2nd dictionary
    ]
    return pipe # Return a list of Pipe pair coordinates



if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize the pygame module
    FPSCLOCK = pygame.time.Clock() # Make a clock object to control FPS
    pygame.display.set_caption('For Kanu & Kinshu')

    # Adding a key-value pair containing a tuple of all NUMBER IMAGES
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha() # Adding a key-value pair containing the BASE IMAGE
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), # Adding a key-value pair containing a tuple of UPPER & LOWER PIPES
    pygame.image.load(PIPE).convert_alpha()
    )

    # Adding a key-value pairs containing all game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    # Adding key-value pair containing BACKGROUND IMAGE
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    # Adding key-value pair containing BACKGROUND IMAGE
    GAME_SPRITES['welcome_background'] = pygame.image.load(WELCOME_BG).convert()

    # Addiing key-value pair containing BIRD IMAGE
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # GAME LOOP
    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        high_score = mainGame(high_score) # This is the main game function 