from SimpleCV import Image, Display
import time

display = Display()

trump = Image("trump.jpg")
#green = Image("green.jpg")

#edges = trump.edges(t1=100)
#(edges+trump).save(display)

blobs = trump.findBlobs(minsize=0.10 * 1200)
blobs.show()

#time.sleep(5)

#trump.save(display)

while not display.isDone():
    time.sleep(0.1)
