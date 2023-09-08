from svgflow.main import *
from svgflow.classdefs import *
from copy import deepcopy
import time

# You may need to run this code twice to generate output, or maybe it's a quirk with my laptop

tem = setTemplate('template.svg', 1000, 1000)
rect = rectangle(level=0, x=400, y=100, width=100, height=100, class_=['unordered'])
rect2 = rectangle(level=0, x=400, y=700, width=100, height=100, class_=['unordered'])

a1 = animation()
a1.addImplicit('y', 700, 5, 0)
rect.add(a1)

a2 = animation()
a2.addImplicit('y', 100, 5, 0)
rect2.add(a2)

#Havent accounted for enlargements in intersections yet
#rect.scale(2, 0, 1)

rect.draw()
rect2.draw()

def spawnObject(j):
  obc = deepcopy(rectangle(level=0, x=100, y=100, width=50, height=50))
  hide = deepcopy(animation())
  hide.addImplicit('opacity', 0, 0.01, 0)
  obc.add(hide)
  show = deepcopy(animation())
  show.addImplicit('opacity', 1, 0.01, j)
  obc.add(show)
  obc.draw()


for i in range(0, 51):
  j = i/10
  x1, y1 = rect.locate(j)
  x2, y2 = rect2.locate(j)
  s1 = [x1-50, y1-50, x1+50, y1+50]
  s2 = [x2-50, y2-50, x2+50, y2+50]
  if intersect(s1, s2):
    spawnObject(j)
    print(f'intersection at time {j}')
    break

