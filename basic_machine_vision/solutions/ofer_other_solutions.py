from PIL import Image

def red_line():
    img = Image.open("32_32_red_line.bmp")
    width, height = img.size

    x, y = 0, 0
    while y < height-1 and x < width-1:
        img.putpixel((x, y), (255,255,255))
        if img.getpixel((x+1, y+1)) == (0, 0, 0):
            y += 1
        x += 1

    img.putpixel((x, y), (255,255,255))

    # show the image
    img.show()
    img.save("red_line_solution.bmp")

def red_corner():
    img = Image.open("32_32_red_corner.bmp")
    width, height = img.size

    x, y = 0, 0
    while y < height-1 and x < width-1:
        img.putpixel((x, y), (255,255,255))
        if img.getpixel((x+1, y+1)) == (0, 0, 0):
            x += 1
            y += 1
        elif img.getpixel((x, y+1)) == (0, 0, 0):
            y += 1
        else: #if img.getpixel((x+1, y)) == (0, 0, 0):
            y -= 1
    
    img.putpixel((x, y), (255,255,255))

    # show the image
    img.show()
    img.save("red_corner_solution.bmp")

red_line()
red_corner()
