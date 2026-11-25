class Etiqueta:
    nombres_usados = []

    def __init__(self, nombre):
        if nombre in Etiqueta.nombres_usados:
            raise ValueError("Ya existe una etiqueta con ese nombre")
        Etiqueta.nombres_usados.append(nombre)
        self.nombre = nombre

    def getNombre(self):
        return self.nombre
