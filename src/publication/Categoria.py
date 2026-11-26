class Categoria:
    nombres_usados = []

    def __init__(self, nombre):
        if nombre in Categoria.nombres_usados:
            raise ValueError("Ya existe una categoria con ese nombre")
        Categoria.nombres_usados.append(nombre)
        self.nombre = nombre

    def getNombre(self):
        return self.nombre
