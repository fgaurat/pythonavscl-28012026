

x = "the value"

def f():
    global x
    x="une autre valeur"
    print(x)


def f2():
    # print(y)

    if False:
        y=2
    

def get_increment(initial):

    def increment(inc):
        return initial+inc

    def decrement(inc):
        return initial-inc
    
    return increment,decrement


def parse_data(l):

    def filter():
        pass



def main():
    inc,dec = get_increment(10)
    c = inc(1)
    c2 = inc(10)
    print(c) # 11
    print(c2) # 11



    print("avant",x)
    f()
    print("après",x)
    f2()


if __name__=='__main__':
    main()
