class Producto:
    def __init__(self, nombre: str, precio: float, categorias: str, etiquetas: list[str], prioridad: int):
        self.nombre = nombre
        self.precio = precio
        self.categorias = categorias
        self.etiquetas = etiquetas
        self.prioridad = prioridad
        self.comprado = False


class ListaCompra:
    def __init__(self):
        self.productos: list[Producto] = []

    def insertar(self, nombre: str, precio: float, categoria: str, etiquetas: tuple =(), prioridad: int =3):
        nuevo_producto = Producto(nombre, precio, categoria, etiquetas, prioridad)
        self.productos.append(nuevo_producto)

    def borrar(self, indice: int):
        del self.productos[indice]

    def actualizar_precio(self, indice: int, precio_nuevo: float):
        self.productos[indice].precio = precio_nuevo

    def cambiar_estado(self, indice: int):
        self.productos[indice].comprado = True

    def mostrar_productos(self, comprados = True, etiquetas: list[str] = None, categorias: list[str] = None):
        etiquetas = etiquetas if etiquetas else [] #si no se ha introducido el parámetro de etiquetas se forma una lista vacía
        categorias = categorias if categorias else [] #si no se ha introducido el parámetro de categorias se forma una lista vacía

        for producto in self.productos:
            if not comprados and producto.comprado:
                continue
            if etiquetas:
                if not any(etiqueta in producto.etiquetas for etiqueta in etiquetas): #si ninguna etiqueta introducida esta en el producto, se pasa
                    continue
            if categorias and producto.categorias not in categorias: #se comprueba si la categoría del producto está en la lista
                continue

            msg = ""
            if producto.comprado:
                msg += "[X] " 
            else:
                "[ ] "
            msg += "- "
            msg += producto.categorias
            msg += "- "
            msg += producto.nombre
            msg += "- "
            msg += '*'*producto.prioridad
            msg += "- "
            msg += str(producto.precio)
            msg += "€ "
            msg += "- "
            msg += str(producto.etiquetas)
            print(msg)

    def ordenar(self):
        for i in range(1, len(self.productos)):
            # Guardamos el valor actual en la variable key
            producto: Producto = self.productos[i]
            j = i - 1

            # Iniciamos el bucle mientras que j sea mayor o igual a 0 y el elemento en "productos[j]" sea mayor que el producto_actual
            while j >= 0 and (self.productos[j].comprado or (not producto.comprado and producto.prioridad > self.productos[j].prioridad)):
                self.productos[j+1] = self.productos[j] # Se desplaza el producto a la derecha
                j -= 1

            # Insertamos el producto actual en el lugar correcto
            self.productos[j + 1] = producto


    