#coding: utf-8

import datetime
import logging
import sys
import os

# study inheritance

class animal(object):

    spacer = "  "   # class-level variable used by all instances

    def __init__(self, nofLegs="", wildDomestic="", flyNoFly=""):
        self.nofLegs = nofLegs
        self.wildDomestic = wildDomestic
        self.flyNoFly = flyNoFly

    def displayAttributes(self):
        report = "\n"
        report += "animal Obj" + self.spacer
        report += "legs: "+str(self.nofLegs) + self.spacer
        report += "Fly?: "+self.flyNoFly + self.spacer
        report += "Domestic or Wild? "+self.wildDomestic + self.spacer  
        return report   


class dog(animal):

    def __init__(self, type=""):
        self.type = type

    def makeASound(self):
        return "I make the sound: woof, woof!"

    def displayAttributes2(self):
        report = "\n"
        report += "in dog Obj" + self.spacer
        report += "type: " + self.type + self.spacer
        report += "legs: "+str(self.nofLegs) + self.spacer
        report += "Fly?: "+self.flyNoFly + self.spacer
        report += "Domestic or Wild? "+self.wildDomestic + self.spacer 
        report += self.makeASound() 
        return report

    def displayAttributes(self):
        report = "\n"
        report += "in dog Obj" + self.spacer
        report += "type: " + self.type + self.spacer
        report += animal.displayAttributes(self)
        ##report += "legs: "+str(self.nofLegs) + self.spacer
        ##report += "Fly?: "+self.flyNoFly + self.spacer
        ##report += "Domestic or Wild? "+self.wildDomestic + self.spacer 
        report += self.makeASound() 
        return report

class animalsIter(object):

    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration

        self.index -= 1
        return self.data[self.index]  

    def bigGenerYes(self):
        print("in gener")
        step = 1
        for idx in range(0, len(self.data), step):
            print("yield")
            yield self.data[idx]

animals = []

anim1 = dog()
anim1.nofLegs = 4
anim1.wildDomestic = "D"
anim1.flyNoFly = "N"
anim1.type = "german Spitz"
if isinstance(anim1,dog):
    print("It's a dog alright!")
if isinstance(anim1,animal):
    print("And, it's an animal as well!")    
if issubclass(dog,animal):
    print("Dog is a sub-class")
if issubclass(animal, animal):
    print("Animal is a subclass of itself")
if not issubclass(float, int):
    print("Float is not a subclass of int")

animals.append(anim1)   

anim2 = dog()
anim2.nofLegs = 4
anim2.wildDomestic = "D"
anim2.flyNoFly = 'N'
anim2.type = "huskey"
animals.append(anim2)   

anim3 = animal()
anim3.nofLegs = 2
anim3.wildDomestic = "W"
anim3.flyNoFly = 'Y'
animals.append(anim3)   

#print(len(animals))
for beast in animals:
    print(beast.displayAttributes())

# using class built-in iterator "for each" functionality
print("##--->>> iterator class test")
Als = animalsIter(animals)
for i in Als:
    print(i.displayAttributes())

# cannot iterate over a class which is seen as a single obj. Can over any kind of array
print ("\n#### iter example with animals array - display 1st animal")
it = iter(animals)
print(next(it).displayAttributes())


## Test Generators - used with function.  Iter and next are auto-generated
print("\n#### test generator #####")
def bigGenerYes(data):
    print("in gener")
    step = 1
    for index in range(0, len(data), step):
        print("yield")
        yield data[index]

for i in bigGenerYes(animals):
    print (i.displayAttributes()) 

print("\n#### use generator in class")
Als = animalsIter(animals)
for i in Als.bigGenerYes():
    print (i.displayAttributes()) 





print ("\n##### test setattr() and getattr()")
setattr(anim3, "nofLegs", 6)
print (getattr(anim3,'nofLegs'))
print (anim3.nofLegs)

# getattr()  --> getattr(obj,x) is same thing as obj.x
# There are only two cases where getattr can be useful.
# 1) You can't write object.x, because you don't know in advance which attribute you want 
#    (it comes from a string). Very useful for meta-programming.
# 2) You want to provide a default value. object.y will raise an AttributeError if there's no y. 
#    But getattr(object, 'y', 5) will return 5.


## Emulate a C style struct 
class Cat:
    pass

cat1 = Cat()  # Create an empty cat record

# Fill the fields of the record
cat1.name = 'Mr.Cuddles'
cat1.food = 'kibbles and bits'
cat1.habbits = "Annoying wailing"

cat2 = Cat()
cat2.name = "Sir Lancelot"

print (cat1.name)
print (cat2.name)