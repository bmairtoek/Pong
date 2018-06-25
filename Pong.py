import pygame
from pygame.locals import *
from random import choice, randint
from math import sin, cos, atan, degrees, radians
from ast import literal_eval as make_tuple
from tkinter import *

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 120

# Global Variables to be used through our program
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
LINETHICKNESS = 8
PADDLESIZE = 50
PADDLEOFFSET = 70
PADDLETHICKNESS = 8
BALLSIZE = 8
root = None
MODE = 0

# Set up the colours
BGCOLOUR = (0, 0, 0)
FGCOLOUR = (255, 255, 255)

# float coordinates of the ball
floatBallX = 0.0
floatBallY = 0.0

# speed of the ball
speed = 6

# difficulty of AI
difficulty = 1


# ends game
def gameQuit():
    pygame.quit()
    sys.exit()


# Draws the arena the game will be played in.
def drawArena():
    DISPLAYSURF.fill(BGCOLOUR)
    # Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, FGCOLOUR, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS * 2)
    # Draw centre line
    pygame.draw.line(DISPLAYSURF, FGCOLOUR, ((WINDOWWIDTH / 2), 0), ((WINDOWWIDTH / 2), WINDOWHEIGHT),
                     int((LINETHICKNESS / 2)))


# Draws the paddle
def drawPaddle(paddle):
    # Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, FGCOLOUR, paddle)


# draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, FGCOLOUR, ball)


# moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    global floatBallX
    global floatBallY
    floatBallX += ballDirX
    floatBallY += ballDirY
    ball.x = int(floatBallX)
    ball.y = int(floatBallY)
    return ball


# Checks for a collision with a wall, and 'bounces' ball off it.
# Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top <= LINETHICKNESS or ball.bottom >= (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left <= LINETHICKNESS or ball.right >= (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY


# calculates new angle of ball movement in reference to Ox (used only in next function)
def calculateAngle(ball, paddle, ballDirX, ballDirY):
    currentAngle = degrees(atan(ballDirY / abs(ballDirX)))
    deltaAngle = (ball.top + BALLSIZE - paddle.top) / (PADDLESIZE + BALLSIZE) * 90 - 45
    newAngle = currentAngle + deltaAngle
    if newAngle > 50:
        newAngle = 50
    elif newAngle < -50:
        newAngle = -50
    return radians(newAngle)


# Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddleL, paddleR, ballDirX, ballDirY):
    global speed
    if ballDirX < 0 and paddleL.right <= ball.left and paddleL.right > ball.left + ballDirX and paddleL.top < ball.bottom and paddleL.bottom > ball.top:
        newAngle = calculateAngle(ball, paddleL, ballDirX, ballDirY)
        ballDirX = speed * cos(newAngle)
        ballDirY = speed * sin(newAngle)
    elif ballDirX > 0 and paddleR.left >= ball.right and paddleR.left < ball.right + ballDirX and paddleR.top < ball.bottom and paddleR.bottom > ball.top:
        newAngle = calculateAngle(ball, paddleR, ballDirX, ballDirY)
        ballDirX = -speed * cos(newAngle)
        ballDirY = speed * sin(newAngle)
    return ballDirX, ballDirY


# Checks to see if a point has been scored returns new score
def checkPointScored(ball, score):
    # point for left player
    if ball.right >= WINDOWWIDTH - LINETHICKNESS:
        score[0] += 1
    # point for right player
    elif ball.left <= LINETHICKNESS:
        score[1] += 1
    return score


# Artificial Intelligence of computer player
def artificialIntelligence(ball, ballDirX, paddleR):
    global difficulty
    global speed
    # If ball is moving away from paddle, center bat
    if ballDirX < 0:
        if paddleR.centery < (WINDOWHEIGHT / 2):
            paddleR.y += 1 * (difficulty + int(speed/5))
        elif paddleR.centery > (WINDOWHEIGHT / 2):
            paddleR.y -= 1 * (difficulty + int(speed/5))
    # if ball moving towards bat, track its movement.
    elif ballDirX > 0:
        if paddleR.centery < ball.centery:
            paddleR.y += 1 * (difficulty + int(speed/5))
        else:
            paddleR.y -= 1 * (difficulty + int(speed/5))
    return paddleR


# Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Wynik = {0} : {1}'.format(score[0], score[1]), True, FGCOLOUR)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 160 - LINETHICKNESS, 25 + LINETHICKNESS)
    DISPLAYSURF.blit(resultSurf, resultRect)


# method used to override X of message box
def doNothing():
    pass


# changes speed of the ball
def changeSpeed(newSpeed, ballDirX, ballDirY):
    global speed
    ballDirX = ballDirX / speed
    ballDirY = ballDirY / speed
    speed = newSpeed
    ballDirX = ballDirX * speed
    ballDirY = ballDirY * speed
    return ballDirX, ballDirY


# loads data from config file
def loadData():
    global WINDOWWIDTH
    global WINDOWHEIGHT
    global LINETHICKNESS
    global PADDLESIZE
    global PADDLEOFFSET
    global PADDLETHICKNESS
    global BALLSIZE
    global BGCOLOUR
    global FGCOLOUR
    global speed

    try:
        with open('config.txt') as config:
            lines = config.readlines()
            # read each value and check if they are correct
            WINDOWWIDTH_tmp = int(lines[8].split(" ")[2])
            WINDOWHEIGHT_tmp = int(lines[10].split(" ")[2])
            LINETHICKNESS_tmp = int(lines[12].split(" ")[2])
            PADDLESIZE_tmp = int(lines[14].split(" ")[2])
            PADDLEOFFSET_tmp = int(lines[16].split(" ")[2])
            PADDLETHICKNESS_tmp = int(lines[18].split(" ")[2])
            BALLSIZE_tmp = int(lines[20].split(" ")[2])
            speed_tmp = float(lines[22].split(" ")[2])
            BGCOLOUR_tmp = make_tuple(lines[24].split(" ")[2])
            FGCOLOUR_tmp = make_tuple(lines[26].split(" ")[2])
            if WINDOWWIDTH_tmp < 700:
                raise ValueError
            if WINDOWHEIGHT_tmp < 300:
                raise ValueError
            if LINETHICKNESS_tmp <= 0 or PADDLESIZE_tmp <= 0 or PADDLEOFFSET_tmp <= 0 or \
                    PADDLETHICKNESS_tmp <= 0 or BALLSIZE_tmp <= 0 or speed_tmp <= 0:
                raise ValueError
            for i in range(3):
                if BGCOLOUR_tmp[i] < 0 or BGCOLOUR_tmp[i] > 255 or FGCOLOUR_tmp[i] < 0 or FGCOLOUR_tmp[i] > 255:
                    raise ValueError
    except:
        warningBox()
    else:
        WINDOWWIDTH = WINDOWWIDTH_tmp
        WINDOWHEIGHT = WINDOWHEIGHT_tmp
        LINETHICKNESS = LINETHICKNESS_tmp
        PADDLESIZE = PADDLESIZE_tmp
        PADDLEOFFSET = PADDLEOFFSET_tmp
        PADDLETHICKNESS = PADDLETHICKNESS_tmp
        BALLSIZE = BALLSIZE_tmp
        speed = speed_tmp
        BGCOLOUR = BGCOLOUR_tmp
        FGCOLOUR = FGCOLOUR_tmp


# brings back original config file
def backupFile():
    backup = open('./config.txt', 'w')
    backup.write(
        '''#Here you can edit some parameters before game.
#Be wary though not to make mistakes in this file,
#because in case of en error whole file may be
#replaced with the original one (on user demand).
#Remember that spaces should be left where they are.
#Each paramter must be bigger than 0 (except colours).

# width of the main window (min 700)
WINDOWWIDTH = 800
# high of the main window (min 300)
WINDOWHEIGHT = 600
# thickness of the arena line
LINETHICKNESS = 8
# length of paddles
PADDLESIZE = 50
# distance between paddles and edges of the arena
PADDLEOFFSET = 70
# thickness of paddles
PADDLETHICKNESS = 8
# size of the ball
BALLSIZE = 8
# speed at which the games startes (recommended values: 1 - 4)
STARTSPEED = 2
# colour of background
BGCOLOUR = (0,0,0)
# colour of arena elements
FGCOLOUR = (255,255,255)'''
    )
    backup.close()
    global root
    root.destroy()

