f = open('image.svg', 'w')

# Haven't done much here yet but I plan to add all the utilities
# (not shapes themselves but functions that use them) e.g. moveTo
# here

canvasWidth = 0
canvasHeight = 0

# This is the template for the svg file
# Provided in Problem 5

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

def conclude():
    f.write('\n</svg>')
    f.close()

def addTitle(title):
    f.write(f'\n<text x="{canvasWidth/2}" y="{canvasHeight/12}">{title}</text>\n')




    
    
