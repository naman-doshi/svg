import math
from svgflow.classdefs import *
from copy import deepcopy

# Haven't done much here yet but I plan to add all the utilities
# (not shapes themselves but functions that use them) e.g. moveTo
# here

canvasWidth = 0
canvasHeight = 0

# This is the template for the svg file
# Provided in Problem 5

# Rect intersection
def intersect(s1, s2):
    blax, blay, trax, tray = s1[0], s1[1], s1[2], s1[3]
    blbx, blby, trbx, trby = s2[0], s2[1], s2[2], s2[3]
    if blax > trbx or trax < blbx or blay > trby or tray < blby:
        return False
    else:
        return True

def collides(shape1, shape2, time):
    if isinstance(shape1, rectangle) and isinstance(shape2, rectangle):
        x1, y1 = shape1.locate(time)
        x2, y2 = shape2.locate(time)
        s1 = [x1-shape1.width/2, y1-shape1.height/2, x1+shape1.width/2, y1+shape1.height/2]
        s2 = [x2-shape2.width/2, y2-shape2.height/2, x2+shape2.width/2, y2+shape2.height/2]
        return intersect(s1, s2)
    if isinstance(shape1, circle) and isinstance(shape2, circle):
        x1, y1 = shape1.locate(time)
        x2, y2 = shape2.locate(time)
        dx = x1 - x2
        dy = y1 - y2
        ds = dx**2 + dy**2
        return ds**0.5 <= shape1.r + shape2.r
    assert 1==0, "Only collisions between 2x circle and 2x rectangle are supported"

def setTemplate(filename, width, height, createBG=True):
    global canvasWidth
    global canvasHeight
    canvasWidth = width
    canvasHeight = height
    template = open(filename, 'r').read()
    # this is just the header needed for all files
    # sorry for bad formattings
    other = f'''<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20001102//EN" 
"http://www.w3.org/TR/2000/CR-SVG-20001102/DTD/svg-20001102.dtd"> 

<svg width="{width}" height="{height}"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
    '''
    f.write(other)
    f.write(template)
    if createBG:
        f.write(f'\n<rect class="border" x="0" y="0" width="{width}" height="{height}" />')
        f.write('\n')

def radialDistribution(cx : float, cy : float, radius : float, numShapes : int, sampleShape, label=None):
    theta = 2 * math.pi / numShapes
    currentAngle = -theta
    shapes = []
    assert label == None or len(label) == numShapes, 'label must be None or have the same length as numShapes'
    for i in range(numShapes):
        currentAngle += theta
        x = -radius * math.sin(currentAngle) + cx
        y = -radius * math.cos(currentAngle) + cy
        x, y = round(x, 2), round(y, 2)
        if label is None:
            if isinstance(sampleShape, circle):
                shapes.append(deepcopy(circle(x, y, sampleShape.r, id=sampleShape.id, class_=sampleShape.class_, animations=sampleShape.animations)))
            elif isinstance(sampleShape, rectangle):
                shapes.append(deepcopy(rectangle(x - sampleShape.width/2, y - sampleShape.width / 2, sampleShape.width, sampleShape.height, id=sampleShape.id, class_=sampleShape.class_, animations=sampleShape.animations)))
            else:
                raise Exception('sampleShape must be a circle or a rectangle')
        else:
            if isinstance(sampleShape, labelledCircle):
                shapes.append(deepcopy(labelledCircle(x, y, sampleShape.r, label[i], id=sampleShape.id, class_=sampleShape.class_)))
            elif isinstance(sampleShape, labelledRectangle):
                shapes.append(deepcopy(labelledRectangle(x - sampleShape.width/2, y - sampleShape.width / 2, sampleShape.width, sampleShape.height, label[i], id=sampleShape.id, class_=sampleShape.class_)))
            else:
                raise Exception('sampleShape must be a labelledCircle or a labelledRectangle')
    return shapes
        
def generateGrid(rows : int, cols : int, x : float, y : float, sampleShape, label=None):
    '''
    labels is a list of labels for each shape, going from left to right, top to bottom
    '''
    if isinstance(sampleShape, circle):
        blockWidth = sampleShape.r * 2
        blockHeight = sampleShape.r * 2
    else:
        blockWidth = sampleShape.width
        blockHeight = sampleShape.height
    shapes = []
    assert label == None or len(label) == rows * cols, 'label must be None or have the same length as rows * cols'
    for i in range(rows):
        for j in range(cols):
            if label is None:
                if isinstance(sampleShape, circle):
                    shapes.append(deepcopy(circle(x + j * blockWidth, y + i * blockHeight, sampleShape.r, id=sampleShape.id, class_=sampleShape.class_, animations=sampleShape.animations)))
                elif isinstance(sampleShape, rectangle):
                    shapes.append(deepcopy(rectangle(x + j * blockWidth, y + i * blockHeight, sampleShape.width, sampleShape.height, id=sampleShape.id, class_=sampleShape.class_, animations=sampleShape.animations)))
                else:
                    raise Exception('sampleShape must be a circle or a rectangle')
            else:
                if isinstance(sampleShape, labelledCircle):
                    shapes.append(deepcopy(labelledCircle(x + j * blockWidth, y + i * blockHeight, sampleShape.r, label[i * cols + j], id=sampleShape.id, class_=sampleShape.class_)))
                elif isinstance(sampleShape, labelledRectangle):
                    shapes.append(deepcopy(labelledRectangle(x + j * blockWidth, y + i * blockHeight, sampleShape.width, sampleShape.height, label[i * cols + j], id=sampleShape.id, class_=sampleShape.class_)))
                else:
                    raise Exception('sampleShape must be a labelledCircle or a labelledRectangle')
    return shapes


def conclude():
    f.write('\n</svg>')
    f.close()

def addTitle(title):
    f.write(f'\n<text x="{canvasWidth/2}" y="{canvasHeight/12}">{title}</text>\n')




    
    
