import Image

im = Image.open("32_32_red_line.bmp")
#x = 0
#y = 0
width, height = im.size
#print "x,y of middle dot: " ,width/2,height/2

'''# draw a short line
x=10; y=10; im.putpixel( (x,y), (255,255,255) )
x=11; y=10; im.putpixel( (x,y), (255,255,255) )
x=12; y=10; im.putpixel( (x,y), (255,255,255) )'''

# Draw a white line on image
for x in range(0,32):
	y = x
	if y<31 and x<31:
		r,g,b = im.getpixel((x+1,y+1))
		im.putpixel((x,y),(255,255,255))
	while r==237:
		x += 1
		im.putpixel((x,y),(255,255,255))
		r,g,b = im.getpixel((x,y+1))
		if r!=237:
			break	
	else:
		continue
	a,b = x,y
	break
r,g,b = im.getpixel((x,y+1))
if r != 237:
	for x in range(a,32):
		y+=1
		im.putpixel((x,y),(255,255,255))
	
				
	
		
#print values of pixels
for y in range(0,height):
    for x in range(0,width):
	r,g,b = im.getpixel((x,y))
        print "x,y:", x,y, "r,g,b:", r,g,b	
	




#print values of red dot
#print "x,y of red dot: ", a,c
# show the image
im.show()
