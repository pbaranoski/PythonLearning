# PythonTest2

import os
import re

temp_dir = "C:\\Users\\user\\Documents\\PythonLearning\\temp"

#######################################
# Create directory and set permissions
#######################################
if not os.path.exists(temp_dir):
    # setting permissions the unix way
    os.mkdir(temp_dir, 755)
    print ("temp_dir created")

#######################################
# While Loop logic
#######################################
print ("while loop")

i = 0
while (i < 10):     
    i = i + 1
    i += 1

    if i == 6:
        # break exits entire while; does not perform WHILE-ELSE
        break
        # continue restarts the loop; will allow the performing of WHILE-ELSE
        ##continue

    print("count: " +str(i)) 
else:
    print("while is done --> this doesn't run if there is a `break` command")

print ("")

#######################################
# For In Loop logic
#######################################
print ("for in loop")

string = "mickey mouse wears army boots!"

for letter in string:
    
    if letter == "m":
        print("we like the letter m")

    if letter == "o":
        print ("we don't like 'o'")
        continue

    # print a character from the string
    print (letter)

#######################################
# For range Loop logic
#######################################
print ("\n ###--- For Range Test -- ####")
#for i in range(10):
#for i in range(0,10):
for i in range(len(string)):

    if string[i] == "m":
        print("we like the letter m")

    if string[i] == "o":
        print ("we don't like 'o'")
        continue

    # print a character from the string
    print (string[i])

#######################################
# For range Loop logic alternate version
#######################################
print()
print ("last example")

l = [10, 20, 30, 40]
# len of l is 4;
for i in range(len(l)):
    # end == character to append at end
    print(l[i], end="|")




    