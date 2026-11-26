from abc import ABC


class Autor(ABC):
    def __init__(self, nombre: str):
        self.__nombre = nombre

    def getNombre(self) -> str:
        return self.__nombre