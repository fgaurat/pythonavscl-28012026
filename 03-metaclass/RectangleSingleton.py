class RectangleSingleton:

    __slots__ = "__longueur","__largeur"
    __cpt = 0

    instance = None       # Attribut statique de classe
    def __new__(cls,*args,**kwargs): 
        "méthode de construction standard en Python"
        
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance


    def __init__(self,longueur=1,largeur=1) -> None:
        self.__longueur = longueur
        self.__largeur = largeur
        RectangleSingleton.__cpt+=1
    
    @classmethod
    def buildFromStr(cls,value):
        lng,lrg = [int(v) for v in value.split(",")]
        r = cls(lng,lrg)
        return r

    @staticmethod    
    def get_cpt():
        return RectangleSingleton.__cpt
    

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