# Using Blender
Instead of trying to draw a depthmap, why not generate one from 3-D?
## Step 1: Prepare
1. Download Blender at https://www.blender.org
2. Open ObjectToDepthmap.blend

Note: Do NOT move the camera
## Step 2: Get a 3-D model
1. Get any desired 3-D model and import it into Blender
2. Go to Properties Screen->Material
3. Set the Material to "F Z-Dist"
4. Go to the 3-D View screen
5. Set Viewport Shading to "Material"
## Step 3: Fiddle with the settings
1. In the Outliner screen, select your object
2. Go to the Node Editor screen
3. Fiddle with the Add and Multiply values until:
    1. The furthest visible point is not black, but close, and
    2. The closest visible point is not white, but close
    
    Note: the Multiply value should _always_ be negative
## Step 4: Export and Crop
1. In the Info toolbar, click Render->Render Image
2. In the UV/Image Editor toolbar that pops up, click Image->Save as image
3. Save your image anywhere
4. Open your favourite image editing software and crop the image to the desired area
5. Save the modified image
## Done!
Now point PyStereogram.py towards your image, then look in the `Output/` folder for your new image!
