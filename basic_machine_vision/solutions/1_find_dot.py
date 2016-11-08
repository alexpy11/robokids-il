import Image

im = Image.open("32_32_red_dot.bmp")
x = 0
y = 0
width, height = im.size



for y in range(0,height):
    for x in range(0,width):
        r,g,b = im.getpixel((x,y))
	if r > 1:
            print 'the coordinates are: ('+str(x)+','+str(y)+')'

#im.show()
