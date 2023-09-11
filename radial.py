from svgflow.main import *
from svgflow.classdefs import *
from copy import deepcopy
import time

tem = setTemplate('template.svg', 1000, 1000)

shapes = radialDistribution(500, 500, 400, 5, labelledRectangle(0, 0, 100, 100, 0, class_=['unordered']), label = [1, 2, 3, 4, 5])


for shape in shapes:
    shape.draw()