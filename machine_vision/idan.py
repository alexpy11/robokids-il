# credit to https://www.youtube.com/watch?v=jihxqg3kr-g

import SimpleCV

display = SimpleCV.Display()
cam = SimpleCV.Camera()
normalDisplay = True

while display.isNotDone():
    
    if display.mouseRight:
        normalDisplay = not(normalDisplay)
        print ("Normal mode: " + str(normalDisplay))


    img = cam.getImage().flipHorizontal()
    #dist= img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
    (red, green, blue) = img.splitChannels()
    greenImg = img.mergeChannels (green, green, green)
    blueImg = img.mergeChannels (blue, blue, blue)
    redImg = img.mergeChannels (red, red, red)
    dist = (greenImg - blueImg) + (greenImg - redImg)
    blobs = dist.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.2) for b in blobs])
        if circles:
            #img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(), SimpleCV.Color.BLUE, 5)
            for circle in circles :
                img.drawCircle((circle.x, circle.y), circle.radius(), SimpleCV.Color.BLUE, 1)
            
    if normalDisplay:
        img.show()
    else:
        dist.show()
