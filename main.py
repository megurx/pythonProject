import random
import numpy as np
import matplotlib.pyplot as pl
from operator import itemgetter
# Import a library of functions called 'pygame'
import pygame

def getRandomNumber(distribution):
    if distribution == 0:
        returningRandomNumber = np.random.uniform() # UNIFORM
    elif distribution == 1:
        returningRandomNumber = np.random.normal(.5, .1) # NORMAL
    elif distribution == 2:
        returningRandomNumber = (np.random.binomial(20, .5, 100) % 10) * 0.1 # BINOMIAL
    elif distribution == 3:
        returningRandomNumber = np.random.poisson(2) * .1 # POISSON
    return returningRandomNumber

def drawSquare(screen, currentColour, currentColumn, cellSize, currentRow):
    pygame.draw.rect(screen, currentColour, [currentColumn * cellSize, currentRow * cellSize, (currentColumn + 1)
                                             * cellSize, (currentRow + 1) * cellSize])

def drawGenerationUniverse(cellCountX, cellCountY, universeTimeSeries):
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    YELLOW =   (255,   255,   0)
    RED =   (255,   0,   0)

    screenHeight = 800
    screenWidth = 800

    cellSize = screenHeight / cellCountX

    size = [int(screenHeight), int(screenWidth)]
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)

    #Loop until the user clicks the close button.
    clock = pygame.time.Clock()

    #while 1:
    # Make sure game doesn't run at more than 60 frames per second
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second.
    playtime = 0
    cycletime = 0
    interval = .15#.15 # how long one single images should be displayed in seconds
    picnr = 0

    #for currentStep in range(simulationIterations):
    currentTimeStep = 0

    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
        cycletime += seconds
        if cycletime > interval:

            if currentTimeStep >= simulationIterations:
                currentTimeStep = 0
                pygame.time.delay(3000)
                break
            else:
                currentTimeStep += 1
            pygame.time.delay(1000)
            pygame.display.set_caption("TimeStep %3i:  " % currentTimeStep)

            picnr += 1
            if picnr > 5:
                picnr = 0
            cycletime = 0

            for currentRow in range(cellCountY):# Draw a solid rectangle
                for currentColumn in range (cellCountX):
                    # rect(Surface, color, Rect, width=0) -> Rect
                    if currentTimeStep > 0 and currentTimeStep < simulationIterations:
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '0':
                            currentColour = BLUE
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '1':
                            currentColour = YELLOW
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '2':
                            currentColour = RED
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '3':
                            currentColour = GREEN
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '4':
                            currentColour = BLACK

                        if hexagonLayout:
                            drawHexagon(screen, currentColour, currentColumn, cellSize, currentRow)
                        else:
                            drawSquare(screen, currentColour, currentColumn, cellSize, currentRow)
        pygame.display.flip()

def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, susceptibleCharacter, exposedCharacter, infectedCharacter, recoveredCharacter, deadCharacter):
    print("TimeStep %3i:  " % currentTimeStep)
    rowLabel = "  "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print(rowLabel)
    for currentRow in range(cellCountY):
        print("%s %s" % (currentRow, universeList[currentRow].replace('0', susceptibleCharacter + " ").replace('1', exposedCharacter + " ").
                         replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " ").replace('4', deadCharacter + " ")))

''' This method calculates the new state of the cell based on Moore neighborhood '''
def newStateVN(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):
    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperCharacter = upperRowNeighbours[1]
    lowerCharacter = lowerRowNeighbours[1]

    newState = selfCharacter

    if selfCharacter == '3':  # .S->I
        if leftCharacter == '2' or rightCharacter == '2' or upperCharacter == '2' or lowerCharacter == '2':
            Pichance = (2 - np.random.uniform())
            if 0 < Pichance < Pi:
                newState = '2'
            else:
                Pdchance = (1 - np.random.normal(0.5, 1.0))
                if 0 < Pdchance < Pd:
                    newState = '4'

    elif selfCharacter == '2':  # I->R
        Prchance = (1 - np.random.normal(0.5, 1.0))
        Pschance = (1 - np.random.normal(0.5, 1.0))
        if Pr > Prchance  > 0:
            newState = '0'
        else:
            if 0 < Pschance < Ps:  # .I->D
                newState = '4'

    elif selfCharacter == '0':  # R->I
        Pschance = (1 - np.random.uniform())
        if Ps > Pschance :
            newState = '3'
        else:
            Pdchance = (1 - np.random.normal(0.5, 1.0))  # .I->D
            if 0 < Pdchance < Pd:
                newState = '4'

    elif selfCharacter == '1':  # I->R
        if leftCharacter == '3' or rightCharacter == '3' or upperCharacter == '3' or lowerCharacter == '3':
            Pbchance = (1 - np.random.normal(0.5, 1.0))
            if Pb > Pbchance > 0:
                newState = '3'

    elif selfCharacter == '4':  # I->R
        if leftCharacter == '0' or rightCharacter == '0' or upperCharacter == '0' or lowerCharacter == '0':
            Plchance = (1 - np.random.normal(0.5, 1.0))
            if Pl > Plchance > 0:
                newState = '1'
    return newState