def set_difficulty(level):
    global difficulty
    global MODE
    global root
    difficulty  = level
    MODE = 0
    root.destroy()


def chooseDifficultyBox():
    global root
    root = Tk()
    root.attributes("-topmost", True)
    root.geometry('%dx%d+%d+%d' % (200, 100, root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2))
    root.protocol('WM_DELETE_WINDOW', doNothing)
    root.resizable(width=False, height=False)
    top = Frame(root)
    bottom = Frame(root)
    top.pack(side=TOP)
    bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

    # create the widgets for the top part of the GUI, and lay them out
    l = Label(root, width=100, height=2, text='Choose difficulty level')
    b1 = Button(root, text="Easy", width=10, height=2, command=lambda: set_difficulty(1))
    b2 = Button(root, text="Hard", width=10, height=2, command=lambda: set_difficulty(2))
    l.pack(in_=top, side=TOP)
    b1.pack(in_=top, side=LEFT)
    b2.pack(in_=top, side=RIGHT)
    mainloop()


def warningBox():
    global root
    root = Tk()
    root.attributes("-topmost", True)
    root.geometry('%dx%d+%d+%d' % (500, 100, root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2))
    root.protocol('WM_DELETE_WINDOW', doNothing)
    root.resizable(width=False, height=False)
    top = Frame(root)
    bottom = Frame(root)
    top.pack(side=TOP)
    bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

    # create the widgets for the top part of the GUI,
    # and lay them out
    l = Label(root, width=200, height=2, text='Problem has occured while loading the file. Do you want to reload original one?')
    b1 = Button(root, text="Yes", width=20, height=2, command=backupFile)
    b2 = Button(root, text="No", width=20, height=2, command=root.destroy)
    l.pack(in_=top, side=TOP)
    b1.pack(in_=top, side=LEFT)
    b2.pack(in_=top, side=RIGHT)
    mainloop()


def disableAI():
    global MODE
    MODE = 1


def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()


# creates clickable buttons on main window
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))

        if click[0] == 1:
            if action is not None:
                action()
            return True
    else:
        pygame.draw.rect(DISPLAYSURF, ic,(x,y,w,h))

    smallText = pygame.font.SysFont('freesansbold.ttf', 24)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    DISPLAYSURF.blit(textSurf, textRect)
    return False

# menu of the game
def game_menu():
    FPSCLOCK = pygame.time.Clock()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                # exit game via clicking Q button
                if event.key == K_q:
                    gameQuit()

        DISPLAYSURF.fill(BGCOLOUR)
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        TextSurf, TextRect = text_objects("PONG", largeText)
        TextRect.center = ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(TextSurf, TextRect)

        button("Load config file", int(TextRect.center[0]) - 100, int(TextRect.center[1]) + 100, 200, 50, (125, 125, 125), (80, 80, 80), loadData)
        if button("Play versus Player", int(TextRect.center[0]) - 350,  int(TextRect.center[1]) + 50, 200, 50, (125,125,125), (80,80,80), disableAI) or \
                button("Play versus Computer", int(TextRect.center[0]) + 150, int(TextRect.center[1]) + 50, 200, 50, (125,125,125), (80,80,80), chooseDifficultyBox):
            break

        pygame.display.update()
        FPSCLOCK.tick(15)


# displays who won this match
def showWhoWon(who):
    if who == 0:
        winner = 'Left Player'
    else:
        winner = 'Right Player'
    resultSurf1 = pygame.font.Font('freesansbold.ttf', 40).render(winner + ' Won', True, FGCOLOUR)
    resultRect1 = resultSurf1.get_rect()
    resultRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    DISPLAYSURF.blit(resultSurf1, resultRect1)
    resultSurf2 = BASICFONT.render('press Q to end game', True, FGCOLOUR)
    resultRect2 = resultSurf2.get_rect()
    resultRect2.midtop = resultRect1.midbottom
    DISPLAYSURF.blit(resultSurf2, resultRect2)
    pygame.display.update()
   # pygame.time.Clock().tick(FPS)



