from abc import ABC, abstractmethod

class Autor(ABC):
    def __init__(self, nombre: str):
        self.__nombre = nombre
        
    @abstractmethod
    def getNombre(self) -> str:
        pass
