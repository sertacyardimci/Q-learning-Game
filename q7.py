import pygame
import random


class Area:
    matrixSize = 7

    def __init__(self, posX, posY, width, height):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.reward = 0
        self.image = None

    def setReward(self, reward):
        self.reward = reward

    def setImage(self, image):
        self.image = image


class Player:

    def __init__(self, posX, posY, image, areaList):
        self.posX = posX
        self.posY = posY
        self.image = image
        self.areaList = areaList

        self.matrixPosX = 0
        self.matrixPosY = 0
        self.pos = 0
        self.areaDistance = 80

    def move(self, direction):
        if direction == 0:
            return self.moveLeft()

        if direction == 1:
            return self.moveRight()

        if direction == 2:
            return self.moveUp()

        if direction == 3:
            return self.moveDown()

    def moveLeft(self):
        if self.matrixPosX > 0:
            self.posX -= self.areaDistance
            self.matrixPosX -= 1
            self.pos -= 1
            return True
        return False

    def moveRight(self):
        if self.matrixPosX < Area.matrixSize - 1:
            self.posX += self.areaDistance
            self.matrixPosX += 1
            self.pos += 1
            return True
        return False

    def moveUp(self):
        if self.matrixPosY > 0:
            self.posY -= self.areaDistance
            self.matrixPosY -= 1
            self.pos -= Area.matrixSize
            return True
        return False

    def moveDown(self):
        if self.matrixPosY < Area.matrixSize - 1:
            self.posY += self.areaDistance
            self.matrixPosY += 1
            self.pos += Area.matrixSize
            return True
        return False

    def spawnRandPos(self):
        self.matrixPosX = random.randint(0, Area.matrixSize - 1)
        self.matrixPosY = random.randint(0, Area.matrixSize - 1)
        self.posX = areaList[self.matrixPosY][self.matrixPosX].posX
        self.posY = areaList[self.matrixPosY][self.matrixPosX].posY
        self.pos = self.matrixPosY * Area.matrixSize + self.matrixPosX


screenWidth = 1000
screenHeight = 600
colorOrange = (255, 100, 0)
colorWhite = (255, 255, 255)


trainMaxIter = 100
trainIter = 0
isTrainStop = False
isAIrunable = False

useNewTrain = False
useSystemTrainData = False
useUserTrainData = False

answer = input("Do you want train ? y => Yes, n => No:  ")
if answer == "y":
    useNewTrain = True
else:
    answer = input("Do you use train data ? y => Yes, n => No:  ")
    if answer == "y":
        answer = input("Which Data ? => 1 = System Data, 2 = User Data:  ")
        if answer == "1":
            useSystemTrainData = True
        elif answer == "2":
            useUserTrainData = True

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

#   Images
playerImage = pygame.image.load('player.png')
bombImage = pygame.image.load('bomb.png')
finishImage = pygame.image.load('finish.png')
playerImage70 = pygame.image.load('player70.png')
bombImage70 = pygame.image.load('bomb70.png')
finishImage70 = pygame.image.load('finish70.png')

#   Font
font = pygame.font.SysFont("arial", 20, 1)


areaList = list()

#   Create game matrix
rectWidth = 70
rectHeight = 70
rectSpace = 10

for i in range(0, Area.matrixSize):
    areaList.append(list())
    for j in range(0, Area.matrixSize):
        area = Area(200 + rectWidth * j + rectSpace * j, 30 + rectWidth * i +
                    rectSpace * i, rectWidth, rectHeight)
        areaList[i].append(area)

#   Add game images and rewards

areaList[0][1].image = bombImage70
areaList[0][1].reward = -100

areaList[1][5].image = bombImage70
areaList[1][5].reward = -100

areaList[2][1].image = bombImage70
areaList[2][1].reward = -100

areaList[3][3].image = bombImage70
areaList[3][3].reward = -100

areaList[4][2].image = bombImage70
areaList[4][2].reward = -100

areaList[5][0].image = bombImage70
areaList[5][0].reward = -100

areaList[5][3].image = bombImage70
areaList[5][3].reward = -100

areaList[5][4].image = bombImage70
areaList[5][4].reward = -100

areaList[5][5].image = bombImage70
areaList[5][5].reward = -100

areaList[6][5].image = finishImage70
areaList[6][5].reward = 100


player = Player(areaList[0][0].posX, areaList[0]
                [0].posY, playerImage70, areaList)


#   Q Table
Q = []
for i in range(Area.matrixSize ** 2):
    Q.append([])
    for j in range(4):
        Q[i].append(float(0))


#   Fill Q table from system train data
if useSystemTrainData == True:
    f = open("systemtrain7.txt", "r")
    lines = f.readlines()
    f.close()

    for i in range(Area.matrixSize ** 2):
        for j in range(4):
            Q[i][j] = float(lines[i * 4 + j])


