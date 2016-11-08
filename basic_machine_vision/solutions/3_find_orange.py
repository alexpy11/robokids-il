import Image

im = Image.open("orange_small.bmp")
x = 0
y = 0
width, height = im.size
print width,height


for y in range(0,height,10):
    for x in range(0,width,10):
        r,g,b = im.getpixel((x,y))
        #if b<100 and b>xxx and r>yyy:
        if b<100 :
             im.putpixel( (x,y), (0,0,255) )
             print x,y,"  ",r,g,b
im.show()
