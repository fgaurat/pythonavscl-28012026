from Rectangle import Rectangle
from Carre import Carre
from Cercle import Cercle
from RectangleData import RectangleData
from ICalcGeoProtocol import ICalcGeoProtocol


def show_surface(o:ICalcGeoProtocol):
    print(o.surface)


def main():
    r = Rectangle(2,3)
    r1 = Rectangle(2,3)
    r2 = Rectangle(2,3)
    r3 = Rectangle.buildFromStr("2,3")
    print(r.longueur) # getter
    # r.longueur = -12 # setter
    print(r.longueur)

    print("get_cpt",Rectangle.get_cpt())
    print("get_cpt",r.get_cpt())


    if r1!=r2:
        print("ko")
    else:
        print("ok")

    s = str(r1)
    print(s)
    
    print(r1)

    print(r1.surface)
    
    # print(50*"-")

    # r4 = RectangleData(2,3)
    # r5 = RectangleData(2,3)

    # print(r4)
    # if r4==r5:
    #     print("ok")

    print(50*"-")
    c1 = Carre(3)
    s = str(c1)
    print("Carre(3)",c1)
    print(c1.surface)
    # print(c1.cote)
    c1.cote = 10
    print(c1.surface)
    
    c1.cote = 12
    print(50*"-")
    r5 = Rectangle(2,3)
    print(r5)
    # r5.longeur = 12
    # print(r5.__dict__)

    # c3 = Carre(3)
    # c3.longeur = "toto"
    # print(c3.__dict__)
    print(50*"-")
    ce = Cercle(3)

    print(ce.surface)
    
    show_surface(ce)
    
    show_surface(c1)

    print(50*'-')

    r6 = Rectangle(2,3)


    print(type(r6))
    print(type(Rectangle))


if __name__=='__main__':
    main()
