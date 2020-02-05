#Imports
from PIL import Image, GifImagePlugin
import numpy as np
import sys

TILESIZE=50

##  TODO: Custom delay
##  TODO: Move BG

#Get input
depthImName = sys.argv[1:2]
if depthImName == []:
    depthImName = input("Depthmap? ")
    depthImName = ("Depth.png" if depthImName == "" else depthImName)
else:
    depthImName = depthImName[0]

movement = sys.argv[2:3]
if movement == []:
    movement = 20
else:
    movement = movement[0]

#Open depthmap
try:
    depthAll = Image.open(depthImName)
except FileNotFoundError:
    depthAll = Image.open("Input/" + depthImName)

outputGIF = []

for frame in range(0,depthAll.n_frames):
    print("Creating tile...")
    import MakeBG
    MakeBG.main(TILESIZE,np.array(depthAll).shape[1::-1])

    print("Opening images...")
    base = np.array(Image.open("BaseAuto.png"))
    
    depthAll.seek(frame)
    depth = np.array(depthAll)
    print("Creating arrays...")
    depth -= depth.min()
    depth = depth * ((TILESIZE / 3) / depth.max())
    #depth = (depth * -1) + (depth.max())
    diffmap = []
    newImage = []
    for i in range(base.shape[1]):
        diffmap.append([0] * base.shape[0])
        newImage.append([0] * base.shape[0])

    print("Calculating shift...")
    for x in range(len(diffmap)-1,-1,-1):
        for y in range(len(diffmap[0])):
            tmp = depthAll.palette.palette[int(depth[y][x])*3]
            if x < len(diffmap) - ((TILESIZE) + int(tmp)):
                tmp += diffmap[x+(TILESIZE)-int(tmp)][y]
            diffmap[x][y] = int(tmp)

    print("Creating images...")
    for x in range(len(diffmap)-1,-1,-1):
        for y in range(len(diffmap[0])):
            newImage[x][y] = tuple(base[y][(x-diffmap[x][y]) % base.shape[1]])

    im = []
    for i in range(len(diffmap[0])):
        im += [newImage[j][i] for j in range(len(diffmap))]

    img = Image.new('RGB', (len(diffmap), len(diffmap[0])))
    img.putdata(im)
    outputGIF.append(img)

outputGIF[0].save('Output/%s' % depthImName.split("/")[-1],
                  save_all=True,
                  append_images=outputGIF[1:],
                  duration=200,
                  loop=0)

print("Done!")
