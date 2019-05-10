import pygame
import random


class Area:
    matrixSize = 4

    def __init__(self, posX, posY, width, height):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.reward = 0

    def setReward(self, reward):
        self.reward = reward


class Player:

    def __init__(self, posX, posY, image, score):
        self.posX = posX
        self.posY = posY
        self.image = image
        self.score = score
        self.matrixPosX = 0
        self.matrixPosY = 0
        self.pos = 0
        self.areaDistance = 110

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
            self.pos -= 4
            return True
        return False

    def moveDown(self):
        if self.matrixPosY < Area.matrixSize - 1:
            self.posY += self.areaDistance
            self.matrixPosY += 1
            self.pos += 4
            return True
        return False

    def increaseScore(self, value):
        self.score = self.score + value


screenWidth = 800
screenHeight = 600
color = (255, 100, 0)
rectWidth = 100
rectHeight = 100
rectSpace = 10

#   Images
playerImage = pygame.image.load('player.png')


areaList = list()

for i in range(0, Area.matrixSize):
    areaList.append(list())
    for j in range(0, Area.matrixSize):
        area = Area(185 + 100 * i + rectSpace * i, 85 + 100 * j +
                    rectSpace * j, rectWidth, rectHeight)
        areaList[i].append(area)
areaList[1][0].reward = 20
player = Player(areaList[0][0].posX, areaList[0][0].posY, playerImage, 100)


#   Q Table
Q = []
for i in range(Area.matrixSize ** 2):
    Q.append([])
    for j in range(4):
        Q[i].append(0)
Q[0][3] = 10


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
    print("*********************************")
    for q in Q:
        print(q)


pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        qFunction(player.pos, 2)
        player.moveUp()

    if pressed[pygame.K_DOWN]:
        qFunction(player.pos, 3)
        player.moveDown()

    if pressed[pygame.K_LEFT]:
        qFunction(player.pos, 0)
        player.moveLeft()

    if pressed[pygame.K_RIGHT]:
        qFunction(player.pos, 1)
        player.moveRight()

    screen.fill((0, 0, 0))

    for i in range(Area.matrixSize):
        for j in range(Area.matrixSize):
            pygame.draw.rect(screen, color, pygame.Rect(
                areaList[i][j].posX, areaList[i][j].posY, areaList[i][j].width, areaList[i][j].height))
            # screen.blit(areaList[i * 4 + j].image, (areaList[i * 4 + j].posX, areaList[i * 4 + j].posY))

    screen.blit(player.image, (player.posX, player.posY))

    # AI

    if player.pos != 10:
        rndDirection = random.randint(0, 3)
        lastPos = player.pos
        if player.move(rndDirection):
            qFunction(lastPos, rndDirection)

    pygame.display.flip()
    clock.tick(10)
