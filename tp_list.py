from collections import deque

def main():
    
    
    a = [10,20,30,40]
    a.append(50)
    l = a.pop()
    print(l)
    a.insert(0,0)
    print(a)

    d = deque(a)




if __name__=='__main__':
    main()
