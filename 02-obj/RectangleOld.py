class Rectangle:


    def __init__(self,longueur,largeur) -> None:
        self.__longueur = longueur
        self.__largeur = largeur

    def get_longueur(self):
        return self.__longueur
    
    def set_longueur(self,l):
        self.__longueur = l

    def get_largeur(self):
        return self.__largeur
    
    def set_largeur(self,l):
        self.__largeur = l

    longueur = property(get_longueur,set_longueur,doc="la longueur")
    largeur = property(get_largeur,set_largeur,doc="la largeur")
