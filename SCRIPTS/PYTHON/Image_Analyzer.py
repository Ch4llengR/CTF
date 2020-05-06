from PIL import Image

newimage2 = Image.open("XXXXX.png")
pix = newimage2.load()
x = 0
while x < newimage2.width:
        y = 0
        while y < newimage2.height:
                print(pix[x,y])
                y += 1
        x += 1
		
#Browse a picture pixel by pixel with pillow library