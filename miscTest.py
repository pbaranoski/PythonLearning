
# test miscellaneous python functions

#using zip function to build key/value pairs like java map
keys = [1,2,3,4]
dogs = ["German Spitz", "Siberian Huskey", "Pomeranian"]

# zipped is an iterator
zipped = zip(keys, dogs)
print (type(zipped)) #--> <class 'zip'>
print("list: "+str(list(zipped)))
print ("len: "+str(len(list(zipped)))) ## --> 0

item_list = []
for item in zip(keys, dogs):
    item_list.append(item)
    print(type(item))
    print(item)

keys, dogs = zip(*item_list)
print("Paul")
print(dogs)

print ("########")

# using the eval function
# Lets a Python program run Python code within itself.
# eval() or exec() parses the expression passed to it and runs python expression(code).
string = " 2 ** 4"
print (eval(string))

## 1) eval() can execute only one expression whereas exec() can be used for executing a 
##    dynamically created statement or program which can include loops, if-else statements, 
##    function and class definitions,
## 2) eval() returns the value after executing a particular expression whereas exec() basically returns nothing and simply ignores the value.
prog_block = 'x = 3 \nif(x < 5): \n print(x*x)'
exec(prog_block)

print("########################")
for key in {'one':1, 'two':2}:
    print(key)

## How do I access the values in the key/value pair?
print("access value in key/value pair")
stuff = {'one':"Paul", 'two':"Tina"}
for key in stuff:
    print(stuff[key] )

print("iterate over string 123")
for char in "123":
    print(char)

# Iterators
s = "123"
it = iter(s)   
print("next(it): "+next(it))