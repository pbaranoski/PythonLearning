import threading
 
def print_cube(num):
    """
    function to print cube of given num
    """
    print("Cube: {}".format(num**3))
 
def print_square(num):
    """
    function to print square of given num
    """
    print("Square: {}".format(num**2))
 
if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
 
    # both threads completely executed
    print("Done!")