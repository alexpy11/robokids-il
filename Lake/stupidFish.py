from twisted.internet import reactor, protocol 
from twisted.protocols import basic
import random, json
validDelta = [ -3, -2, -1, 1, 2, 3 ]


ip = "localhost"
#ip = "192.168.1.6"

name = "Jon"

def getNextPos(status):
    state = status["STATE"]
    map = status["MAP"]

    ############################################################
    ###     modify code below to make the fish smarter       ###
    deltaX = random.choice( validDelta )
    deltaY = random.choice( validDelta )
    ################################################################

    return deltaX, deltaY


class FishProtocol(basic.LineReceiver):    
    def connectionMade(self):
        self.sendLine( name )
    def dataReceived(self, data):
        status = None
        try:
            status = json.loads(data)
        except:
            print "Msg from server is not a valid JSON string."
            print "Msg from server is:",data
            return

        if "ERROR" in status.keys():
            print "+---"+ "-"*84 +"---+"
            print "|   "+status["ERROR"].ljust(84) +"   |"
            print "+---"+ "-"*84 +"---+"
            return
        print "State:",status["STATE"]
        print "Map:" 
        for l in status["MAP"]:
            print l
        deltaX, deltaY = getNextPos(status)
        print "deltaX: ", deltaX, "deltaY:", deltaY
        replayDict = { "deltaX": deltaX, "deltaY": deltaY }
        self.sendLine( json.dumps(replayDict) )

        #deltaX = str(deltaX)
        #if len(deltaX)==1: deltaX = "+" + deltaX
        #deltaY = str(deltaY)
        #if len(deltaY)==1: deltaY = "+" + deltaY
        #self.sendLine( deltaX + deltaY )
    
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