# Main function
def main():
    pygame.init()
    global DISPLAYSURF
    global WINDOWWIDTH
    global WINDOWHEIGHT
    global LINETHICKNESS
    global PADDLESIZE
    global PADDLEOFFSET
    global PADDLETHICKNESS
    global BALLSIZE
    global BGCOLOUR
    global FGCOLOUR
    global speed
    global MODE
    # Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')
    game_menu()

    # Initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = WINDOWWIDTH / 2 - LINETHICKNESS / 2
    ballY = WINDOWHEIGHT / 2 - LINETHICKNESS / 2
    global floatBallX
    global floatBallY
    floatBallX = float(ballX)
    floatBallY = float(ballY)
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
    score = [0, 0]
    pause = False

    # Keeps track of ball direction
    ballAngle = randint(30, 150) + choice([0, 180])
    ballDirX = speed*sin(radians(ballAngle))  # - = left, + = right
    ballDirY = speed*cos(radians(ballAngle))  # - = up, + = down

    # Creates Rectangles for ball and paddles.
    paddleL = pygame.Rect(PADDLEOFFSET, playerOnePosition, PADDLETHICKNESS, PADDLESIZE)
    paddleR = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, PADDLETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, BALLSIZE, BALLSIZE)

    # Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddleL)
    drawPaddle(paddleR)
    drawBall(ball)

    pygame.mouse.set_visible(0)  # make cursor invisible

    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                gameQuit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddleL.y = mousey
            elif event.type == KEYDOWN:
                # exit game via clicking Q button
                if event.key == K_q:
                    gameQuit()
                # pause the game
                elif event.key == K_SPACE:
                    if score[0] != 21 or score[1] != 21:
                        pause = not pause
                # pause the game
                elif event.key == K_r:
                    score = [0,0]
                    displayScore(score)
                    pygame.display.update()
                # change speed of the ball
                elif event.key == K_1:
                    ballDirX, ballDirY = changeSpeed(1.5, ballDirX, ballDirY)
                elif event.key == K_2:
                    ballDirX, ballDirY = changeSpeed(2, ballDirX, ballDirY)
                elif event.key == K_3:
                    ballDirX, ballDirY = changeSpeed(2.5, ballDirX, ballDirY)
                elif event.key == K_4:
                    ballDirX, ballDirY = changeSpeed(3, ballDirX, ballDirY)
                elif event.key == K_5:
                    ballDirX, ballDirY = changeSpeed(4, ballDirX, ballDirY)
                elif event.key == K_6:
                    ballDirX, ballDirY = changeSpeed(5, ballDirX, ballDirY)
                elif event.key == K_7:
                    ballDirX, ballDirY = changeSpeed(7, ballDirX, ballDirY)
                elif event.key == K_8:
                    ballDirX, ballDirY = changeSpeed(9, ballDirX, ballDirY)
                elif event.key == K_9:
                    ballDirX, ballDirY = changeSpeed(12, ballDirX, ballDirY)
        if pause:
            continue
        # when someone scores 21 points
        if score[0] == 21:
            showWhoWon(0)
            pause = True
            continue
        if score[1] == 21:
            showWhoWon(1)
            pause = True
            continue
        keys = pygame.key.get_pressed()
        if keys[K_UP] and MODE == 1:
            paddleR.y -= 1 * (1 + int(speed)/1.2)
        elif keys[K_DOWN] and MODE == 1:
            paddleR.y += 1 * (1 + int(speed)/1.2)

        drawArena()
        drawPaddle(paddleL)
        drawPaddle(paddleR)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        score = checkPointScored(ball, score)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkHitBall(ball, paddleL, paddleR, ballDirX, ballDirY)
        if MODE == 0:
            paddleR = artificialIntelligence(ball, ballDirX, paddleR)

        displayScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
