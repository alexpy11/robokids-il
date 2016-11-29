from PIL import Image
from collections import defaultdict

#img = img.crop((int(0.25*width), int(0.25*height), int(0.5*width), int(0.5*height)))

if True and False:
    img = Image.open("orange.JPG")
    width, height = img.size
    for y in range(0,height):
        for x in range(0,width):
            color = img.getpixel((x,y))
            if color[2] < 100:
	        img.putpixel((x,y), (0,0,0))
            else:
                img.putpixel((x, y), (255,255,255))

    print("Thresholded")
    img.save("first_thresh_orange.jpg")
    img.show()
else:
    img = Image.open("first_thresh_orange.jpg")
    width, height = img.size

for y in range(height):
    for x in range(width):
        neighbors = img.crop((x-5, y-5, 10, 10))
        counter = defaultdict(int)
        for pixel in neighbors.getdata():
            counter[pixel] += 1
        if counter[(0, 0, 0)] > (sum(counter.values()) / 2):
            img.putpixel((x,y), (0, 0, 0))
        else:
            img.putpixel((x, y), (255, 255, 255))

img.save("black_white_orange.jpg")

# show the image
img.show()

