from SimpleCV import *

# create image object by reading file
img = Image("images/donkey.jpg")


#get width and height of image
width = img.width;  height = img.height
print "width is", width, "height is", height

#show image object and wait for user to press ENTER
img.show()
raw_input("image is displayed. Press Enter to continue >")

#save image
img.save("new_donkey.jpg")
print "image was saved as new_donkey.jpg"

print "Show circle on the image"
circlelayer = DrawingLayer((img.width, img.height))
center_point = (img.width/2, img.height/2)
circlelayer.circle(center_point, 80, Color.RED)
img.addDrawingLayer(circlelayer)
img.applyLayers()
img.show()
raw_input("cirle is displayed. Press Enter to continue >")

#clone the imgage
clone = img.copy()

print "\ncreate re-sized copy of the image, by specifing width and hight"
resized = img.scale(360,500)
#show image object and wait for user to press ENTER
resized.show()
raw_input("scaled image is displayed. Press Enter to continue >")

print "\ncreate rotated copy of the image, by factor"
rotated = img.rotate(90)
rotated.show()
raw_input("rotated image is displayed. Press Enter to continue >")

#cut part of the image
cropped = img.crop(200, 200, 200, 200)

#show image object and wait for user to press ENTER
cropped.show()
raw_input("\nCorped image is displayed. Press Enter to continue >")

print "split image into channels and unite again"
(r,g,b)=img.splitChannels()
new = img.mergeChannels(r,b,None)
#new = img.mergeChannels(r,b,g)
raw_input("\nno green image is displayed. Press Enter to continue >")
new.show()

#convert image to grey
img.toGray().show()
raw_input("\ngraged image is displayed. Press Enter to continue >")
