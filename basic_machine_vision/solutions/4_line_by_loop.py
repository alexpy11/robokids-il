import Image, sys, os

im = Image.open("32_32_red_dot.bmp")
width, height = im.size


for i in range(height):
    x = i; y = i  
    im.putpixel( (x,y), (255,255,255) )

im.show()
#x = raw_input("Press Enter")
