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
resized = img.scale(90,90)
#show image object and wait for user to press ENTER
resized.show()
raw_input("scaled image is displayed. Press Enter to continue >")

print "\ncreate double size copy of the image, by factor"
scaled = img.scale(2)
#show image object and wait for user to press ENTER
scaled.show()
raw_input("scaled image is displayed. Press Enter to continue >")

print "\ncreate rotated copy of the image, by factor"
rotated = img.rotate(90)
rotated.show()
raw_input("rotated image is displayed. Press Enter to continue >")


#cut part of the image
cropped = img.crop(100, 100, 50, 50)

#show image object and wait for user to press ENTER
cropped.show()
raw_input("\nCorped image is displayed. Press Enter to continue >")

print "split image into channels and unite again"
(r,g,b)=img.splitChannels()
#new = img.mergeChannels(None,b,g)
new = img.mergeChannels(r,b,g)

#convert image to grey
img.toGray().show()
raw_input("\ngraged image is displayed. Press Enter to continue >")

print "Two operations at once: edges and invert:"
img.invert().edges().show()
raw_input("\nEdges of inverted image is displayed. Press Enter to continue >")


print "\nDetecting the yellow car"
car = Image("images/car.png")
yellow_car = car.colorDistance(Color.YELLOW)
only_car = car - yellow_car
print "The mean color is", only_car.meanColor()

#get distance from specified RGP color
imgDiffFromBlue = img.colorDistance( (21, 28, 63) )   #R, G, B

car.sideBySide(yellow_car).sideBySide(only_car).show() #show sidebyside
raw_input("\nDisplaying few images side by side: car, yellow_car, only_car Press Enter to continue >")


print "=========================="
print "Advanced exmples: finding features"
print "\nfind blobs of color"
blobs = img.findBlobs()
print "The first blog:", blobs[0]
print "The last blog:", blobs[-1]
print "blobs are returned in order of area, smallest first"
print "largest blob at ", blobs[-1].x, ", ", blobs[-1].y
img.findBlobs().show(autocolor=True)
raw_input("Press Enter to continue >")

print "\nfind corners"
corners = img.findCorners()
print
print "Number of corners found:", len(corners)
print "x of first corner is at", corners[0].x, "yof first corner is at", corners[0].y



print "\nfind blobs of color"
blobs = img.findBlobs()
print "The first blog:", blobs[0]
print "The last blog:", blobs[-1]
print "blobs are returned in order of area, smallest first"
print "largest blob at ", blobs[-1].x, ", ", blobs[-1].y
img.findBlobs().show(autocolor=True)
raw_input("Press Enter to continue >")

print "\nfind corners"
corners = img.findCorners()
print
print "Number of corners found:", len(corners)
print "x of first corner is at", corners[0].x, "yof first corner is at", corners[0].y



#split image into channels and unite again
#get blobs
screensize = img.width * img.height
min_blob_size = 0.10 * screensize # the minimum blob is at least 10% of screen
max_blob_size = 0.80 * screensize # the maximum blob is at most 80% of screen
blobs = img.findBlobs(minsize=min_blob_size, maxsize=max_blob_size) # get the largest blob on the screen



#Find edges of image
img = img.edges()

# find lines in image
lines = img.findLines()
#find longest line
longest_line = lines.sortLength()[0]

#find match of small pic in big pic
t = 5
#methods = ["SQR_DIFF","SQR_DIFF_NORM","CCOEFF","CCOEFF_NORM","CCORR","CCORR_NORM"] # the various types of template matching
m = "CCOEFF"
dl = DrawingLayer((img.width,img.height))
fs = img.findTemplate(template,threshold=t,method=m)
for match in fs:
    if match.y<38: continue #upper end of the pics is legit logos, matches not relevant
    dl.rectangle((match.x,match.y),(match.width(),match.height()),color=Color.RED)

