from svgflow.main import *
from svgflow.classdefs import *
from copy import deepcopy
import time

# You may need to run this code twice to generate output, or maybe it's a quirk with my laptop

tem = setTemplate('template.svg', 1000, 1000)
rect = circle(450, 150, 50, class_=['unordered'])
rect2 = circle(450, 750, 50, class_=['unordered'])

a1 = animation()
a1.addImplicit('cy', 700, 5, 0)
rect.add(a1)

obc = deepcopy(rectangle(x=100, y=100, width=50, height=50))
hide = deepcopy(animation())
hide.addImplicit('opacity', 0, 0.01, 0)
obc.add(hide)
show = deepcopy(animation())

rect2.moveTo(obc, 0, 13)

#Havent accounted for enlargements in intersections yet
#rect.scale(2, 0, 1)

rect.draw()
rect2.draw()

def spawnObject(j):
  show.addImplicit('opacity', 1, 0.01, j)
  obc.add(show)
  obc.draw()


for i in range(0, 51):
  j = i/10
  if collides(rect, rect2, j):
    spawnObject(j)
    print(f'intersection at time {j}')
    break