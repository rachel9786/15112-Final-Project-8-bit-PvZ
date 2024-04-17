#Term Project Plants vs. Zombies
from cmu_graphics import *
from PIL import Image
import random
import math

class Plant:
     def __init__(self, lawnRow, lawnCol, health = 10):
          self.lawnRow = lawnRow
          self.lawnCol = lawnCol
          self.health = health

     def loseHealth(self, damage):
          self.health -= damage

     def __hash__(self):
          return hash(self.lawnRow + self.lawnCol)
     
     def __eq__(self, other):
          return (isinstance(other, Plant) and self.lawnRow == other.lawnRow
                  and self.lawnCol == other.lawnCol)

class Peashooter(Plant):
     image = "peashooter.png"
     imageURL = None
     shotRate = 4 # 1 shot / 4 seconds
     peaSpeed = 5 # px/step
     damagePerPea = 2
     coolDownTime = 10  # 10 seconds
     sunCost = 100

     def __init__(self, lawnRow, lawnCol):
          super().__init__(lawnRow, lawnCol)
          self.selfTimer = 0 # to keep track of when to shoot next pea

     def updateSelfTimer(self):
          self.selfTimer += 1

     def __hash__(self):
          return super().__hash__()

     def __eq__(self, other):
          return super().__eq__(other)
     
class Sunflower(Plant):
     image = "sunflower.png"
     coolDownTime = 7
     sunCost = 50
     sunSpawnRate = 7

     def __init__(self, lawnRow, lawnCol):
          super().__init__(lawnRow, lawnCol)
          self.selfTimer = 0 # to keep track of when to produce next Sun

     def updateSelfTimer(self):
          self.selfTimer += 1

     def __hash__(self):
          return super().__hash__()

     def __eq__(self, other):
          return super().__eq__(other)

class CabbagePult(Plant):
     image = "Cabbage pult.png"
     pultRate = 6
     cabbageSpeed = 5
     damagePerHead = 2
     coolDownTime = 10  # 10 seconds
     sunCost = 150

     def __init__(self, lawnRow, lawnCol):
          super().__init__(lawnRow, lawnCol)
          self.selfTimer = 0 # to keep track of when to launch next cabbage

     def updateSelfTimer(self):
          self.selfTimer += 1

     def __hash__(self):
          return super().__hash__()

     def __eq__(self, other):
          return super().__eq__(other)

class Zombie:
     image = "zombie.png"
     speed = 1 # px/step
     biteFrequency = 2 #bite every 2 seconds
     
     def __init__(self, lawnRow, health = 10):
          self.x = 810
          self.lawnRow = lawnRow
          self.health = health
          self.selfTimer = 5
          self.encounteredPlant = None
          self.damage = 5

     def move(self):
          self.x -= Zombie.speed

     def loseHealth(self, damage):
          self.health -= damage  

     def updateSelfTimer(self):
          self.selfTimer += 1

     def __hash__(self):
          return hash(self.lawnRow)
     
     def __eq__(self, other):
          return (isinstance(other, Zombie) and self.lawnRow == other.lawnRow
                  and self.x == other.x)

class ConeHead(Zombie):
     image = "conehead zombie.png"
     def __init__(self, lawnRow):
          health = 15
          super().__init__(lawnRow, health)

     def move(self):
          super().move()

     def loseHealth(self, damage):
          super().loseHealth(damage) 

     def updateSelfTimer(self):
          super().updateSelfTimer()

     def __hash__(self):
          return super().__hash__()
     
     def __eq__(self, other):
          return isinstance(other, ConeHead) and super().__hash__()

class BucketHead(Zombie):
     image = "buckethead zombie.png"
     def __init__(self, lawnRow):
          health = 20
          super().__init__(lawnRow, health)

     def move(self):
          super().move()

     def loseHealth(self, damage):
          super().loseHealth(damage) 

     def updateSelfTimer(self):
          super().updateSelfTimer()

     def __hash__(self):
          return super().__hash__()
     
     def __eq__(self, other):
          return isinstance(other, BucketHead) and super().__hash__()

class SmartZombie(Zombie):
     image = 'smart zombie.png'
     def __init__(self, lawnRow):
          health = 10
          super().__init__(lawnRow, health)

     def move(self):
          super().move()

     def loseHealth(self, damage):
          super().loseHealth(damage) 

     def updateSelfTimer(self):
          super().updateSelfTimer()

     def __hash__(self):
          return super().__hash__()
     
     def __eq__(self, other):
          return isinstance(other, SmartZombie) and super().__hash__()     

class Sun:
     image = 'sun.png'
     lifeSpan = 15 # seconds

     def __init__(self, x, y = 0):
          self.x = x
          self.y = y
          self.selfTimer = 0

     def updateSelfTimer(self):
          self.selfTimer += 1

     def fall(self):
          self.y += 2

     def __hash__(self):
          return hash(self.x)
     
     def __eq__(self, other):
          return (isinstance(other, Sun) and self.x == other.x and self.y == other.y)

class Pea:
     def __init__(self, x, lawnRow):
          self.x = x
          self.lawnRow = lawnRow
          self.damage = 2

     def move(self, dx):
          self.x += dx

     def __hash__(self):
          return hash(self.lawnRow)
     
     def __eq__(self, other):
          return (isinstance(other, Pea) and self.x == other.x and 
                  self.lawnRow == other.lawnRow)

class Cabbage:
     g = -3 # gravitational constant # px / step^2
     def __init__(self, startX, startY):
          self.startX = startX
          self.startY = startY
          self.x = startX
          self.y = startY
          self.dx = 0

          self.startdY = 24
          self.dy = self.startdY
          self.damage = 4
          self.selfTimer = 0

          # v = v(original) + a*t
          self.timeInAir = 2 * self.startdY / abs(Cabbage.g) # steps (not seconds)

     def setDX(self, dx):
          self.dx = dx

     def move(self):
          # v = v(original)t + 0.5 * a * t**2  
          # a being acceleration (in this case, g) 
          t = self.selfTimer
          self.dy += Cabbage.g

          self.x += self.dx
          self.y -= self.dy

     def updateSelfTimer(self):
          self.selfTimer += 1

     def __hash__(self):
          return hash(self.dx + self.startX)
     
     def __eq__(self, other):
          return (isinstance(other, Cabbage) and self.x == other.x and 
                  self.y == other.y)

class Level:
     def __init__(self, rosterSize, lawnLanes, zombieWaves, zombieTypes, 
                  sunFallRate, levelDuration, waveDuration, zombieSpawnRate,
                  waveSpawnRate):
          self.rosterSize = rosterSize # int
          self.lawnLanes = lawnLanes # int
          self.zombieWaves = zombieWaves # int
          self.sunFallRate = sunFallRate
          self.levelDuration = levelDuration #seconds
          self.waveDuration = waveDuration
          self.zombieSpawnRate = zombieSpawnRate
          self.waveSpawnRate = waveSpawnRate

          self.roster = [] # list
          self.rosterInCoolDown = []
          self.rosterCoolDownTimes = []

          self.zombieTypes = []
          self.zombieSpawnRates = [6,3,1,2] # corresponding to normal, cone and bucket zombies, respectively
          self.randZombieTypes = [] # to randomly generate zombie type based on probability

     def setRoster(self, roster):
          self.roster = roster # list
          self.rosterInCoolDown = [False] * len(self.roster)
          self.rosterCoolDownTimes = []
          for plantType in self.roster: 
               self.rosterCoolDownTimes.append(plantType.coolDownTime)

     def setZombies(self, zombieTypes):
          self.zombieTypes = zombieTypes # list
          if len(self.zombieTypes) == 1:
               self.randZombieTypes = [self.zombieTypes[0]]
          else:
               for i in range(len(self.zombieTypes)):
                    list = [self.zombieTypes[i]] * self.zombieSpawnRates[i]
                    self.randZombieTypes.extend(list)

     def coolDown(self):
          for i in range(len(self.roster)):
               if self.rosterInCoolDown[i] == True:
                    if self.rosterCoolDownTimes[i] <= 0:
                         self.rosterInCoolDown[i] = False
                         plantType = self.roster[i]
                         self.rosterCoolDownTimes[i] = plantType.coolDownTime
                    else:
                         self.rosterCoolDownTimes[i] -= 1