def getNewState2Ddiff(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):
    difchance = 0.1
    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperCharacter = upperRowNeighbours[1]
    lowerCharacter = lowerRowNeighbours[1]

    if selfCharacter == upperCharacter:
        swap1 = [selfCharacter, rightCharacter, leftCharacter, lowerCharacter]
        swap = [a for a in swap1 if a != '4']
        if np.random.uniform() > difchance:
            try:
                q = random.choice(swap)
                selfCharacter, q = q, selfCharacter
            except IndexError:
                pass

    elif selfCharacter == lowerCharacter:
        swap1 = [selfCharacter, rightCharacter, upperCharacter, leftCharacter]
        swap = [a for a in swap1 if a != '4']
        if np.random.uniform() > difchance:
            try:
                q = random.choice(swap)
                selfCharacter, q = q, selfCharacter
            except IndexError:
                pass

    elif selfCharacter == leftCharacter:
        swap1 = [selfCharacter, rightCharacter, upperCharacter, lowerCharacter]
        swap = [a for a in swap1 if a != '4']
        if np.random.uniform() > difchance:
            try:
                q = random.choice(swap)
                selfCharacter, q = q, selfCharacter
            except IndexError:
                pass

    elif selfCharacter == rightCharacter:
        swap1 = [selfCharacter, leftCharacter, upperCharacter, lowerCharacter]
        swap = [a for a in swap1 if a != '4']
        if np.random.uniform() > difchance:
            try:
                q = random.choice(swap)
                selfCharacter, q = q, selfCharacter
            except IndexError:
                pass

    return selfCharacter


Pi = 1.33
Pr = 0.1
Ps = 0.1
Pb = 0.5
Pd = 0.1
Pl = 0.5

simulationIterations = 50
cellCountX = 10
cellCountY = 10
hexagonLayout = False

susceptibleCharacter = 'S'
exposedCharacter = 'E'
recoveredCharacter = 'R'
infectedCharacter ='I'
deadCharacter ='D'
extremeEndValue = '0'
timeStart = 0.0
timeEnd = simulationIterations
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)
universeList = []

for currentColumn in range(cellCountY):
    universe = ''.join(random.choice('00000000000000000000000001') for universeColumn in range(cellCountX))
    universeList.append(universe)

InitSusceptibles = 0.0
InitInfected = 0.0
InitRecovered = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0, 0.0]

RES = [InitVariables]

universeTimeSeries = []

for currentTimeStep in range(simulationIterations):
    if currentTimeStep < 0:
        printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, susceptibleCharacter, exposedCharacter, infectedCharacter, recoveredCharacter, deadCharacter)
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    threeCount = 0
    fourCount = 0
    for currentRow in range(cellCountY):
        zeroCount += universeList[currentRow].count('0')
        oneCount += universeList[currentRow].count('1')
        twoCount += universeList[currentRow].count('2')
        threeCount += universeList[currentRow].count('3')
        fourCount += universeList[currentRow].count('4')
    RES.append([zeroCount, oneCount, twoCount, threeCount, fourCount, currentTimeStep])

    oldUniverseList = []
    toCopyUniverseList = []
    for currentRow in range(cellCountY):
        oldUniverseList.append(extremeEndValue + universeList[currentRow] + extremeEndValue)
        toCopyUniverseList.append(universeList[currentRow])

    universeTimeSeries.append(toCopyUniverseList)

    for currentRow in range(cellCountY):
        newUniverseRow = ''
        for currentColumn in range(cellCountX):
            upperRowNeighbours = '000'
            lowerRowNeighbours = '000'
            currentRowNeighbours = oldUniverseList[currentRow][currentColumn:currentColumn+3]
            if (currentRow - 1) >= 0:
                upperRowNeighbours = oldUniverseList[currentRow-1][currentColumn:currentColumn+3]
            if (currentRow + 1) < cellCountY:
                lowerRowNeighbours = oldUniverseList[currentRow+1][currentColumn:currentColumn+3]

            #newUniverseRow += newStateVN(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
            #universeList[currentRow] = newUniverseRow
            newUniverseRow += getNewState2Ddiff(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
            universeList[currentRow] = newUniverseRow

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
RES = np.array(RES)
print(RES)

pl.show()

drawGenerationUniverse(cellCountX, cellCountY, universeTimeSeries)