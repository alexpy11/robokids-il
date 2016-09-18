from twisted.internet.task import LoopingCall
from twisted.internet import reactor, protocol  # , stdio
from twisted.protocols import basic
import pygame, pygame.surfarray as surfarray, math, sys, random, pprint, os

secsBetweenTicks = 1
idColorNextFish = (1, 0, 0)
validDelta = [ "-3", "-2", "-1", "-0", "+0", "+1", "+2", "+3" ]
LAND_COLOR = (128, 64, 0, 255)
WATER_COLOR = (0, 0, 252, 255)
MASK_COLOR = (252, 0, 252, 255)
fishStates = [ "1st challenge: Swim to the bottom", 
               "2nd challenge: Pass the 0 strait",
               "3rd challenge: 5 together", 
               "4th challenge: > formation",
               "Winner" ]

def getIdColorNextFish():
    global idColorNextFish
    idColorThisFish = idColorNextFish
    c = 1 + idColorNextFish[0] + idColorNextFish[1] * 4 + idColorNextFish[2] * 16
    idColorNextFish = (c & 0x3, (c & 0xC) / 4 , (c & 0x30) / 16)
    # [AP] Adopption to Python 3
    print "new idColor:", idColorNextFish
    return idColorThisFish

def pixel2char(pixel, idColor):
    if pixel == WATER_COLOR:
        return "~"  
    elif pixel == LAND_COLOR: 
        return "L"  # land      
    elif ((pixel[0] & 3) == idColor[0]) and ((pixel[1] & 3) == idColor[1]) and ((pixel[2] & 3) == idColor[2]):
       return "O"
    else: 
        return "X"

def getMap((midX, midY) , size, idColor):
    startX = midX - size / 2; endX = midX + size / 2
    startY = midY - size / 2; endY = midY + size / 2
    s = ""
    try:
        for y in range(startY, endY):
            for x in range(startX, endX):
                s += pixel2char(screen.get_at((x, y)), idColor)
            s = s + "\n"
        return s[:-1]
    except:
        return None

def logI(msg):
    print msg

def logD(msg):
    pass

def getWellFormedName(s):
    clean = ""
    for c in s:
        if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.~!@#$%^&*(){}[]<>?:":
             clean += c
    if len(clean) > 20: clean = clean[:20]
    if len(clean) == 0: clean = "random-name-" + str(random.randint(1000, 9999))
    return clean

