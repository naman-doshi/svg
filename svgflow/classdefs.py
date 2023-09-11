f  = open('image.svg', 'a')

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

class animation:
    # attributeName can be anything: x, y, fill, stroke etc.
    '''
    Implicit = moving the object from A to B, and assigning an obvious time
    Explicit = specifying values and keytimes
    '''
    def __init__(self, isRepeat=None):
        self.isRepeat = isRepeat
        self.dataType = "animation"
        self.type_ = ''
    
    def addImplicit(self, attributeName : str, to, dur : float, begin : float, fill="freeze"):
        self.attributeName = attributeName
        self.type_ = 'implicit'
        self.to = to
        self.dur = dur
        self.begin = begin 
        self.fill = fill

    def addExplicit(self, attributeName, values : list[float], begin : float, dur : float, keyTimes=[], fill="freeze"):
        self.attributeName = attributeName
        self.type_ = 'explicit'
        self.values = list(map(str, values))
        self.keyTimes = list(map(str, keyTimes))
        self.fill = fill
        self.dur = dur
        self.begin = begin
        if self.keyTimes == []:
            self.keyTimes = [i/(len(self.values)-1) for i in range(len(self.values))]
    
    def addRepeat(self, isCountorDur : bool, val : int):
        self.isRepeat = isCountorDur
        self.repeat = val

    def generate(self, indent=1):
        ind = indent * '  '
        if self.type_ == "implicit":
            return f'{ind}<animate attributeName="{self.attributeName}" fill="{self.fill}" begin="{self.begin}s" dur="{self.dur}s" to="{self.to}" />\n'
        
        elif self.type_ == "explicit":
              assert len(self.values) == len(self.keyTimes) or len(self.keyTimes) == 0, "Length of values and keyTimes must be equal"
              assert self.values[0] == self.values[-1], "First and last value must be the same"

              if self.isRepeat == None:
                  assert 1 == 0, "Must specify repeatCount or repeatDur"

              assert float(self.keyTimes[0]) == 0 and float(self.keyTimes[-1]) == 1, "First keyTime must be 0 and last keyTime must be 1" 
              
              self.keyTimes = list(map(str, self.keyTimes))

              if self.isRepeat:
                  return f'{ind}<animate attributeName="{self.attributeName}"  begin="{self.begin}" dur="{self.dur}s"  repeatCount="{self.repeat}" fill="{self.fill}" values="{";".join(self.values)}" keyTimes="{";".join(self.keyTimes)}"/>\n'
              else:
                  return f'{ind}<animate attributeName="{self.attributeName}" begin="{self.begin}" fill="{self.fill}" values="{";".join(self.values)}" keyTimes="{";".join(self.keyTimes)}" repeatDur="{self.repeat}" dur="{self.dur}/>\n'
            

class animateTransform:
    '''
    Reminder: translates are relative to the object's original position
    These are still WIP
    '''
    def __init__(self, type : str, begin : float, dur : float, to, from_="", fill="freeze", additive=None):
        self.attributeName = "transform"
        self.type_ = type
        self.to = to
        self.dur = dur
        self.fill = fill
        self.begin = begin
        self.from_ = from_
        self.additive = additive
        self.dataType = "transform"
    
    
    def generate(self, indent=1):
        if self.from_ == "":
           if self.additive:
               return f'{"  "*indent}<animateTransform attributeName="{self.attributeName}" type="{self.type_}" begin="{self.begin}s"  to="{self.to}" dur="{self.dur}s" fill="{self.fill}" additive={self.additive} />\n'
           return f'{"  "*indent}<animateTransform attributeName="{self.attributeName}" type="{self.type_}" begin="{self.begin}s"  to="{self.to}" dur="{self.dur}s" fill="{self.fill}" />\n'
        else:
            if self.additive:
                return f'{"  "*indent}<animateTransform attributeName="{self.attributeName}" type="{self.type_}" begin="{self.begin}s" from="{self.from_}" to="{self.to}" dur="{self.dur}s" fill="{self.fill}" additive={self.additive} />\n'
            return f'{"  "*indent}<animateTransform attributeName="{self.attributeName}" type="{self.type_}" begin="{self.begin}s" from="{self.from_}" to="{self.to}" dur="{self.dur}s" fill="{self.fill}" />\n'  

