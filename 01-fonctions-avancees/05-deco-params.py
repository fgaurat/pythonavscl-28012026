from functools import wraps

def log(destination_log):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print(f"Log -> {destination_log} avant",args,kwargs)
            r = func(*args,**kwargs)
            print(f"Log -> {destination_log} aprés",r)
            return r
            
        return wrapper
    return decorator

@log("thelog.log")
def hello(name):
    return f"Bonjour {name}"



def main():
    r = hello("fred")
    print(r)

if __name__=='__main__':
    main()
