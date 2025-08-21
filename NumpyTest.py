import numpy as np

# default dtype='int32'
a = np.array([1,2,3,4,5], dtype="int16")
#print(a)
#print(" ")

b = np.array([[1.2, 3.4, 5.6, 7.8],
              [4.5, 6.5, 7.0, 8.0]])
#print (b)


''' print(f"a.ndim:{a.ndim}")
print(f"a.shape:{a.shape}")
print(f"a.dtype:{a.dtype}")
print(f"a.itemsize:{a.itemsize}")
print(f"a.nbytes:{a.nbytes}")

print(f"b.ndim:{b.ndim}")
print(f"b.shape:{b.shape}")
print(f"b.dtype:{b.dtype}")
print(f"b.itemsize:{b.itemsize}")
print(f"b.nbytes:{b.nbytes}") '''

# arrays are zero-based
#print(a[2])
#print(b[1,3])
# 2nd element from end
#print(b[1,-2])
#print ("\n")

# print entire row
print("row")
print(b[0,:])
print ("\n")

print("col")
print(b[:, 0])
print ("\n")

# change a value in array
b[0,0] = 88.8

# change all values in a column
b[:,2] = 69
# change column values with a list of values
b[:,2] = [69, 96]

#print(b[0,0:4:3])

#print(b[0,0:-1:2])

print("all Elements")
for x in b:
    print("new row")
    for y in x:
        print(y)

print("\nPrint Entire Array")
print(b)