class LandSprite(pygame.sprite.Sprite):

    def __init__(self, name, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.src_image = pygame.image.load(name + ".bmp")
        self.image = self.src_image
        self.image.set_colorkey(MASK_COLOR)
        self.mask = pygame.mask.from_surface(self.image)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        pass

class FishSprite(pygame.sprite.Sprite):

    def __init__(self, name, image, position, idColor):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.statesAchievedTime = []
        self.time = 0
        self.idColor = idColor
        self.src_image = image
        self.image = self.src_image
        self.image.set_colorkey(MASK_COLOR)
        self.mask = pygame.mask.from_surface(self.image)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.deltaX = 0
        self.deltaY = 0

    def update(self):
        self.time += 1
        if not self.deltaX and not self.deltaY: return
        x, y = self.position
        x += self.deltaX; y += self.deltaY
        self.position = (x, y)
        if self.deltaY == 0:
            direction = 90 if self.deltaX > 0 else 270
        else:
            direction = math.atan(float(self.deltaX) / float(self.deltaY)) * 180. / math.pi
            if self.deltaY < 0: direction += 180
        self.image = pygame.transform.rotate(self.src_image, direction).convert()
        self.image.set_colorkey(MASK_COLOR)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

def printFishStatus():
    print "\nName".ljust(16), "1st", "2nd", "3rd"
    for name in FishFactoryInstance.fishProtocolByName.keys(): 
        print name.ljust(16),
        for s in fishSpriteByName[name].statesAchievedTime:  print str(s).ljust(3),
        print
    print


def game_tick():
   events = pygame.event.get()  # (then process in loop)
   fishGroup.update()
   fishGroup.clear(screen, background)
   fishGroup.draw(screen)
   pygame.display.flip()
   fishToKill = []
   atLeastOnefishStatusChange = False
   for name in FishFactoryInstance.fishProtocolByName.keys():
       fishSprite = fishSpriteByName[name]; fishProtocol = FishFactoryInstance.fishProtocolByName[name]
       if pygame.sprite.collide_mask(fishSprite, zeroIsland):
           fishToKill.append((name, "Fish " + name + " have collided with the zero-island - bye bye."))
       for otherName in FishFactoryInstance.fishProtocolByName.keys():
           if otherName == name: continue
           if pygame.sprite.collide_mask(fishSprite, fishSpriteByName[otherName]):
               fishToKill.append((name, "Fish " + name + " have collided with " + otherName + " - bye bye."))
       map = getMap(fishSprite.position, 25, fishSprite.idColor)
       if map:
           if len(fishSprite.statesAchievedTime) == 1:
               if fishSprite.position[0] < 35 and fishSprite.position[1] < 35: 
                   fishSprite.statesAchievedTime.append(fishSprite.time)
                   atLeastOnefishStatusChange = True 
           if len(fishSprite.statesAchievedTime) == 0:
               if "L" in map[-25:]:
                   fishSprite.statesAchievedTime.append(fishSprite.time)
                   atLeastOnefishStatusChange = True
           msg = "STATE\n" + fishStates[len(fishSprite.statesAchievedTime)]
           msg += "\nMAP\n" + map
           fishProtocol.sendLine(msg)
       else:
           fishToKill.append((name, "Fish " + name + " fell from the edge of the world - bye bye."))
   for name, reason in fishToKill:
       logI(reason)
       FishFactoryInstance.fishProtocolByName[name].sendLine(reason)
       FishFactoryInstance.fishProtocolByName[name].transport.loseConnection()
   if atLeastOnefishStatusChange: printFishStatus()



class TalkToFish(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.factory.fishProtocols.append(self)
        logI("talkToFish: connection made") 

    def connectionLost(self, reason):
        print "inside connectionLost. Name is ", self.name
        if self.name:
            delFish(self.name)
            del self.factory.fishProtocolByName[self.name]
            self.factory.fishProtocols.remove(self)
            logI("talkToFish: connection to fish " + self.name + " lost.") 

    def dataReceived(self, data):
        if not self.name:
            self.name = getWellFormedName(data.strip())
            while self.name in self.factory.fishProtocolByName.keys():
                msg = "A new fish, named: " + self.name + " already exists - will add '-A' to name"
                logI(msg)
                self.sendLine(msg)
                self.name += "-A"

            self.factory.fishProtocolByName[self.name] = self
            addFish(self.name)
            logI("Got a new fish, named: " + self.name)
            # self.sendLine("Nice to meet you,"+self.name)
        else:
            d = data.strip()
            if len(d) != 4:
                msg = "Wrong length data received. Len should be 4 and is actually " + str(len(d))
                logI("Bad data from fish " + self.name + ": " + msg)
                self.sendLine(msg)
                return
            deltaX = d[:2]; deltaY = d[2:]
            if deltaX not in validDelta:
                msg = "deltaX (first 2 chars) is invalid. Valid values are '" + \
                      ",".join(validDelta) + "'. Actual value is '" + deltaX + "'"
                logI("Bad data from fish " + self.name + ": " + msg)
                self.sendLine(msg)
                return
            if deltaY not in validDelta:
                msg = "deltaY (last 2 chars) is invalid. Valid values are '" + \
                      ",".join(validDelta) + "'. Actual value is '" + deltaY + "'"
                logI("Bad data from fish " + self.name + ": " + msg)
                self.sendLine(msg)
                return
            if int(deltaX) == 0 and int(deltaY) == 0:
                msg = "Both deltaX and deltaY are zero. At least one of them must be different than zero"
                logI("Bad data from fish " + self.name + ": " + msg)
                self.sendLine(msg)
                return

            logD("Got valid deltas for fish %s: deltaX = %s, deltaY = %s" % (self.name, deltaX, deltaY))
            for fish in fishGroup.sprites():
                if fish.name == self.name:
                    fish.deltaX = int(deltaX); fish.deltaY = int(deltaY)

class FishFactory(protocol.ServerFactory):
    def __init__(self):
        self.fishProtocolByName = {}
        self.fishProtocols = []
    def buildProtocol(self, addr):
        return TalkToFish(self)

def addFish(name):
    rect = screen.get_rect()
    idColor = getIdColorNextFish()
    if os.path.isfile(name + ".bmp"):
        otherImageValid = True
        image = pygame.image.load(name + ".bmp")
        if image.get_width() <> 16: otherImageValid = False
        if image.get_height() <> 16: otherImageValid = False
    else:
        otherImageValid = False
    if not otherImageValid:
        image = pygame.image.load("defaultFishImage.bmp")    

    imgarray = surfarray.array3d(image)
    imgarray[:, :, :] &= 0xFC
    bg_color = list(MASK_COLOR[:3])
    count = 0
    for y in range(16):
       for x in range(16):
           if (list(imgarray[y, x, :]) != bg_color):
               count += 1
               for i in [0, 1, 2]: imgarray[y, x, i] |= idColor[i]
    print "init: num pix set", count
    surfarray.blit_array(image, imgarray)

    startPos = (random.randint(85, 115), random.randint(85, 115))
    fish = FishSprite(name, image, startPos, idColor)
    fishGroup.add(fish)
    fishSpriteByName[name] = fish

def delFish(name):
    fish = fishSpriteByName[name]
    # remove frm fishSpriteByName
    del fishSpriteByName[name]
    # remove from fishGroup
    fishGroup.remove(fish)
    # remove the sprite 
    fish = None

FishFactory.protocol = TalkToFish
FishFactoryInstance = FishFactory()
reactor.listenTCP(9020, FishFactoryInstance)

screen = pygame.display.set_mode((200, 200))    
background = pygame.image.load('water.bmp')
screen.blit(background, (0, 0))
screen.set_colorkey(MASK_COLOR)
pygame.display.set_caption('Lake of Robotic Fish')


fishSpriteByName = {}
fishGroup = pygame.sprite.Group()
zeroIsland = LandSprite("zeroIsland", (40, 40)); fishGroup.add(zeroIsland)
tick = LoopingCall(game_tick)
tick.start(secsBetweenTicks)

reactor.run() 

