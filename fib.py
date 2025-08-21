



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

    