def onAppStart(app):
     app.width = 800
     app.height = 500
     app.numLevels = 3
     app.currentLevelNum = 0
     app.currentLevel = None
     app.stepsPerSecond = 15

     screens(app)
     mainMenu(app)
     levelSelect(app)
     images(app)
     levelPlantSelect(app)
     levels(app)
     levelGameplay(app)
     levelEnd(app)

def screens(app):
     app.atMainMenu = True
     app.atHowToPlay = False
     app.atLevelSelect = False
     app.atLevelPlantSelect = False
     app.atLevelGameplay = False
     app.atLevelLost = False
     app.atLevelWon = False
     app.atUnlockPlant = False

def mainMenu(app):
     playButton(app)
     howToPlay(app)

def playButton(app):
     app.playButtonY = 2*app.height/3 + 17
     app.playButtonLeft = app.width/2 - 100
     app.playButtonWidth = 188
     app.playButtonHeight = 79

     app.playButtonX = app.playButtonLeft + app.playButtonWidth//2
     app.playButtonY = app.playButtonY + app.playButtonHeight//2

def howToPlay(app):
     cornerOffset = 15
     app.howToPlayButtonRight = app.width - cornerOffset
     app.howToPlayButtonTop = cornerOffset
     app.howToPlayButtonWidth = 150
     app.howToPlayButtonHeight = 40
     app.howToPlayButtonX = app.howToPlayButtonRight - app.howToPlayButtonWidth//2
     app.howToPlayButtonY = app.howToPlayButtonTop + app.howToPlayButtonHeight//2

     app.cornerXRight = app.width - 10
     app.cornerXTop = 10
     app.cornerXWidth = 30
     app.cornerXHeight = 30
     app.cornerXX = app.cornerXRight - app.cornerXWidth//2
     app.cornerXY = app.cornerXTop + app.cornerXHeight//2

def levelSelect(app):
     app.levelButtonY = app.height/3
     app.levelOneButtonX = app.width/4
     app.levelButtonWidth = 100
     app.levelButtonHeight = 100

def levelPlantSelect(app):
     app.allPlants = [Peashooter, Sunflower, CabbagePult]
     app.availablePlants = [Peashooter] # added to w each unlocked plant type
     app.allZombies = [Zombie, ConeHead, BucketHead]
     app.zombieTypes = [Zombie] # added to upon level win (like available plants)
     app.selectedPlants = []
     app.nextUnlockedPlant = None
     app.nextUnlockedZombie = None
     for i in range(len(app.allPlants)):
          plant = app.allPlants[i]
          if plant not in app.availablePlants:
               app.nextUnlockedPlant = plant
               break
     for zombie in app.allZombies:
          if zombie not in app.zombieTypes:
               app.nextUnlockedZombie = zombie
               break

     startLevelButton(app)
     availablePlants(app)
     plantSelectRoster(app)
     smartZombiesToggle(app)

def startLevelButton(app):
     app.startLevelButtonX = 3*app.width/4
     app.startLevelButtonY = 4*app.height/5
     app.startLevelButtonWidth = 300
     app.startLevelButtonHeight = 100

def availablePlants(app):
     app.availablePlantsSquareWidth = 100
     app.availablePlantsSquareHeight = 100
     app.availablePlantsStartX = app.availablePlantsSquareWidth/2 + 20
     app.availablePlantsY = 300

def plantSelectRoster(app):
     app.plantSelectRosterSquareWidth = 70
     app.plantSelectRosterSquareHeight = 70
     app.plantSelectRosterStartX = app.plantSelectRosterSquareWidth/2 + 20
     app.plantSelectRosterY = app.plantSelectRosterSquareHeight/2 + 20

def smartZombiesToggle(app):
     app.toggleX = 50
     app.toggleY = 450
     app.toggleWidth = 50
     app.toggleHeight = 50

def levels(app):
     # Level(self, rosterSize, lawnLanes, zombieWaves, zombieTypes, sunFallRate,
     #         levelDuration, waveDuration, zombieSpawnRate, waveSpawnRate)
     app.testLevel = Level(1, 5, 0, app.zombieTypes, 20, 10, 0, 10, 5)
     app.level1 = Level(1, 5, 1, app.zombieTypes, 8, 70, 15, 20, 5)
     app.level2 = Level(2, 5, 1, app.zombieTypes, 15, 60, 15, 11, 3)
     app.level3 = Level(3, 5, 2, app.zombieTypes, 15, 90, 15, 11, 3)
     app.levels = [app.level1, app.level2, app.level3]

def levelGameplay(app):
     app.draggedPlant = None
     lawn(app)
     roster(app)
     projectiles(app)
     zombies(app)
     sun(app)
     paused(app)

def lawn(app):
     app.lawnCols = 9
     app.lawnRows = 5
     app.lawnStartColX = 2 * app.width//11
     app.lawnStartRowY = app.width//7
     app.lawnSquareWidth = app.width//11
     app.lawnSquareHeight = app.height//7

     app.plants = set()
     app.defenseMap = dict()
     
def roster(app):
     app.rosterSquareWidth = 50
     app.rosterSquareHeight = 50
     app.rosterStartX = app.rosterSquareWidth/2 + 5
     app.rosterY = app.rosterSquareHeight/2 + 5

     app.selectedPlant = None

def projectiles(app):
     # peas
     app.peaRadius = 10
     app.peas = set()
     # cabbage heads
     app.cabbageRadius = 10
     app.cabbages = set()

def zombies(app):
     app.toggledSmartZombies = False
     app.zombieStepCounter = 0
     zombieWave(app)

     app.movingZombies = set()
     app.eatingZombies = set()
     app.zombies = set()

def zombieWave(app):
     app.zombieWaveCounter = 0
     app.inZombieWave = False
     app.zombieWaveNum = 0

     app.zombieWaveStartTimes = []

def sun(app):
     app.fallingSuns = set()
     app.fallenSuns = set()
     app.sunStepCounter = 0

     app.sunAmount = 50
     app.sunCounterWidth = 50
     app.sunCounterHeight = 50
     app.sunCounterX = app.sunCounterWidth/2 + 5
     rosterBot = app.rosterY + app.rosterSquareHeight/2
     app.sunCounterY = rosterBot + 5 + app.sunCounterHeight/2

     app.sunRadius = 20

     lawnEndY = app.lawnStartRowY + app.lawnSquareHeight * app.lawnRows
     app.sunStopY = random.randint(app.height/2, lawnEndY)

def paused(app):
     app.isPaused = False

     app.pauseMenuWidth = app.width/2
     app.pauseMenuHeight = app.width/2
     app.pauseMenuTop = app.height/2 - app.pauseMenuHeight/2

     resumeButton(app)
     restartButton(app)
     mainMenuButton(app)

def resumeButton(app):
     app.resumeButtonY = app.pauseMenuTop + app.pauseMenuHeight//4
     app.resumeButtonWidth = app.width/3
     app.resumeButtonHeight = app.height//6

def restartButton(app):
     app.restartButtonY = app.pauseMenuTop + app.pauseMenuHeight//2
     app.restartButtonWidth = app.width/3
     app.restartButtonHeight = app.height//6

def mainMenuButton(app):
     app.mainMenuButtonX = app.width//2
     app.mainMenuButtonY = app.pauseMenuTop + 3 * app.pauseMenuHeight//4
     app.mainMenuButtonWidth = app.width/3
     app.mainMenuButtonHeight = app.height//6

def levelEnd(app):
     returnToMainMenuButton(app)
     keepPlayingButton(app)

def returnToMainMenuButton(app):
     app.returnToMMButtonX = app.width//3
     app.returnToMMButtonY = 5* app.height//7
     app.returnToMMButtonWidth = 150
     app.returnToMMButtonHeight = 50

def keepPlayingButton(app):
     app.keepPlayingButtonX = 2 * app.width//3
     app.keepPlayingButtonY = 5* app.height//7
     app.keepPlayingButtonWidth = 150
     app.keepPlayingButtonHeight = 50

def getXYfromLawnCords(app, lawnRow, lawnCol):
     # lawn (row, col) conversion to app (x,y) #pixels
     lawnSquareX = app.lawnStartColX + (lawnCol * app.lawnSquareWidth)
     lawnSquareY = app.lawnStartRowY + (lawnRow * app.lawnSquareHeight)
     return lawnSquareX, lawnSquareY

def secondsToSteps(app, seconds):
     return seconds * app.stepsPerSecond

def stepsToSeconds(app, steps):
     return steps // app.stepsPerSecond

