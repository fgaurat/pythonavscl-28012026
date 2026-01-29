from ICalcGeo import ICalcGeo
import math

# class Cercle(ICalcGeo):
class Cercle:

    def __init__(self, rayon) -> None:
        self.__rayon = rayon

    @property
    def rayon(self):
        return self.__rayon
    
    @rayon.setter
    def rayon(self,c):
        self.__rayon = c

    @property
    def surface(self):
        return math.pi * math.pow(self.__rayon,2)

    def __str__(self):
        return f"{__class__.__name__}   {self.rayon=}"
