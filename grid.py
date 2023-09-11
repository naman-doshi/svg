from svgflow.main import *
from svgflow.classdefs import *
from copy import deepcopy
import time

tem = setTemplate('template.svg', 1000, 1000)
shapes = generateGrid(4, 5, 200, 200, rectangle(0, 0, 100, 100, class_=['unordered']))
for shape in shapes:
    shape.draw()