def images(app):
     # all images drawn by me using "make8bitart.com" or cmu_graphics
     app.imageScale, app.smallImageScale = 4, 6
     screenImages(app)
     objectImages(app)
     plantImages(app)
     zombieImages(app)
     
def screenImages(app):
     app.mainMenuImage = Image.open('PvZ title page.png')
     app.MMImageWidth, app.MMImageHeight = app.mainMenuImage.width, app.mainMenuImage.height
     app.MMScale = 3/2

     app.levelWonImage = Image.open('game won page.png')
     app.wonImageWidth, app.wonImageHeight = app.levelWonImage.width, app.levelWonImage.height
     app.wonImageScale = 5/3

     app.howToPlayImage = Image.open('how to play.png')
     app.howToPlayWidth, app.howToPlayHeight = app.howToPlayImage.width, app.howToPlayImage.height
     app.howToPlayScale = 3/2
     app.howToPlayImageY = 150

     app.levelLostImage = Image.open('level lost screen.png')
     app.levelLostWidth, app.levelLostHeight = app.levelLostImage.width, app.levelLostImage.height
     app.levelLostImageScale = 3/2

     app.levelSelectImage = Image.open('level select background.png')
     app.levelSelectWidth, app.levelSelectHeight = app.levelSelectImage.width, app.levelSelectImage.height
     app.levelSelectImageScale = 3/2

     app.zombieMessage = Image.open('zombie message.png')
     app.zombieMessageWidth, app.zombieMessageHeight = app.zombieMessage.width, app.zombieMessage.height
     app.zombieMessageScale = 2
     app.zombieMessageRight = app.width-20
     app.zombieMessageTop = 20

     #cast to CMUImage for faster drawing, idea courtesy of CMUGraphicsPILDemo
     app.mainMenuImage = CMUImage(app.mainMenuImage)
     app.levelWonImage = CMUImage(app.levelWonImage)
     app.howToPlayImage = CMUImage(app.howToPlayImage)
     app.levelLostImage = CMUImage(app.levelLostImage)
     app.levelSelectImage = CMUImage(app.levelSelectImage)
     app.zombieMessage = CMUImage(app.zombieMessage)

def objectImages(app):
     app.sunImage = Image.open(Sun.image)
     app.sunImageWidth, app.sunImageHeight = app.sunImage.width, app.sunImage.height
     app.sunScale = 5
     app.sunCounterScale = 6
     app.sunImage = CMUImage(app.sunImage)

def plantImages(app):
     app.peashooterImage = Image.open(Peashooter.image)
     app.sunflowerImage = Image.open(Sunflower.image)
     app.cabbagePultImage = Image.open(CabbagePult.image)

     app.peashooterWidth,app.peashooterHeight = app.peashooterImage.width,app.peashooterImage.height
     app.sunflowerWidth,app.sunflowerHeight = app.sunflowerImage.width, app.sunflowerImage.height
     app.cabbagePultWidth,app.cabbagePultHeight = app.cabbagePultImage.width, app.cabbagePultImage.height

     app.peashooterImage = CMUImage(app.peashooterImage)
     app.sunflowerImage = CMUImage(app.sunflowerImage)
     app.cabbagePultImage = CMUImage(app.cabbagePultImage)

def zombieImages(app):
     app.zombieImage = Image.open(Zombie.image)
     app.coneHeadImage = Image.open(ConeHead.image)
     app.bucketHeadImage = Image.open(BucketHead.image)
     app.smartZombieImage = Image.open(SmartZombie.image)

     app.zombieWidth,app.zombieHeight = app.zombieImage.width, app.zombieImage.height
     app.scaledZombieWidth = app.zombieWidth//app.imageScale
     app.coneHeadWidth,app.coneHeadHeight = app.coneHeadImage.width, app.coneHeadImage.height
     app.bucketHeadWidth,app.bucketHeadHeight = app.bucketHeadImage.width, app.bucketHeadImage.height
     app.smartZombieWidth, app.smartZombieHeight = app.smartZombieImage.width, app.smartZombieImage.height

     app.zombieImage = CMUImage(app.zombieImage)
     app.coneHeadImage = CMUImage(app.coneHeadImage)
     app.bucketHeadImage = CMUImage(app.bucketHeadImage)
     app.smartZombieImage = CMUImage(app.smartZombieImage)

def redrawAll(app):
     if app.atMainMenu:
          drawMainMenu(app)
     elif app.atLevelSelect:
         drawLevelSelect(app)
     elif app.atLevelPlantSelect:
         drawLevelPlantSelect(app)
     elif app.atLevelGameplay:
         drawLevelGameplay(app)
     elif app.atLevelLost:
          drawLevelLost(app)
     elif app.atLevelWon:
          drawLevelWon(app)
         
def drawMainMenu(app):
    if app.atHowToPlay:
         drawHowToPlay(app)
    else:
          #background
          drawRect(0, 0, app.width, app.height, fill = 'lightCyan')
          groundY = app.playButtonY + app.playButtonHeight/2
          drawRect(0, groundY, app.width, app.height-groundY, fill = 'saddleBrown')

          drawPlayButton(app)

          scaledWidth, scaledHeight = app.MMImageWidth//app.MMScale, app.MMImageHeight//app.MMScale
          drawImage(app.mainMenuImage, app.width/2+20, app.height/2, width = scaledWidth, 
                    height = scaledHeight, align = 'center')
          
          drawHowToPlayButton(app)

               #credits
          creditY = app.height - 20
          drawLabel('inspired by Plants vs. Zombies by Pop Cap Games', 20, 
                    creditY, align = 'left', bold = True, size = 14)
          drawLabel('by Rachel Lewis', app.width - 20, creditY, align = 'right', bold = True,
                    size = 14)

def drawPlayButton(app):
     height = app.playButtonHeight
     width = app.playButtonWidth
     drawRect(app.playButtonX, app.playButtonY, width, height, 
              border = 'black', fill = None, align = 'center')

def drawHowToPlayButton(app):
     x, y = app.howToPlayButtonX, app.howToPlayButtonY 
     width, height = app.howToPlayButtonWidth, app.howToPlayButtonHeight

     drawRect(x, y, width, height, fill = None, border = 'black', align = 'center',
              borderWidth = 3)
     drawLabel('How To Play', x, y, size = 20)

def drawHowToPlay(app):
     scaledWidth, scaledHeight = app.howToPlayWidth//app.howToPlayScale, app.howToPlayHeight//app.howToPlayScale
     drawImage(app.howToPlayImage, app.width/2, app.howToPlayImageY, width = scaledWidth,
               height = scaledHeight, align = 'center' )
     
     x, y = app.cornerXX, app.cornerXY
     drawRect(x, y, app.cornerXWidth, app.cornerXHeight, fill = None, border = 'black',
              align = 'center')
     drawRect(x, y, 3, app.cornerXHeight, fill = 'red', rotateAngle = 45, 
              align = 'center')
     drawRect(x, y, 3, app.cornerXHeight, fill = 'red', rotateAngle = -45, 
              align = 'center')

