import func
import sys
import copy


empty_list = []

# DANGER : la liste est partagée entre tous les appels
def ajouter_element_danger(element, liste=empty_list):
    liste.append(element)
    return liste

def ajouter_element_safe(element, liste=None):
    if liste is None:
        liste = []
    liste.append(element)
    return liste


print("\n--- Version dangereuse ---")
print(f"Appel 1 : {ajouter_element_danger(1)}")  # [1]
print(f"Appel 2 : {ajouter_element_danger(2)}")  # [1, 2] - Surprise !
print(f"Appel 3 : {ajouter_element_danger(3)}")  # [1, 2, 3] - Continue !



def main():
    a = 1
    b = 1


    a=123

    print(hex(id(a)))
    print(hex(id(b)))

    c = 134345642434532
    d= 134345642434532
    e= 134345642434532
    print("getrefcount",sys.getrefcount(134345642434532))
    print("getrefcount 1",sys.getrefcount(1))
    f = 1
    print("getrefcount 1",sys.getrefcount(1))



    l = [10,20,30,40]
    print("l",l)
    l.append(50)
    print("l",l)
    # l1 = l.copy()
    # l1 = l.copy()
    # l1 = copy.copy(l)
    l1 = l[:]

    print("l1",l1)
    l.append(60)
    print("l1",l1)

    l2 = [
        [10,20,30],
        [40,50,60],
        [70,80,90],
    ]

    print("l2",l2)

    # l3 = l2.copy()
    l3 = copy.deepcopy(l2)
    print("l2",l2)
    l2[1][1] = 500

    print("l2",l2)
    print("l3",l3)

if __name__=='__main__':
    # main()

    # print(c)
    pass
