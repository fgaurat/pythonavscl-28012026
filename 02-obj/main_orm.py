class A:

    def show(self):
        print("A")

class B(A):

    def show(self):
        print("B")


class C(A):

    def show(self):
        print("C")


class D(B,C):

    def show(self):
        print("D") # D
        super().show() # B
        super(B,self).show() #C 
        super(C,self).show() #A 



def main():
    print(D.mro())
    d = D()
    d.show()

if __name__=='__main__':
    main()
