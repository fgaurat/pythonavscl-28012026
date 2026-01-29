import time
from functools import wraps


def my_timeit(func):
    
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        r = func(*args,**kwargs)
        end = time.perf_counter()
        print(func.__name__,"t:",end-start)
        return r
    return wrapper

def log(func):
    print("deco",func)
    @wraps(func)
    def wrapper(*args,**kwargs):
        print("Log avant",args,kwargs)
        r = func(*args,**kwargs)
        print("Log aprés",r)
        return r
        
    return wrapper

def gras(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        return f"<b>{func(*args,**kwargs)}</b>"
    
    return wrapper

@log
@gras
def hello(name):
    return f"Bonjour {name}"


@my_timeit
def long_work():
    """ la doc de long_work"""
    time.sleep(0.5)
    print("end")



def main():
    r = hello("fred")
    print(r)
    # long_work()
    # print("Doc de long_work",long_work.__doc__)
    # print(long_work.__name__)

if __name__=='__main__':
    main()


