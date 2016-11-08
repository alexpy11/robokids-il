import Image

im = Image.open("32_32_red_dot.bmp")
x = 0
y = 0
width, height = im.size


# draw a short line
x=10; y=10; im.putpixel( (x,y), (255,255,255) )
x=11; y=10; im.putpixel( (x,y), (255,255,255) )
x=12; y=10; im.putpixel( (x,y), (255,255,255) )

# print values of pixels
for y in range(0,height):
    for x in range(0,width):
        r,g,b = im.getpixel((x,y))
        print "x,y:", x,y, "r,g,b:", r,g,b

# show the image
im.show()
