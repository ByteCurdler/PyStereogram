from PIL import Image
from random import randint

def main(tilesize, imsize):
    dots = []

    for i in range(tilesize*tilesize):
        if randint(0,1):
            dots.append(
                (randint(0,127), randint(0,127), randint(0,127))
            )
        else:
            dots.append(
                (randint(127,255), randint(127,255), randint(127,255))
            )

    ##for i in range(50):
    ##    dots.append((i%2*255, 0, 0))

    tile = Image.new('RGB', (tilesize,tilesize))
    tile.putdata(dots)                 

    img = Image.new('RGB', imsize)
    for x in range(0, imsize[0], tilesize):
        for y in range(0, imsize[1], tilesize):
    ##        print(left, top)
            img.paste(tile, (x, y))

    dot = Image.new('RGB', (10,10))
    dot.putdata([(255,0,0)] * 100) 
    
    for x in range(20, imsize[0], tilesize):
        img.paste(dot, (x, 10))
        img.paste(dot, (x, imsize[1]-20))
    
    img.save('BaseAuto.png')
    tile.save('BaseAuto.tile.png')

if __name__ == "__main__":
    main(50, (600,400))
