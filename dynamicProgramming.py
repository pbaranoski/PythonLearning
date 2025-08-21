

###############################################
# dynamic programming - fibonacci number calc
###############################################
def fib(n, dictFib={}):
    if (n in dictFib):
        return dictFib[n]
    if n <= 2:
        return 1

    dictFib[n] =  fib(n - 1) + fib(n - 2) 
    return dictFib[n]

 

print(fib(6))
print(fib(7))
print(fib(50))

#########################################
# non-dynamic programming
##########################################
def fibfwd(x):

    for i in range(x):
        if i == 0:
            n_1 = 0
            n_2 = 0
        elif i == 1:
            n_1 = 1
            n_2 = 0
        else:
            n_2 = n_1
            n_1 = n

        n = n_1 + n_2


    return n

print(fibfwd(6))
print(fibfwd(7))
print(fibfwd(50))
