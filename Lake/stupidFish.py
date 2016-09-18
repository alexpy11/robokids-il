from twisted.internet import reactor, protocol 
from twisted.protocols import basic
import random
validDelta = [ -3, -2, -1, 1, 2, 3 ]


ip = "localhost"
#ip = "192.168.1.6"

name = "Jon"

def getNextPos(map):
    deltaX = random.choice( validDelta )
    deltaY = random.choice( validDelta )
    #print map
    #print map[-2]
    deltaX = 0
    deltaY = +2
       
    print "deltaX: ", deltaX
    print "deltaY:", deltaY



    return deltaX, deltaY


class FishProtocol(basic.LineReceiver):    
    def connectionMade(self):
        self.sendLine( name )
    def dataReceived(self, data):
        print "Server said:", data
        if "MAP" in data:  
            deltaX, deltaY = getNextPos(data[4:-2].split("\n"))
            deltaX = str(deltaX)
            if len(deltaX)==1: deltaX = "+" + deltaX
            deltaY = str(deltaY)
            if len(deltaY)==1: deltaY = "+" + deltaY
            self.sendLine( deltaX + deltaY )
    
    def connectionLost(self, reason):
        print "connection lost"

class FishFactory(protocol.ClientFactory):
    protocol = FishProtocol
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()

reactor.connectTCP(ip, 9020, FishFactory())
reactor.run()