def drawLevelSelect(app):
    drawRect(0,0, app.width, app.height, fill = 'lightCyan')
    scaledWidth, scaledHeight = app.levelSelectWidth//app.levelSelectImageScale, app.levelSelectHeight//app.levelSelectImageScale
    drawImage(app.levelSelectImage, app.width/2, app.height+5, align = 'bottom', 
              width = scaledWidth, height = scaledHeight)

    width = app.levelButtonWidth
    height = app.levelButtonHeight
    
    for i in range(app.numLevels):
        drawRect(((i%3)+1)*app.levelOneButtonX, app.levelButtonY + app.levelButtonY * (i//3), 
                 width, height, align = 'center', border = 'black', fill = None, 
                 borderWidth = 5)
        drawLabel((f'Level {i+1}'), ((i%3)+1)*app.levelOneButtonX, 
                  app.levelButtonY + app.levelButtonY * (i//3), size = 20)

def drawLevelPlantSelect(app):
     drawRect(0,0, app.width, app.height, fill = 'lightGray')
     scaledWidth, scaledHeight = app.zombieMessageWidth//app.zombieMessageScale, app.zombieMessageHeight//app.zombieMessageScale
     drawImage(app.zombieMessage, app.zombieMessageRight, app.zombieMessageTop, 
               align = 'right-top', width = scaledWidth, height = scaledHeight)
     drawStartLevelButton(app)
     drawAvailablePlants(app)
     drawPlantSelectRoster(app)
     drawSmartZombieToggle(app)
     
def drawStartLevelButton(app):
     width = app.startLevelButtonWidth
     height = app.startLevelButtonHeight
     drawRect(app.startLevelButtonX, app.startLevelButtonY, width, height, align = 'center',
              fill = None, border = 'black')
     drawLabel('Click to start level', app.startLevelButtonX, app.startLevelButtonY, size = 20)

def drawAvailablePlants(app):
     startX, y = app.availablePlantsStartX, app.availablePlantsY
     labelX, labelY = startX - app.availablePlantsSquareWidth/2, y - app.availablePlantsSquareHeight/2 - 20
     drawLabel('Choose your plants:', labelX, labelY, align = 'left', fill = 'green', 
               size = 20)
     for i in range(len(app.allPlants)):
          width, height = app.availablePlantsSquareWidth, app.availablePlantsSquareHeight
          spacing = 4*width//3
          x = startX + i*spacing
          drawRect(x, y, width, height, fill = None, border = 'black', align = 'center')
          drawLock(x, y, width, height)
     for i in range(len(app.availablePlants)):
          width, height = app.availablePlantsSquareWidth, app.availablePlantsSquareHeight
          spacing = 4*width//3
          x = startX + i*spacing
          drawRect(x, y, width, height, fill = 'white', border = 'black', align = 'center')
          drawPlant(app, app.availablePlants[i], x, y)

def drawLock(x, y, width, height):
     drawLabel('Locked', x, y, size = 16)

def drawPlantSelectRoster(app):
     width = app.rosterSquareWidth
     height = app.rosterSquareHeight

     for i in range(3):
          drawRect(app.rosterStartX + width*i, app.rosterY, width, height, border = 'black',
                   fill = None, align = 'center')
     for i in range(len(app.selectedPlants)):
          plantType = app.selectedPlants[i]
          x, y = app.rosterStartX + width*i, app.rosterY
          drawSmallPlant(app, plantType, x, y)
          drawLabel(f'{plantType.sunCost}', x, y + height/3, size = 16)
          #drawImage(currentPlant.imageURL, app.rosterStartX + width*i, app.rosterY)

     drawLabel('^ Your plant roster', app.rosterStartX - width//3, 
               app.rosterY + 2*height//3, size = 16, align = 'left')

def drawPlant(app, plantType, x, y):
     if plantType == Peashooter:
          drawPeashooter(app, x, y)
     elif plantType == Sunflower:
          drawSunflower(app, x, y)
     elif plantType == CabbagePult:
          drawCabbagePult(app, x, y)

def drawSmallPlant(app, plantType, x, y):
     if plantType == Peashooter:
          drawSmallPeashooter(app, x, y)
     elif plantType == Sunflower:
          drawSmallSunflower(app, x, y)
     elif plantType == CabbagePult:
          drawSmallCabbagePult(app, x, y)

def drawPeashooter(app, x, y):
     scaledWidth, scaledHeight = app.peashooterWidth//app.imageScale, app.peashooterHeight//app.imageScale
     drawImage(app.peashooterImage, x, y, align = 'center', width = scaledWidth, 
               height = scaledHeight)
     #drawRect(x, y, 20, 20, fill = 'green', align = 'center') #drawn in place of peashooter right now

def drawSunflower(app, x, y):
     scaledWidth, scaledHeight = app.sunflowerWidth//app.imageScale, app.sunflowerHeight//app.imageScale
     drawImage(app.sunflowerImage, x, y, align = 'center', width = scaledWidth, 
               height = scaledHeight)
     #drawRect(x, y, 20, 20, fill = 'orange', align = 'center')

def drawCabbagePult(app, x, y):
     scaledWidth, scaledHeight = app.cabbagePultWidth//app.imageScale, app.cabbagePultHeight//app.imageScale
     drawImage(app.cabbagePultImage, x, y, align = 'center', width = scaledWidth, 
               height = scaledHeight)
     #drawRect(x, y, 20, 20, fill = 'lightGreen', align = 'center')

def drawSmallPeashooter(app, x, y):
     scaledWidth, scaledHeight = app.peashooterWidth//app.smallImageScale, app.peashooterHeight//app.smallImageScale
     drawImage(app.peashooterImage, x, y, align = 'center', width = scaledWidth, 
               height = scaledHeight)
     
def drawSmallSunflower(app, x, y):
     scaledWidth, scaledHeight = app.sunflowerWidth//app.smallImageScale, app.sunflowerHeight//app.smallImageScale
     drawImage(app.sunflowerImage, x, y, align = 'center', width = scaledWidth, 
               height = scaledHeight)
     
def drawSmallCabbagePult(app, x, y):
     scaledWidth, scaledHeight = app.cabbagePultWidth//app.smallImageScale, app.cabbagePultHeight//app.smallImageScale
     drawImage(app.cabbagePultImage, x, y, align = 'center', width = scaledWidth, 
               height = scaledHeight)

def drawSmartZombieToggle(app):
     x, y, width, height = app.toggleX, app.toggleY, app.toggleWidth, app.toggleHeight
     drawRect(x, y, width, height, border = 'black', borderWidth = 3, fill = None, 
              align = 'center')
     drawLabel('Spawn Smart Zombies' , x + width - 10, y, align = 'left', size = 20)
     if app.toggledSmartZombies:
          drawCheckMark(x, y, width)

def drawCheckMark(x, y, size):
    left, up = 3, 19
    drawRect(x - left, y - up, size*3//2, size//6, fill = 'red', rotateAngle = -60, align = 'left')
    drawRect(x, y, size*2//3, size//6, fill = 'red', rotateAngle = 45 ,align = 'right')

def drawLevelGameplay(app):
     drawRect(0,0,app.width, app.height, fill = 'tan')
     drawRoster(app)
     drawSunCounter(app)
     drawLawn(app)
     drawProjectiles(app)
     drawZombies(app)
     drawSuns(app)
     drawDraggedPlant(app)
     if app.inZombieWave:
          drawZombieWaveIncoming(app)
     if app.isPaused:
          drawPauseMenu(app)

def drawRoster(app):
     level = app.currentLevel
     width = app.rosterSquareWidth
     height = app.rosterSquareHeight

     for i in range(len(level.roster)):
          plantType = level.roster[i]
          x, y = app.rosterStartX + width*i, app.rosterY
          drawRect(x, y, width, height, border = 'black',
                   fill = None, align = 'center')
          if plantType == Peashooter:
               drawSmallPeashooter(app, x, y)
          elif plantType == Sunflower:
               drawSmallSunflower(app, x, y)
          elif plantType == CabbagePult:
               drawSmallCabbagePult(app, x, y)
          if level.rosterInCoolDown[i] == True or not isEnoughSun(app, plantType):
               drawRect(app.rosterStartX + width*i, app.rosterY, width, height,
                   fill = 'black', opacity = 50, align = 'center')
               
          drawLabel(f'{plantType.sunCost}', x, y + height/3, size = 16)

def drawDraggedPlant(app):
     if app.draggedPlant != None:
          drawPlant(app, app.draggedPlant, app.draggedPlantX, app.draggedPlantY)

def drawLawn(app):
     color = 'mediumSeaGreen'
     for r in range(app.lawnRows):
          for c in range(app.lawnCols):
               if color == 'mediumSeaGreen':
                    color = 'limeGreen'
               else:
                    color = 'mediumSeaGreen'
               lawnSquareX , lawnSquareY = getXYfromLawnCords(app, r, c)
               drawRect(lawnSquareX, lawnSquareY, app.lawnSquareWidth, 
                        app.lawnSquareHeight, align = 'center', fill = color )
     drawPlants(app)

def drawPlants(app):
     for plant in app.plants:
          r , c = plant.lawnRow , plant.lawnCol
          x , y = getXYfromLawnCords(app, r, c)
          y -= app.lawnSquareHeight//7
          if isinstance(plant, Peashooter):
               drawPeashooter(app, x, y)
          elif isinstance(plant, Sunflower):
               drawSunflower(app, x, y)
          elif isinstance(plant, CabbagePult):
               drawCabbagePult(app, x - app.lawnSquareWidth//5, y)
          # elif isinstance *insert other plant types here* 

def drawProjectiles(app):
     for pea in app.peas:
          drawPea(app, pea)
     for cabbage in app.cabbages:
          drawCabbage(app, cabbage)

def drawCabbage(app, cabbage):
     drawCircle(cabbage.x, cabbage.y, app.cabbageRadius, fill = 'lightGreen')

def drawPea(app, pea):
     x, y = getXYfromLawnCords(app, pea.lawnRow, 3)
     x = pea.x
     drawCircle(x, y - app.lawnSquareHeight//4, app.peaRadius, fill = 'green')

def drawZombies(app):
     for zombie in app.zombies:
          if isinstance(zombie, BucketHead):
               drawBucketHeadZombie(app, zombie)
          elif isinstance(zombie, ConeHead):
               drawConeHeadZombie(app, zombie)
          elif isinstance(zombie, SmartZombie):
               drawSmartZombie(app, zombie)
          elif isinstance(zombie, Zombie):
               drawZombie(app, zombie)

def drawBucketHeadZombie(app, zombie):
     x, y = getXYfromLawnCords(app, zombie.lawnRow, 0)
     y += app.lawnSquareHeight//5
     x = zombie.x

     scaledWidth, scaledHeight = app.bucketHeadWidth//app.imageScale, app.bucketHeadHeight//app.imageScale
     drawImage(app.bucketHeadImage, x, y, align = 'bottom', width = scaledWidth, 
               height = scaledHeight)

def drawConeHeadZombie(app, zombie):
     x, y = getXYfromLawnCords(app, zombie.lawnRow, 0)
     y += app.lawnSquareHeight//5
     x = zombie.x

     scaledWidth, scaledHeight = app.coneHeadWidth//app.imageScale, app.coneHeadHeight//app.imageScale
     drawImage(app.coneHeadImage, x, y, align = 'bottom', width = scaledWidth, 
               height = scaledHeight)

def drawSmartZombie(app, zombie):
     x, y = getXYfromLawnCords(app, zombie.lawnRow, 0)
     y += app.lawnSquareHeight//5
     x = zombie.x

     scaledWidth, scaledHeight = app.smartZombieWidth//app.imageScale, app.smartZombieHeight//app.imageScale
     drawImage(app.smartZombieImage, x, y, align = 'bottom', width = scaledWidth, 
               height = scaledHeight)

def drawZombie(app,zombie):
     x, y = getXYfromLawnCords(app, zombie.lawnRow, 0)
     y += app.lawnSquareHeight//5
     x = zombie.x
     scaledWidth, scaledHeight = app.zombieWidth//app.imageScale, app.zombieHeight//app.imageScale
     drawImage(app.zombieImage, x, y, align = 'bottom', width = scaledWidth, 
               height = scaledHeight)

def drawSunCounter(app):
     x, y = app.sunCounterX, app.sunCounterY
     drawRect(x, y, app.sunCounterWidth, app.sunCounterHeight, align = 'center', 
              fill = 'skyBlue', border = 'black')
     
     scaledWidth, scaledHeight = app.sunImageWidth//app.sunCounterScale, app.sunImageHeight//app.sunCounterScale
     drawImage(app.sunImage, x, y, width = scaledWidth, height = scaledHeight, 
               align = 'center')

     drawLabel(f'{app.sunAmount}', x, y + app.sunCounterHeight/3, size = 16)

def drawSuns(app):
     for sun in app.fallingSuns:
          drawSun(app, sun)
     for sun in app.fallenSuns:
          drawSun(app, sun)

def drawSun(app, sun):
     scaledWidth, scaledHeight = app.sunImageWidth//app.sunScale, app.sunImageHeight//app.sunScale
     drawImage(app.sunImage, sun.x, sun.y, width = scaledWidth, height = scaledHeight, 
               align = 'center')

def drawZombieWaveIncoming(app):
     if app.zombieWaveCounter <= secondsToSteps(app, 5):
          drawLabel('A Wave of Zombies is Approaching', app.width/2, app.height/2,
                    fill = 'red', bold = True, size = 40)

def drawPauseMenu(app):
     drawRect(app.width/2, app.height/2, app.pauseMenuWidth, app.pauseMenuHeight,
              fill = 'white', align = 'center', border = 'black')
     drawResumeButton(app)
     drawRestartButton(app)
     drawMainMenuButton(app)

def drawResumeButton(app):
     height, width = app.resumeButtonWidth, app.resumeButtonHeight
     drawRect(app.width/2, app.resumeButtonY, height, width, border = 'black', 
              fill = None, borderWidth = 5, align = 'center')
     drawLabel('Resume', app.width/2, app.resumeButtonY, size = 25)

def drawRestartButton(app):
     height, width = app.restartButtonWidth, app.restartButtonHeight
     drawRect(app.width/2, app.restartButtonY, height, width, border = 'black', 
              fill = None, borderWidth = 5, align = 'center')
     drawLabel('Restart', app.width/2, app.restartButtonY, size = 25)

def drawMainMenuButton(app):
     height, width = app.mainMenuButtonWidth, app.mainMenuButtonHeight
     drawRect(app.width/2, app.mainMenuButtonY, height, width, border = 'black', 
              fill = None, borderWidth = 5, align = 'center')
     drawLabel('To Main Menu', app.width/2, app.mainMenuButtonY, size = 25)

def drawLevelLost(app):
     drawRect(0,0, app.width, app.height, fill = 'blue')
     scaledWidth, scaledHeight = app.levelLostWidth//app.levelLostImageScale, app.levelLostHeight//app.levelLostImageScale
     drawImage(app.levelLostImage, app.width/2, app.height/2, width = scaledWidth,
               height = scaledHeight, align = 'center' )
     drawLabel('Press R to restart', app.width/2, 450, fill = 'white')
     drawLabel('Press M to return to Main Menu', app.width/2, 475, fill = 'white')

     # drawLabel("GAME OVER", app.width/2, app.height/3, size = 80, fill = 'red', bold = True)
     # drawLabel("The Zombies Ate Your Brains", app.width/2, app.height/2)

def drawLevelWon(app):
     if app.atUnlockPlant:
          drawNextUnlockedPlant(app)
          drawReturnToMainMenuButton(app)
          drawKeepPlayingButton(app)
     else:
          scaledWidth, scaledHeight = app.wonImageWidth//app.wonImageScale, app.wonImageHeight//app.wonImageScale
          x, y = app.width//2, app.height//2
          drawImage(app.levelWonImage, x, y, width = scaledWidth, 
                    height = scaledHeight, align = 'center')
          drawBorder(app, x, y, scaledWidth, scaledHeight, 'black')
          if app.nextUnlockedPlant == None:
               drawReturnToMainMenuButton(app)
               drawKeepPlayingButton(app)
          else:
               drawLabel('Click to continue', app.width/2 - 20, 400, size = 16)

def drawBorder(app, centerX, centerY, width, height, color):
     top, bot = centerY - height//2, centerY + height//2
     left, right = centerX - width//2, centerX + width//2

     drawRect(centerX, top, app.width, app.height-top, align = 'bottom', fill = color)
     drawRect(centerX, bot, app.width, app.height-bot, align = 'top', fill = color)
     drawRect(left, centerY, app.width-left, app.height, align = 'right', fill = color)
     drawRect(right, centerY, app.width-right, app.height, align = 'left', fill = color)

def drawNextUnlockedPlant(app):
     drawRect(0,0,app.width, app.height, fill = 'lightCyan')
     x, y = app.width/2, 3*app.height//7
     width, height = 120, 120
     drawLabel('New Plant Unlocked!', x, y - 2*height//3, size = 25)
     drawRect(x, y, width, height, align = 'center', fill = None, 
              border = 'black')
     drawPlant(app, app.nextUnlockedPlant, x, y)
     plantName = getPlantName(app.nextUnlockedPlant)
     drawLabel(plantName, app.width/2, y + height/2 + 15, size = 20)

def getPlantName(plantType):
     if plantType == Peashooter:
          return 'Peashooter'
     elif plantType == Sunflower:
          return 'Sunflower'
     elif plantType == CabbagePult:
          return 'Cabbage-pult'

def drawReturnToMainMenuButton(app):
     x, y = app.returnToMMButtonX, app.returnToMMButtonY
     width, height = app.returnToMMButtonWidth, app.returnToMMButtonHeight 
     drawRect(x, y, width, height, fill = None, border = 'black', borderWidth = 5,
              align = 'center')
     drawLabel('Main Menu', x, y, size = 20)

def drawKeepPlayingButton(app):
     x, y = app.keepPlayingButtonX, app.keepPlayingButtonY
     width, height = app.keepPlayingButtonWidth, app.keepPlayingButtonHeight 
     drawRect(x, y, width, height, fill = None, border = 'black', borderWidth = 5,
              align = 'center')
     drawLabel('Keep Playing', x, y, size = 20)

def onMousePress(app, mouseX, mouseY):
     if app.atMainMenu:
        if app.atHowToPlay:
             if onCornerXButton(app, mouseX, mouseY):
                  app.atHowToPlay = False
        else:
             if onHowToPlayButton(app, mouseX, mouseY):
                  app.atHowToPlay = True
             elif onPlayButton(app, mouseX, mouseY):
               app.atMainMenu = False
               app.atLevelSelect = True
     elif app.atLevelSelect:
          app.currentLevelNum = selectedLevelButton(app, mouseX, mouseY)
          if app.currentLevelNum != 0:
              app.currentLevel = app.levels[app.currentLevelNum-1]
              setWaveStartTimes(app)
              app.atLevelSelect = False
              app.atLevelPlantSelect = True
     elif app.atLevelPlantSelect:
         if onAvailablePlant(app, mouseX, mouseY):
              selectedPlant = selectedAvailablePlant(app, mouseX, mouseY)
              if not inPlantSelectRoster(app, selectedPlant):
                   app.selectedPlants.append(selectedPlant)
         elif onLevelStartButton(app, mouseX, mouseY) and app.selectedPlants != []:
              #ensures at least one plant has been selected to start level
              level = app.currentLevel
              level.setRoster(app.selectedPlants)
              level.setZombies(app.zombieTypes)
              app.atLevelPlantSelect = False
              app.atLevelGameplay = True
         elif onToggleSmartZombies(app, mouseX, mouseY):
              app.toggledSmartZombies = not app.toggledSmartZombies
              if app.toggledSmartZombies == True:
                   app.zombieTypes.append(SmartZombie)
              else:
                   app.zombieTypes.remove(SmartZombie)
     elif app.atLevelGameplay:
          if not app.isPaused:
               if onRosterPlant(app, mouseX, mouseY):
                    selectedPlant = selectedRosterPlant(app, mouseX, mouseY)
                    if not inCoolDown(app, selectedPlant) and isEnoughSun(app, selectedPlant):
                         app.selectedPlant = selectedPlant
               elif onSun(app, mouseX, mouseY):
                    removeSun(app, mouseX, mouseY)
                    app.sunAmount += 25
          else:
               if onResumeButton(app, mouseX, mouseY):
                    app.isPaused = False
               elif onRestartButton(app, mouseX, mouseY):
                    app.isPaused = False
                    app.atLevelGameplay = False
                    app.atLevelPlantSelect = True
                    reset(app)
               elif onMainMenuButton(app, mouseX, mouseY):
                    app.isPaused = False
                    app.atLevelGameplay = False
                    app.atMainMenu = True
                    reset(app)
     elif app.atLevelWon:
          if app.nextUnlockedPlant != None and not app.atUnlockPlant:
               app.atUnlockPlant = True
          elif onReturnToMainMenuButton(app, mouseX, mouseY):
               app.atLevelWon = False
               app.atUnlockPlant = False
               unlockNewPlantAndZombie(app)
               app.atMainMenu = True
          elif onKeepPlayingButton(app, mouseX, mouseY):
               app.atLevelWon = False
               app.atUnlockPlant = False
               unlockNewPlantAndZombie(app)
               app.atLevelSelect = True
     elif app.atLevelLost:
          if onReturnToMainMenuButton(app, mouseX, mouseY):
               app.atLevelLost = False
               app.atMainMenu = True

def onCornerXButton(app, x, y):
     width, height = app.cornerXWidth, app.cornerXHeight
     centerX, centerY = app.cornerXX, app.cornerXY
     return onButton(x, y, width, height, centerX, centerY)

def onHowToPlayButton(app, x, y):
     width, height = app.howToPlayButtonWidth, app.howToPlayButtonHeight
     centerX, centerY = app.howToPlayButtonX, app.howToPlayButtonY
     return onButton(x, y, width, height, centerX, centerY)

def getNextUnlockedPlant(app):
     for plant in app.allPlants:
          if plant not in app.availablePlants:
               return plant
     app.nextUnlockedPlant = None

def getNextUnlockedZombie(app):
     for zombie in app.allZombies:
          if zombie not in app.zombieTypes:
               return zombie
     app.nextUnlockedZombie = None

def unlockNewPlantAndZombie(app):
     if app.nextUnlockedPlant != None:
          app.availablePlants.append(app.nextUnlockedPlant)
          app.nextUnlockedPlant = getNextUnlockedPlant(app)
     if app.nextUnlockedZombie != None:
          app.zombieTypes.append(app.nextUnlockedZombie)
          app.nextUnlockedZombie = getNextUnlockedZombie(app)

def onPlayButton(app, x, y):
    width, height = app.playButtonWidth, app.playButtonHeight
    centerX, centerY = app.playButtonX, app.playButtonY
    return onButton(x, y, width, height, centerX, centerY)

def selectedLevelButton(app, x, y):
     width = app.levelButtonWidth
     height = app.levelButtonHeight

     for i in range(app.numLevels):
        buttonX = ((i%3)+1) * app.levelOneButtonX 
        buttonY = app.levelButtonY + app.levelButtonY * (i//3)

        buttonLeft = buttonX - width/2
        buttonRight = buttonX + width/2
        buttonTop = buttonY - height/2
        buttonBot = buttonY + height/2

        if x > buttonLeft and x < buttonRight and y > buttonTop and y < buttonBot:
             return i+1
     return 0

def onAvailablePlant(app, x, y):
     width, height = app.availablePlantsSquareWidth, app.availablePlantsSquareHeight

     for i in range(len(app.availablePlants)):
          spacing = 4*width//3
          centerX, centerY = app.availablePlantsStartX + i*spacing, app.availablePlantsY
          if onButton(x, y, width, height, centerX, centerY):
               return True
     return False

def selectedAvailablePlant(app, x, y):
     width, height = app.availablePlantsSquareWidth, app.availablePlantsSquareHeight

     for i in range(len(app.availablePlants)):
          spacing = 4*width//3
          centerX, centerY = app.availablePlantsStartX + i*spacing, app.availablePlantsY
          if onButton(x, y, width, height, centerX, centerY):
               return app.availablePlants[i]

def inPlantSelectRoster(app, plantType):
     for plant in app.selectedPlants:
          if plant == plantType:
               return True
     return False

def onLevelStartButton(app, x, y):
    width, height = app.startLevelButtonWidth, app.startLevelButtonHeight
    centerX, centerY = app.startLevelButtonX, app.startLevelButtonY
    return onButton(x, y, width, height, centerX, centerY)

def onToggleSmartZombies(app, x, y):
     width, height = app.toggleWidth, app.toggleHeight
     centerX, centerY = app.toggleX, app.toggleY
     return onButton(x, y, width, height, centerX, centerY)

def setWaveStartTimes(app):
     level = app.currentLevel
     waveEndTime = 0
     for i in range(level.zombieWaves):
          waveEndTime += level.levelDuration//level.zombieWaves
          waveStartTime = waveEndTime - level.waveDuration
          app.zombieWaveStartTimes.append(waveStartTime)

def onRosterPlant(app, x, y):
    level = app.currentLevel
    width, height = app.rosterSquareWidth, app.rosterSquareHeight

    for i in range(len(level.roster)):
          centerX, centerY = app.rosterStartX + width*i, app.rosterY
          if onButton(x, y, width, height, centerX, centerY):
               return True
    return False

def selectedRosterPlant(app, x, y):
    level = app.currentLevel
    width = app.rosterSquareWidth
    height = app.rosterSquareHeight

    for i in range(len(level.roster)):
          squareLeft = app.rosterStartX + width*i - width/2 
          squareRight = app.rosterStartX + width*i + width/2
          squareTop = app.rosterY - height/2
          squareBot = app.rosterY + height/2

          if x > squareLeft and x < squareRight and y > squareTop and y < squareBot:
               return level.roster[i]

def inCoolDown(app, plantType):
     level = app.currentLevel
     index = None
     for i in range(len(level.roster)):
          if level.roster[i] == plantType:
               index = i
     return level.rosterInCoolDown[index]

def isEnoughSun(app, plantType):
     return plantType.sunCost <= app.sunAmount

def onLawn(app, x, y):
    width = app.lawnSquareWidth
    height = app.lawnSquareHeight

    for r in range(app.lawnRows):
          for c in range(app.lawnCols):
               centerX, centerY = app.lawnStartColX + (c * width), app.lawnStartRowY + (r * height)
               if onButton(x, y, width, height, centerX, centerY):
                    return True
    return False

def getLawnCords(app, x, y):
     width = app.lawnSquareWidth
     height = app.lawnSquareHeight

     for r in range(app.lawnRows):
          for c in range(app.lawnCols):
               lawnSquareLeft = app.lawnStartColX + (c * width) - width/2
               lawnSquareRight = app.lawnStartColX + (c * width) + width/2
               lawnSquareBot = app.lawnStartRowY + (r * height) + height/2
               lawnSquareTop = app.lawnStartRowY + (r * height) - height/2

               if (x > lawnSquareLeft and x < lawnSquareRight and 
                   y < lawnSquareBot and y > lawnSquareTop):
                    return r,c

def onSun(app, x, y):
     for sun in app.fallingSuns:
          if distance(x, y, sun.x, sun.y) < app.sunRadius:
               return True
     for sun in app.fallenSuns:
          if distance(x, y, sun.x, sun.y) < app.sunRadius:
               return True
     return False

def removeSun(app, x, y):
     for sun in app.fallingSuns:
          if distance(x, y, sun.x, sun.y) < app.sunRadius:
               app.fallingSuns.remove(sun)
               return
     for sun in app.fallenSuns:
          if distance(x, y, sun.x, sun.y) < app.sunRadius:
               app.fallenSuns.remove(sun)
               return

def onResumeButton(app, x, y):
     width, height = app.resumeButtonWidth, app.resumeButtonHeight
     buttonX, buttonY = app.width/2, app.resumeButtonY
     return onButton(x, y, width, height, buttonX, buttonY)

def onRestartButton(app, x, y):
     width, height = app.restartButtonWidth, app.restartButtonHeight
     buttonX, buttonY = app.width/2, app.restartButtonY
     return onButton(x, y, width, height, buttonX, buttonY)

def onMainMenuButton(app, x, y):
     width, height = app.mainMenuButtonWidth, app.mainMenuButtonHeight
     buttonX, buttonY = app.mainMenuButtonX, app.mainMenuButtonY
     return onButton(x, y, width, height, buttonX, buttonY)

def onReturnToMainMenuButton(app, x, y):
     width, height = app.returnToMMButtonWidth, app.returnToMMButtonHeight
     buttonX, buttonY = app.returnToMMButtonX, app.returnToMMButtonY
     return onButton(x, y, width, height, buttonX, buttonY)

def onKeepPlayingButton(app, x, y):
     width, height = app.keepPlayingButtonWidth, app.keepPlayingButtonHeight
     buttonX, buttonY = app.keepPlayingButtonX, app.keepPlayingButtonY
     return onButton(x, y, width, height, buttonX, buttonY)

def onButton(x, y, width, height, buttonX, buttonY):
     buttonLeft = buttonX - width/2
     buttonRight = buttonX + width/2
     buttonTop = buttonY - height/2
     buttonBot = buttonY + height/2

     if x > buttonLeft and x < buttonRight and y > buttonTop and y < buttonBot:
         return True
     else: return False

def distance(x1, y1, x2, y2):
     return ((x1-x2)**2 + (y1-y2)**2) ** 0.5

def onStep(app):
     if app.atLevelGameplay and not app.isPaused:
        spawnZombies(app)
        updateZombieList(app)
        spawnPlantObjects(app)
        sunFall(app)
        updateTimers(app)
        moveProjectiles(app)
        moveZombies(app)
        eatPlants(app)
        checkHealthBars(app)
        if app.inZombieWave:
             app.zombieWaveCounter += 1
     if app.atLevelLost:
          pass
          #level lost timer or something so that game over message comes into view

def updateZombieList(app):
     app.zombies = app.movingZombies | app.eatingZombies

def spawnZombies(app):
     app.zombieStepCounter += 1
     level = app.currentLevel
     levelDuration = secondsToSteps(app, level.levelDuration)

     if (not app.inZombieWave and app.zombieStepCounter < levelDuration):
         # if normal zombie spawning (not a wave)
         if not app.zombieWaveNum >= level.zombieWaves:
               currentWaveStartTime = secondsToSteps(app, app.zombieWaveStartTimes[app.zombieWaveNum])
               if app.zombieStepCounter == currentWaveStartTime:
                    app.inZombieWave = True
                    return
         if app.zombieStepCounter % secondsToSteps(app, level.zombieSpawnRate) == 0:
               spawnZombie(app)

     elif app.inZombieWave:
          app.zombieWaveCounter += 1
          currentWaveStartTime = secondsToSteps(app, app.zombieWaveStartTimes[app.zombieWaveNum])
          if app.zombieStepCounter == currentWaveStartTime + secondsToSteps(app, level.waveDuration):
               #if wave has ended
               app.inZombieWave = False
               app.zombieWaveNum += 1
               app.zombieWaveCounter = 0
               return
          else:
               if app.zombieStepCounter % secondsToSteps(app, level.waveSpawnRate) == 0:
                    spawnZombie(app)
     elif app.zombieStepCounter >= levelDuration and app.zombies == set():
          winLevel(app)

def winLevel(app):
     app.atLevelGameplay = False
     app.atLevelWon = True
     reset(app)

def reset(app):
     app.zombieStepCounter = 0
     app.plants = set()
     app.fallenSuns = set()
     app.fallingSuns = set()
     app.peas = set()
     app.cabbages = set()
     app.selectedPlants = []
     app.sunAmount = 50
     if app.toggledSmartZombies == True:
          app.zombieTypes.remove(SmartZombie)
          app.toggledSmartZombies = False
     app.defenseMap = dict()

def spawnZombie(app):
     level = app.currentLevel
     index = random.randint(0, len(level.randZombieTypes)-1)
     ZombieType = level.randZombieTypes[index]
     if ZombieType == SmartZombie:
          makeDefenseMap(app)
          lawnRow = findWeakestLawnRow(app)
     else:
          lawnRow = random.randint(0, app.lawnRows-1)
     app.movingZombies.add(ZombieType(lawnRow))

def makeDefenseMap(app):
     # key = lawnRow, value = combat plants (peashooter, cabbagepult) in that row
     for row in range(app.lawnRows):
          app.defenseMap[row] = 0
     for plant in app.plants:
          row = plant.lawnRow
          if isinstance(plant, CabbagePult) or isinstance(plant, Peashooter):
               app.defenseMap[row] = (damagePerSecond(app, plant) + 
                                      app.defenseMap.get(plant.lawnRow))
               
def damagePerSecond(app, plant):
     if isinstance(plant, CabbagePult):
          return CabbagePult.damagePerHead / CabbagePult.pultRate
     elif isinstance(plant, Peashooter):
          return Peashooter.damagePerPea / Peashooter.shotRate

def findWeakestLawnRow(app):
     weakestRows = []
     minDamagePerSec = None
     for row in app.defenseMap:
          damagePerSec = app.defenseMap[row]
          if minDamagePerSec == None or damagePerSec < minDamagePerSec:
               weakestRows = [row]
          elif damagePerSec == minDamagePerSec:
               weakestRows.append(row)

     index = random.randint(0, len(weakestRows)-1)
     return weakestRows[index]

def spawnPlantObjects(app):
     spawnProjectiles(app)
     spawnFlowerSun(app)

def spawnProjectiles(app):
     for plant in app.plants:
          if isZombieInRow(app, plant.lawnRow):
               if isinstance(plant, Peashooter):
                    spawnPeashooter(app, plant)
               if isinstance(plant, CabbagePult):
                    spawnCabbage(app, plant)

def spawnPeashooter(app, plant):
     steps = secondsToSteps(app, Peashooter.shotRate)
     if (plant.selfTimer % steps == steps - 1): 
          # shoots a new pea from peashooter
          x, y = getXYfromLawnCords(app, plant.lawnRow, plant.lawnCol)
          x += 2 * app.lawnSquareWidth//5
          newPea = Pea(x, plant.lawnRow)
          app.peas.add(newPea)

def spawnCabbage(app, plant):
     steps = secondsToSteps(app, CabbagePult.pultRate)
     if (plant.selfTimer % steps == steps - 1):
          x, y = getXYfromLawnCords(app, plant.lawnRow, plant.lawnCol)
          newCabbage = Cabbage(x, y)
          newCabbage.setDX(calculateCabbageDX(app, newCabbage, plant.lawnRow))
          app.cabbages.add(newCabbage)
     
def isZombieInRow(app, lawnRow):
     for zombie in app.zombies:
          if zombie.lawnRow == lawnRow:
               return True
     return False

def calculateCabbageDX(app, cabbage, lawnRow):
     closestZombie = findClosestZombie(app, lawnRow)
     # total distance / time = average speed
     # dx is constant (no air resistance in this game)
     dx = math.ceil((closestZombie.x - cabbage.x) / cabbage.timeInAir)
     return dx

def findClosestZombie(app, lawnRow):
     closestZombie = None
     for zombie in app.zombies:
          if zombie.lawnRow == lawnRow:
               if closestZombie == None or zombie.x < closestZombie.x:
                    closestZombie = zombie
     return closestZombie

def spawnFlowerSun(app):
     for plant in app.plants:
          if isinstance(plant, Sunflower):
               steps = secondsToSteps(app, Sunflower.sunSpawnRate)
               if plant.selfTimer % steps == steps - 1:
                    x, y = getXYfromLawnCords(app, plant.lawnRow, plant.lawnCol)
                    newSun = Sun(x + 10, y + 10)
                    app.fallenSuns.add(newSun)

def sunFall(app):
     spawnSkySun(app)
     for sun in app.fallingSuns:
          sun.fall()
          if sun.y > app.sunStopY:
               app.fallenSuns.add(sun)
               app.fallingSuns.remove(sun)
               return

def spawnSkySun(app):
     app.sunStepCounter += 1
     level = app.currentLevel
     if app.sunStepCounter % secondsToSteps(app, level.sunFallRate) == 0:
          updateSunStopY(app)
          leftX = app.lawnStartColX
          rightX = app.lawnSquareWidth * app.lawnCols
          sunX = random.randint(leftX, rightX)
          newSun = Sun(sunX)
          app.fallingSuns.add(newSun)

def updateSunStopY(app):
     # to make the sun fall onto different depths of the lawn
     lawnEndY = app.lawnStartRowY + app.lawnSquareHeight * app.lawnRows
     app.sunStopY = random.randint(app.height/2, lawnEndY)

def updateTimers(app):
     updatePlantTimers(app)
     updateObjectTimers(app)
     updateCoolDownTimers(app)
     updateZombieTimers(app)

def updatePlantTimers(app):
     for plant in app.plants:
          plant.updateSelfTimer()
     
def updateObjectTimers(app):
     updateSunTimers(app)
     updateCabbageTimers(app)

def updateSunTimers(app):
     for sun in app.fallenSuns:
          sun.updateSelfTimer()
          # if sun has been sitting un-collected for too long, it disappears
          if sun.selfTimer >= secondsToSteps(app, Sun.lifeSpan):
               app.fallenSuns.remove(sun)
               return

def updateCabbageTimers(app):
     for cabbage in app.cabbages:
          cabbage.updateSelfTimer()

def updateCoolDownTimers(app):
     level = app.currentLevel
     level.coolDown()

def updateZombieTimers(app):
     for zombie in app.eatingZombies:
          zombie.updateSelfTimer()

def moveProjectiles(app):
     movePeas(app)
     moveCabbages(app)

def movePeas(app):
    dx = Peashooter.peaSpeed
    for pea in app.peas:
        if pea.x > app.width or hitsZombie(app, pea):
            app.peas.remove(pea)
            return
        else: 
             pea.move(dx)

def moveCabbages(app):
     for head in app.cabbages:
        if head.y >= head.startY and head.x != head.startX:
            # if cabbage ends trajectory aka hits its target zombie
            r, c = getLawnCords(app, head.startX, head.startY)
            zombie = findClosestZombie(app, r)
            if zombie == None:
                 # for cases where the target zombie dies before cabbage lands
                 app.cabbages.remove(head)
                 return
            zombie.loseHealth(head.damage)
            app.cabbages.remove(head)
            return
        else: 
             head.move()

def moveZombies(app):
    for zombie in app.movingZombies:
         lawnLeft = app.lawnStartColX - app.lawnSquareWidth/2
         if zombie.x < lawnLeft:
              # zombie got past lawn defenses and into house
              # level loss condition
              loseLevel(app)
         else:
               if app.zombieStepCounter % 2 == 0:
                    zombie.move()
                    a, zombieY = getXYfromLawnCords(app, zombie.lawnRow, 0)
                    if onLawn(app, zombie.x, zombieY):
                         zombie.encounteredPlant = encounteredPlant(app, zombie)
                         if zombie.encounteredPlant != None:
                              # if zombie reaches a plant, stop to eat it
                              app.eatingZombies.add(zombie)
                              app.movingZombies.remove(zombie)
                              return
     
def eatPlants(app):
     for zombie in app.eatingZombies:
          zombie.encounteredPlant = encounteredPlant(app, zombie)
          if zombie.encounteredPlant == None:
               # if encounteredPlant has been eaten, continue moving
               app.movingZombies.add(zombie)
               app.eatingZombies.remove(zombie)
               return
          else:
               if zombie.selfTimer % secondsToSteps(app, Zombie.biteFrequency) == 0:
                    plant = zombie.encounteredPlant
                    plant.loseHealth(zombie.damage)

def hitsZombie(app, pea):
     for zombie in app.zombies:
          if pea.lawnRow == zombie.lawnRow:
               if distance(pea.x, 0, zombie.x, 0) <= (app.peaRadius + app.scaledZombieWidth//2 - 10):
                    zombie.loseHealth(pea.damage)
                    return True
     return False

def encounteredPlant(app, zombie):
     lawnRow, lawnCol = getLawnCords(app, zombie.x, app.height/2) # get zombie lawnCol from x value
     lawnRow = zombie.lawnRow

     for plant in app.plants:
          if plant.lawnRow == lawnRow and plant.lawnCol == lawnCol:
               return plant    
     return None   

def checkHealthBars(app):
     checkPlantHealthBars(app)
     checkZombieHealthBars(app)
          
def checkPlantHealthBars(app):
     for plant in app.plants:
          if plant.health <= 0:
               app.plants.remove(plant)
               return

def checkZombieHealthBars(app):
     for zombie in app.zombies:
          if zombie.health <= 0:
               if zombie in app.movingZombies:
                    app.movingZombies.remove(zombie)
               else:
                    app.eatingZombies.remove(zombie)
               return

def loseLevel(app):
     app.atLevelGameplay = False
     app.atLevelLost = True
     reset(app)

def onKeyPress(app, key):
     if app.atLevelGameplay:
          if key == 'space':
               app.isPaused = not app.isPaused
          elif key == '0':
               winLevel(app)
          elif key == '1':
               loseLevel(app)
     if app.atLevelLost:
          if key == 'r':
               app.atLevelLost = False
               reset(app)
               app.atLevelPlantSelect = True
          if key == 'm':
               app.atLevelLost = False
               reset(app)
               app.atMainMenu = True

def onMouseDrag(app, mouseX, mouseY):
     if app.atLevelGameplay:
          if app.selectedPlant != None:
               app.draggedPlant = app.selectedPlant
               app.draggedPlantX = mouseX
               app.draggedPlantY = mouseY
               #draw translucent plant to follow cursor to know what is being dragged
               
def onMouseRelease(app, mouseX, mouseY):
     if app.atLevelGameplay:
          app.draggedPlant = None
          if app.selectedPlant != None:
               if onLawn(app, mouseX, mouseY):
                    lawnRow, lawnCol = getLawnCords(app, mouseX, mouseY)
                    newPlant = app.selectedPlant(lawnRow, lawnCol)
                    if newPlant in app.plants:
                         return
                    app.plants.add(newPlant)
                    app.sunAmount -= app.selectedPlant.sunCost
                    startPlantCoolDown(app)
                    app.selectedPlant = None

def startPlantCoolDown(app):
     level = app.currentLevel
     for i in range(len(level.roster)):
          if level.roster[i] == app.selectedPlant:
               level.rosterInCoolDown[i] = True

def main():
     runApp(width = 800, height = 500)

main()