class line:
    def __init__(self, x1, y1, x2, y2, opacity="", class_=None, animations=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.opacity = opacity
        if class_ == None:
            self.class_ = []
        else:
            self.class_ = class_
        if animations == None:
            self.animations = []
        else:
            self.animations = animations
    
    def addAnimation(self, anim):
        self.animations.append(anim)

    def deleteClass(self, clas):
        self.class_.remove(clas)

    def addClass(self, clas):
        self.class_.append(clas)

    def draw(self):
        f.write(f'<line class="{" ".join(self.class_)}" x1="{self.x1}" y1="{self.y1}" x2="{self.x2}" y2="{self.y2}" opacity="{self.opacity}" >\n')
        for anim in self.animations:
            f.write(anim.generate())
        f.write('</line>\n')

class rectangle:
    '''
    optional: rx (border radius) — yet to implement
    '''
    def __init__(self, level, x, y, width, height, id="", class_=None, filter="", animations=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if class_ == None:
            self.class_ = []
        else:
            self.class_ = class_
        if animations == None:
            self.animations = []
        else:
            self.animations = animations
        self.id = id
        self.filter = filter
        self.level = level
        self.validAnimations = []

    def locate(self, time):
        x = self.x
        y = self.y
        for anim in self.validAnimations:
            if anim.attributeName != 'x' and anim.attributeName != 'y':
                continue
            
            if anim.dataType == "animation" and anim.type_ == "implicit":
                if time >= anim.begin + anim.dur:
                    if anim.attributeName == "x":
                        x = anim.to
                    elif anim.attributeName == "y":
                        y = anim.to
                
                if anim.begin <= time and time <= anim.begin + anim.dur:
                    elapsed = (time - anim.begin) / anim.dur
                    if anim.attributeName == "x":
                        x += (anim.to - x) * elapsed
                    elif anim.attributeName == "y":
                        y += (anim.to - y) * elapsed

            elif anim.dataType == "animation" and anim.type_ == "explicit":
                totalDur = 0
                if anim.isRepeat:
                    totalDur = anim.dur * anim.repeat
                else:
                    totalDur = anim.repeat


                if time >= anim.begin and time <= totalDur:
                    elapsed = time - anim.begin
                    elapsed %= anim.dur
                    elapsed /= anim.dur

                    # Find first element in keyTimes larger than elapsed
                    i = 0
                    while i < len(anim.keyTimes):
                        if float(anim.keyTimes[i]) > elapsed:
                            break
                        else:
                            i += 1
                    elapsed -= float(anim.keyTimes[i-1])
                    goingTo = anim.values[i]
                    prev = anim.values[i-1]

                    if anim.attributeName == "x":
                        x = (float(goingTo) - float(prev)) * elapsed + float(prev)
                    elif anim.attributeName == "y":
                        y = (float(goingTo) - float(prev)) * elapsed + float(prev)

            elif anim.dataType == "transform" and anim.type_ == 'translate':
                # we assume it's not additive
                # this is a WIP
                if anim.begin <= time and time <= anim.begin + anim.dur:
                    pass

        return (x + self.width / 2, y + self.height / 2)

    def rotate(self, angle, begin, dur):
        cx = self.x + self.width/2
        cy = self.y + self.height/2
        anim = animateTransform('rotate', begin, dur, f"{angle} {cx} {cy}", from_=f"0 {cx} {cy}")
        self.animations.append(anim)

    def scale(self, size, begin, dur):
        cx = (size-1)*(self.x + self.width/2)*-1
        cy = (size-1)*(self.y + self.height/2)*-1
        self.animations.append(animateTransform('translate', begin, dur, f"{cx} {cy}", from_=f"0 0"))
        self.animations.append(animateTransform('scale', begin, dur, size, from_=f"1", additive="sum"))
    
    def add(self, anim):
        self.animations.append(anim)
        self.validAnimations.append(anim)

    def deleteClass(self, clas):
        self.class_.remove(clas)

    def addClass(self, clas):
        self.class_.append(clas)

    def draw(self):
        f.write(f'{"  "*self.level}<rect id="{self.id}" class="{" ".join(self.class_)}" filter="{self.filter}" x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" >\n')
        for anim in self.animations:
            f.write(anim.generate(self.level+1))
        f.write(f'{"  "*self.level}</rect>\n')

class circle:
    def __init__(self, cx, cy, r, id="", class_=None, animations=None):
        self.cx = cx
        self.cy = cy
        self.r = r
        if class_ == None:
            self.class_ = []
        else:
            self.class_ = class_
        if animations == None:
            self.animations = []
        else:
            self.animations = animations
        self.id = id
        self.validAnimations = []
    
    def locate(self, time):
        x = self.cx
        y = self.cy
        for anim in self.validAnimations:
            if anim.attributeName != 'cx' and anim.attributeName != 'cy':
                continue
            
            if anim.dataType == "animation" and anim.type_ == "implicit":
                if time >= anim.begin + anim.dur:
                    if anim.attributeName == "cx":
                        x = anim.to
                    elif anim.attributeName == "cy":
                        y = anim.to
                
                if anim.begin <= time and time <= anim.begin + anim.dur:
                    elapsed = (time - anim.begin) / anim.dur
                    if anim.attributeName == "cx":
                        x += (anim.to - x) * elapsed
                    elif anim.attributeName == "cy":
                        y += (anim.to - y) * elapsed

            elif anim.dataType == "animation" and anim.type_ == "explicit":
                totalDur = 0
                if anim.isRepeat:
                    totalDur = anim.dur * anim.repeat
                else:
                    totalDur = anim.repeat


                if time >= anim.begin and time <= totalDur:
                    elapsed = time - anim.begin
                    elapsed %= anim.dur
                    elapsed /= anim.dur

                    # Find first element in keyTimes larger than elapsed
                    i = 0
                    while i < len(anim.keyTimes):
                        if float(anim.keyTimes[i]) > elapsed:
                            break
                        else:
                            i += 1
                    elapsed -= float(anim.keyTimes[i-1])
                    goingTo = anim.values[i]
                    prev = anim.values[i-1]

                    if anim.attributeName == "cx":
                        x = (float(goingTo) - float(prev)) * elapsed + float(prev)
                    elif anim.attributeName == "yy":
                        y = (float(goingTo) - float(prev)) * elapsed + float(prev)

            elif anim.dataType == "transform" and anim.type_ == 'translate':
                # we assume it's not additive
                # this is a WIP
                if anim.begin <= time and time <= anim.begin + anim.dur:
                    pass

        return (x, y)

    # Might work, havent tested on circle
    def scale(self, size, begin, dur):
        cx = (size-1)*cx*-1
        cy = (size-1)*cy*-1
        self.animations.append(animateTransform('translate', begin, dur, f"{cx} {cy}", from_="0 0"))
        self.animations.append(animateTransform('scale', begin, dur, size, from_="1", additive="sum"))
    
    def add(self, anim):
        self.animations.append(anim)
        self.validAnimations.append(anim)

    def deleteClass(self, clas):
        self.class_.remove(clas)

    def addClass(self, clas):
        self.class_.append(clas)

    def draw(self):
        f.write(f'<circle id="{self.id}" class="{" ".join(self.class_)}" cx="{self.cx}" cy="{self.cy}" r="{self.r}" >\n')
        for anim in self.animations:
            f.write(anim.generate())
        f.write('</circle>\n')

class text:
    def __init__(self, x, y, text, id="", class_=None, animations=None):
        self.x = x
        self.y = y
        self.text = text
        if class_ == None:
            self.class_ = []
        else:
            self.class_ = class_
        if animations == None:
            self.animations = []
        else:
            self.animations = animations
        self.id = id
    
    def addAnimation(self, anim):
        self.animations.append(anim)

    def deleteClass(self, clas):
        self.class_.remove(clas)

    def addClass(self, clas):
        self.class_.append(clas)

    def draw(self):
        f.write(f'<text id="{self.id}" class="{" ".join(self.class_)}" x="{self.x}" y="{self.y}" >\n')
        for anim in self.animations:
            f.write(anim.generate())
        f.write(f'{self.text}</text>\n')

class ellipse:
    def __init__(self, cx, cy, rx, ry, id="", class_=None, animations=None):
        self.cx = cx
        self.cy = cy
        self.rx = rx
        self.ry = ry
        if class_ == None:
            self.class_ = []
        else:
            self.class_ = class_
        if animations == None:
            self.animations = []
        else:
            self.animations = animations
        self.id = id
    
    def addAnimation(self, anim):
        self.animations.append(anim)

    def deleteClass(self, clas):
        self.class_.remove(clas)

    def addClass(self, clas):
        self.class_.append(clas)

    def draw(self):
        f.write(f'<ellipse id="{self.id}" class="{" ".join(self.class_)}" cx="{self.cx}" cy="{self.cy}" rx="{self.rx}" ry="{self.ry}" >\n')
        for anim in self.animations:
            f.write(anim.generate())
        f.write('</ellipse>\n')


class group:
    def __init__(self, x, y, id="", class_=None, animations=None, shapes=None):
        self.x = x
        self.y = y
        self.id = id

        if class_ == None:
            self.class_ = []
        else:
            self.class_ = class_
        if animations == None:
            self.animations = []
        else:
            self.animations = animations
        if shapes == None:
            self.shapes = []
        else:
            self.shapes = shapes
        
    
    def addAnimation(self, anim):
        self.animations.append(anim)

    def deleteClass(self, clas):
        self.class_.remove(clas)

    def addClass(self, clas):
        self.class_.append(clas)

    def addShape(self, shape):
        self.shapes.append(shape)
    
    def draw(self):
        f.write(f'<g id="{self.id}" class="{" ".join(self.class_)}" transform="translate({self.x}, {self.y})" >\n')
        for anim in self.animations:
            f.write(anim.generate())
        for shape in self.shapes:
            shape.draw()
        f.write('</g>\n')