import Image

def isPixelOk(x,y):
     pointOk = True
     if x<0 or y<0: pointOk = False
     if x>=width or y>=height: pointOk = False
     if pointOk:
         r,g,b = im.getpixel((x,y))
         if r>0: pointOk = False
     if pointOk:
         print x,y
     return pointOk

im = Image.open("32_32_red_line.bmp")
width, height = im.size

x = 0; y = 0; im.putpixel( (x,y), (0,0,255) )

while ((x<width-1) or (y<height-1)) :
 
    tryX = x + 1
    if isPixelOk(tryX,y): 
        x = tryX

    tryY = y + 1
    if isPixelOk(x,tryY): 
        y = tryY
    
    im.putpixel( (x,y), (0,0,255) )
    
print "Good new point: ",x,y
  

im.show()

  

  