#   Fill Q table from user train data
if useUserTrainData == True:
    f = open("usertrain7.txt", "r")
    lines = f.readlines()
    f.close()

    for i in range(Area.matrixSize ** 2):
        for j in range(4):
            Q[i][j] = float(lines[i * 4 + j])

#   Q reward function


def qFunction(pos, direction):
    directionList = []
    if direction == 0:
        if pos % Area.matrixSize - 1 > 0:
            directionList.append(0)
        directionList.append(1)
        if int(pos / Area.matrixSize) - 1 > 0:
            directionList.append(2)
        if int(pos / Area.matrixSize) + 1 < Area.matrixSize:
            directionList.append(3)

    elif direction == 1:
        if pos % Area.matrixSize + 1 < Area.matrixSize:
            directionList.append(1)
        directionList.append(0)
        if int(pos / Area.matrixSize) - 1 > 0:
            directionList.append(2)
        if int(pos / Area.matrixSize) + 1 < Area.matrixSize:
            directionList.append(3)

    elif direction == 2:
        if int(pos / Area.matrixSize) - 1 > 0:
            directionList.append(2)
        directionList.append(3)
        if pos % Area.matrixSize - 1 > 0:
            directionList.append(0)
        if pos % Area.matrixSize + 1 < Area.matrixSize:
            directionList.append(1)

    elif direction == 3:
        if int(pos / Area.matrixSize) + 1 < Area.matrixSize:
            directionList.append(3)
        directionList.append(2)
        if pos % Area.matrixSize - 1 > 0:
            directionList.append(0)
        if pos % Area.matrixSize + 1 < Area.matrixSize:
            directionList.append(1)

    newPos = pos
    if direction == 0:
        newPos = pos - 1
    elif direction == 1:
        newPos = pos + 1
    elif direction == 2:
        newPos = pos - Area.matrixSize
    elif direction == 3:
        newPos = pos + Area.matrixSize
    maxQ = []
    for d in directionList:
        maxQ.append(Q[newPos][d])

    v = Q[pos][direction] + 0.3 * (areaList[int(newPos / Area.matrixSize)]
                                   [newPos % Area.matrixSize].reward + 0.8 * max(maxQ) - Q[pos][direction])
    Q[pos][direction] = v


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE]:
        if isAIrunable == False:
            while(True):
                player.spawnRandPos()
                if areaList[player.matrixPosY][player.matrixPosX].reward != -100 and areaList[player.matrixPosY][player.matrixPosX].reward != 100:
                    isAIrunable = True
                    break

    screen.fill((20, 20, 20))

#   Fill matrix color to screen
    for i in range(Area.matrixSize):
        for j in range(Area.matrixSize):
            pygame.draw.rect(screen, colorOrange, pygame.Rect(
                areaList[i][j].posX, areaList[i][j].posY, areaList[i][j].width, areaList[i][j].height))
            # screen.blit(areaList[i * 4 + j].image, (areaList[i * 4 + j].posX, areaList[i * 4 + j].posY))

#   Display matrix image to screen
    for i in range(Area.matrixSize):
        for j in range(Area.matrixSize):
            if areaList[i][j].image != None:
                screen.blit(areaList[i][j].image, (areaList[i]
                                                   [j].posX, areaList[i][j].posY))


#   Display player to screen
    screen.blit(player.image, (player.posX, player.posY))

    text = font.render("Iterasyon: " + str(trainIter), True, (200, 200, 200))
    screen.blit(text,
                (0, 0))

#   AI
    if useNewTrain == True:
        if trainIter < trainMaxIter:
            if areaList[player.matrixPosY][player.matrixPosX].reward != -100 and areaList[player.matrixPosY][player.matrixPosX].reward != 100:
                rndDirection = random.randint(0, 3)
                lastPos = player.pos
                if player.move(rndDirection):
                    qFunction(lastPos, rndDirection)
            else:
                if trainIter < trainMaxIter:
                    if areaList[player.matrixPosY][player.matrixPosX].reward == 100:
                        trainIter += 1
                player.spawnRandPos()

                if trainIter >= trainMaxIter:
                    isTrainStop = True
                    #   Fill system train data from Q
                    if useNewTrain == True:
                        f = open("usertrain7.txt", "w")
                        for row in Q:
                            for column in row:
                                f.write(str(column) + "\n")

                        f.close()

    if isAIrunable == True:
        d = Q[player.pos].index(max(Q[player.pos]))
        player.move(d)
        if areaList[player.matrixPosY][player.matrixPosX].reward == 100:
            isAIrunable = False

    pygame.display.flip()
    clock.tick(5)
