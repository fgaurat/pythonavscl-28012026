from singletonDeco import singleton
from SingletonMeta import SingletonMeta


# @singleton
class Rectangle(metaclass=SingletonMeta):

    __slots__ = "__longueur","__largeur"
    __cpt = 0

    def __init__(self,longueur,largeur) -> None:
        self.__longueur = longueur
        self.__largeur = largeur
        Rectangle.__cpt+=1
    
    @classmethod
    def buildFromStr(cls,value):
        lng,lrg = [int(v) for v in value.split(",")]
        r = cls(lng,lrg)
        return r

    @staticmethod    
    def get_cpt():
        return Rectangle.__cpt
    

    @property
    def longueur(self):
        return self.__longueur
    
    @longueur.setter
    def longueur(self,l):
        if l<0:
            raise Exception('Hooooo !')
        self.__longueur = l
    
    @property
    def largeur(self):
        return self.__largeur
    
    @largeur.setter
    def largeur(self,l):
        self.__largeur = l

    def __eq__(self,o):
        return self.longueur == o.longueur and self.largeur == o.largeur


    def __str__(self):
        return f"{__class__.__name__}   {self.longueur=},{self.largeur=} {type(self)}"
    
    @property
    def surface(self):
        return self.longueur * self.largeur