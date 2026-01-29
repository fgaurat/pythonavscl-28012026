from typing import Protocol

class ICalcGeoProtocol(Protocol):

    @property
    def surface(self)->float:...


