from multiprocessing import Process
import time
import os
import sys
import datetime
import requests

# process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) 
#psutil (FYI)

def getDateTime():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S.%f')

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def print_func( sleepSecs, continent='Asia'):
    print("start function at "+getDateTime())
    info(f"print_func parm:{continent}")
    time.sleep(sleepSecs)
    print('The name of continent is : ', continent)


if __name__ == "__main__":  # confirms that the code is under main function
    info("print_func main")
    names = ['America', 'Europe', 'Africa']
    procs = []
#    proc = Process(target=print_func)  # instantiating without any argument
#    procs.append(proc)
#    proc.start()

    # instantiating processes with arguments
    i = 6
    for name in names:
        # print(name)
        i -= 2
        proc = Process(target=print_func, args=(i,name,))
        procs.append(proc)
        proc.start()
        #time.sleep(1)

    # complete the processes
    # Join is like a wait --> to wait for child processes to complete
    for proc in procs:
        proc.join()

    sys.exit(0)

    print("\n\n****************")

    # test
def cube(x):
    print('%s cube is %s' % (x, x**3))

if __name__ == "__main__": 
    pees = []
    my_numbers = [3, 4, 5, 6, 7, 8]
    for x in my_numbers:
        p = Process(target=cube, args=(x,))
        pees.append(p)
        p.start()

    for p in pees:
        p.join
        #print("join")
    
    print ("Done")

    ## Assert test when fails throws a AssertionError
    ##
    #i = 8
    #assert i == 9
    #
    #with requests.Session() as session:
    #    page = session.get("https://realpython.com/python-async-features/")

    #page = requests.session().get("https://realpython.com/python-async-features/")
    #print("hi there")