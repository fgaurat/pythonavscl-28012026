
def mult2(i):
    return i*2



# def add(l):
def add(*l):
    # assert isinstance(l,int)
    print(l)
    r = 0
    for i in l:
        r+=i
    return r

def hello(**kwargs):
    print(kwargs)

def main():
    l = [10,20,30,40,50]
    # l2 = [i*2 for i in l]
    m2 = lambda i: i*2
    l2 = list(map(mult2,l))
    l2 = list(map(m2,l))
    l2 = list(map(lambda i: i*2,l))
    print(l2)

    r = add(*l) # 150 [10,20,30,40,50] 10,20,30,40,50
    # r = add(1,2,3)
    print(r)

    a,b,*toto,d=0,1,2,3,4,5
    print(a)
    print(d)

    a,b,*c = l


    print(*l,sep=";")


    t = [1,2,3]
    t = 1,2,3
    d = {
        "name":"Gaurat",
        "firstName":"Fred"
    }
    hello(name="Gaurat", firstName="Fred")
    hello(**d)

    print("Bonjour {name} {firstName}".format(**d))

if __name__=='__main__':
    main()
