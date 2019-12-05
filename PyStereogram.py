#Imports
from PIL import Image
import numpy as np
import sys

TILESIZE=50

#Get input
depthImName = sys.argv[1:2]
if depthImName == []:
    depthImName = input("Depthmap? ")
    depthImName = ("Depth.png" if depthImName == "" else depthImName)
else:
    depthImName = depthImName[0]

#Open depthmap
try:
    depth = np.array(Image.open(depthImName))
except FileNotFoundError:
    depth = np.array(Image.open("Input/" + depthImName))

print("Creating tile...")
import MakeBG
MakeBG.main(TILESIZE,depth.shape[1::-1])

print("Opening images...")
base = np.array(Image.open("BaseAuto.png"))
assert base.shape[:2] == depth.shape[:2], "Base and depthmap differ in size."

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
        tmp = depth[y][x][0]
        if x < len(diffmap) - ((TILESIZE) + int(tmp)):
            tmp += diffmap[x+(TILESIZE)-int(tmp)][y]
        diffmap[x][y] = int(tmp)

print("Creating images...")
for x in range(len(diffmap)-1,-1,-1):
    for y in range(len(diffmap[0])):
        newImage[x][y] = tuple(base[y][(x-diffmap[x][y]) % base.shape[1]])

def bound(n):
    return int(
        (
            ((n + (TILESIZE/2)) % TILESIZE) - (TILESIZE/2)
        ) * 255/TILESIZE
    )

difflist = []
for i in range(len(diffmap[0])):
    difflist += [(-bound(diffmap[j][i]), bound(diffmap[j][i]), 0) for j in range(len(diffmap))]

img = Image.new('RGB', (len(diffmap), len(diffmap[0])))
img.putdata(difflist)
img.save('trueDepth.png')

del difflist
im = []
for i in range(len(diffmap[0])):
    im += [newImage[j][i] for j in range(len(diffmap))]

img = Image.new('RGB', (len(diffmap), len(diffmap[0])))
img.putdata(im)
img.save('Output/%s' % depthImName.split("/")[-1])

print("Done!")
