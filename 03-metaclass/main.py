from typing import Any
from Rectangle import Rectangle
from RectangleSingleton import RectangleSingleton
from SingletonMeta import SingletonMeta




class Test(metaclass=SingletonMeta):

    def __new__(cls):
        print("__new__")
        return super().__new__(cls)

    def __init__(self) -> None:
        print("__init__")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("__call__")


def main():
    r = Rectangle(1, 2)
    print(type(r))
    print(type(Rectangle))

    t = Test()
    t1 = Test()
    print()
    t()
    print(hex(id(t)))
    print(hex(id(t1)))

    # rs1 = RectangleSingleton(2,4)
    # rs2 = RectangleSingleton(2,4)

    # print(hex(id(rs1)))
    # print(hex(id(rs2)))
    # print(50*'-')
    r1 = Rectangle(1, 2)
    print(r1)
    r2 = Rectangle(145, 256)
    print(r2)
    
    print(hex(id(r1)))
    print(hex(id(r2)))



if __name__ == '__main__':
    main()
