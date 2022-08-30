import pygame
import numpy as np
import matplotlib.pyplot as pl
import logging
import random
from operator import itemgetter


def drawSquare(screen, currentColour, current_column, cellSize, current_row):
    pygame.draw.rect(screen, currentColour, [current_column * cellSize, current_row * cellSize,
                                             (current_column + 1) * cellSize, (current_row + 1) * cellSize])


def draw(generation, currentTimeStep, x_cell, y_cell, neutral,
         susceptible, infected, recovered, dead):
    logging.info("Iteration %3i:  " % currentTimeStep)
    rowLabel = "  "
    for l in range(x_cell):
        rowLabel += str(l) + " "
    logging.info(rowLabel)
    for current_row in range(y_cell):
        logging.info("%s %s" % (current_row, generation[current_row].replace('0', neutral + "")
                                .replace('1', susceptible + "")
                                .replace('2', infected + "").replace('3', recovered + "").replace('5', dead + "")))
    return draw


def newStateVN(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours, beta, gamma, alpha, rho, rho1):
    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperCharacter = upperRowNeighbours[1]
    lowerCharacter = lowerRowNeighbours[1]

    newState = selfCharacter

    if selfCharacter == '1':  # .S->I
        if leftCharacter == '2' or rightCharacter == '2' or upperCharacter == '2' or lowerCharacter == '2':
            betaChance = (2 - np.random.uniform())
            if 0 < betaChance < beta:
                newState = '2'

    elif selfCharacter == '2':  # I->R
        gammaChance = (1 - np.random.normal(0.5, 1.0))
        rhoChance = (1 - np.random.normal(0.5, 1.0))
        if gamma > gammaChance > 0:
            newState = '3'
        else:
            if 0 < rhoChance < rho1:  # .R->D
                newState = '5'

    elif selfCharacter == '3':  # R->I
        alphaChance = (1 - np.random.uniform())
        if alpha > alphaChance:
            newState = '1'
        else:
            rhoChance = (1 - np.random.normal(0.5, 1.0))  # .I->D
            if 0 < rhoChance < rho:
                newState = '5'

    return newState


def newStateMOOR(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours, beta, gamma, alpha, rho, rho1):
    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperLeftCharacter = upperRowNeighbours[0]
    upperCenterCharacter = upperRowNeighbours[1]
    upperRightCharacter = upperRowNeighbours[2]

    lowerLeftCharacter = lowerRowNeighbours[0]
    lowerCenterCharacter = lowerRowNeighbours[1]
    lowerRightCharacter = lowerRowNeighbours[2]

    newState = selfCharacter

    if selfCharacter == '1':  # S->I
        if leftCharacter == '2' or rightCharacter == '2' or upperLeftCharacter == '2' or \
                upperRightCharacter == '2' or upperCenterCharacter == '2' or lowerLeftCharacter == '2' or \
                lowerRightCharacter == '2' or lowerCenterCharacter == '2':
            betaChance = (2 - np.random.uniform())
            if 0 < betaChance < beta:
                newState = '2'

    elif selfCharacter == '2':  # I->R
        gammaChance = (1 - np.random.normal(0.5, 1.0))
        rhoChance = (1 - np.random.normal(0.5, 1.0))
        if gamma > gammaChance > 0:
            newState = '3'
        else:
            if 0 < rhoChance < rho1:  # .R->D
                newState = '5'

    elif selfCharacter == '3':  # R->I
        alphaChance = (1 - np.random.uniform())
        if alpha > alphaChance:
            newState = '1'
        else:
            rhoChance = (1 - np.random.normal(0.5, 1.0))  # .I->D
            if 0 < rhoChance < rho:
                newState = '5'

    return newState


def diffVN(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):
    difchance = 0.5

    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperCharacter = upperRowNeighbours[1]
    lowerCharacter = lowerRowNeighbours[1]

    swap = [leftCharacter, selfCharacter, rightCharacter, upperCharacter, lowerCharacter]

    if np.random.uniform() > difchance:
        selfCharacter = random.choice(swap)

    return selfCharacter


def diffMOOR(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):
    difchance = 1

    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperLeftCharacter = upperRowNeighbours[0]
    upperCharacter = upperRowNeighbours[1]
    upperRightCharacter = upperRowNeighbours[2]

    lowerLeftCharacter = lowerRowNeighbours[0]
    lowerCharacter = lowerRowNeighbours[1]
    lowerRightCharacter = lowerRowNeighbours[2]
    swap = [leftCharacter, selfCharacter, rightCharacter, upperRightCharacter, upperLeftCharacter, upperCharacter,
            lowerRightCharacter, lowerLeftCharacter, lowerCharacter]

    if np.random.uniform() > difchance:
        t = random.choice(swap)
        selfCharacter, t = t, selfCharacter

    return diffMOOR


def screenplay(cellCountX, cellCountY, info, total_iteration):
    pygame.init()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    screenHeight = 500
    screenWidth = 500

    cellSize = screenHeight / cellCountX

    size = [int(screenHeight), int(screenWidth)]
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    mainloop = True
    FPS = 60
    playtime = 0
    cycletime = 0
    interval = 1
    step = 0
    while mainloop:
        milliseconds = clock.tick(FPS)
        seconds = milliseconds / 1000.0
        playtime += seconds
        cycletime += seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
        if cycletime > interval:

            if step >= total_iteration:
                pygame.time.wait(2000)
                pygame.quit()
                break
            else:
                step += 1
                pygame.display.set_caption("Итерация %3i:  " % step)

            cycletime = 0

            currentColour = BLACK
            for current_row in range(cellCountY):
                for current_column in range(cellCountX):
                    if 0 < step < total_iteration:
                        if info[step][current_row][current_column] == '1':
                            currentColour = GREEN
                        if info[step][current_row][current_column] == '2':
                            currentColour = RED
                        if info[step][current_row][current_column] == '3':
                            currentColour = BLUE
                        if info[step][current_row][current_column] == '5':
                            currentColour = BLACK
                        drawSquare(screen, currentColour, current_column, cellSize, current_row)

        pygame.display.flip()
    return "step", step


def initialization(x_cell, y_cell):
    List = ['1' * x_cell for i in range(x_cell)]
    temp = ''
    for i in range(x_cell):
        if i == x_cell // 2:
            temp += '2'
        else:
            temp += '1'
    List[y_cell // 2] = temp
    return List


Q = int(input('[1] Ручной ввод данных\n[2] Автоматический ввод данных\n '))
if Q == 1:
    matrix = input("Введите размерность матрицы M*M: ")
    cellCountX = int(matrix)
    cellCountY = int(matrix)
    alpha = float(input("Параметр потери иммунитета "))
    beta = float(input("Параметр заражения "))
    gamma = float(input("Параметр приобретения иммунитета "))
    rho = float(input("Параметр смертности здоровой особи "))
    rho1 = float(input("Параметр смертности больной особи "))
else:
    cellCountX = 10
    cellCountY = 10
    alpha = 0.001  # .R->S
    rho = 0.001  # .R->D
    rho1 = 0.1  # .I->D
    beta = 1.22  # .S->I \1.22
    gamma = 0.5  # .I->R    \0.5

susceptibleCharacter = 'S'
recoveredCharacter = 'R'
infectedCharacter = 'I'
deadCharacter = 'D'
extremeEndValue = '1'

universeList, RES = [], []
info = []

S = int(input('[1] Центральное размешение зараженной клетки\n[2] Случайное размещение зараженной клетки\n '))
if S == 2:
    for currentColumn in range(cellCountX):
        universe = ''.join(random.choice('1111112') for i in range(cellCountY))
        universeList.append(universe)
else:
    universeList = initialization(cellCountX, cellCountY)

currentIteration = 0
neutralCount = 0
susceptibleCount = 0
infectedCount = 0
recoveredCount = 0
deadCount = 0

for currentRow in range(cellCountY):
    neutralCount += universeList[currentRow].count('0')
    susceptibleCount += universeList[currentRow].count('1')
    infectedCount += universeList[currentRow].count('2')
    recoveredCount += universeList[currentRow].count('3')
    deadCount += universeList[currentRow].count('5')
RES.append([neutralCount, susceptibleCount, infectedCount, recoveredCount, currentIteration])

while RES[-1][-3] != 0:

    neutralCount = 0
    susceptibleCount = 0
    infectedCount = 0
    recoveredCount = 0
    deadCount = 0

    for currentRow in range(cellCountY):
        neutralCount += universeList[currentRow].count('0')
        susceptibleCount += universeList[currentRow].count('1')
        infectedCount += universeList[currentRow].count('2')
        recoveredCount += universeList[currentRow].count('3')
        deadCount += universeList[currentRow].count('5')
    RES.append([neutralCount, susceptibleCount, infectedCount, recoveredCount, currentIteration])
    oldUniverseList = []
    temp = []
    for currentRow in range(cellCountY):
        oldUniverseList.append(extremeEndValue + universeList[currentRow] + extremeEndValue)
        temp += [universeList[currentRow]]
    info.append(temp)
    for currentRow in range(cellCountY):
        newUniverseRow = ''
        for currentColumn in range(cellCountX):
            upperRowNeighbours = '111'
            lowerRowNeighbours = '111'
            currentRowNeighbours = oldUniverseList[currentRow][currentColumn:currentColumn + 3]
            if (currentRow - 1) >= 0:
                upperRowNeighbours = oldUniverseList[currentRow - 1][currentColumn:currentColumn + 3]
            if (currentRow + 1) < cellCountY:
                lowerRowNeighbours = oldUniverseList[currentRow + 1][currentColumn:currentColumn + 3]
            newUniverseRow += newStateMOOR(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours, beta, gamma,
                                          alpha, rho, rho1)
            ##newUniverseRow += diffVN(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
            universeList[currentRow] = newUniverseRow
    currentIteration += 1
start = 0.0
end = 10
iteration = 1
timeRange = np.arange(start, end + start, iteration)

pl.plot(list(map(itemgetter(4), RES)), list(map(itemgetter(1), RES)), 'green', label='Восприимчивые')
pl.plot(list(map(itemgetter(4), RES)), list(map(itemgetter(2), RES)), 'red', label='Больные')
pl.plot(list(map(itemgetter(4), RES)), list(map(itemgetter(3), RES)), 'blue', label='Выздоровевшие')

pl.legend(loc=0)

pl.xlabel('Time')
pl.ylabel('Population')
pl.show()
print(screenplay(cellCountX, cellCountY, info, currentIteration), currentIteration, RES[1])
print(deadCount)