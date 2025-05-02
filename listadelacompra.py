'''
Módulo de gestión la lista de la compra

Un producto es un diccionario con las siguientes claves:

* nombre, prioridad, precio, etiquetas, categoria, comprado

Por ejemplo:

producto = {
  "nombre": "Huevo",
  "precio": 12.50,
  "etiquetas": ("huevos fritos", "empanada"),
  "categoria": "Alimentación",
  "comprado": False
}

En la parte 4 de está práctica veremos cómo transformar esto en una estructura más elegante.
'''
# insertar filete; 12; carne; (pollo, rico, sano); 4

#Actividad 1


productos: list[dict] = []

def insertar(nombre: str, precio: float, categoria: str, etiquetas: str =(), prioridad: int =3):
    '''Añade un producto nuevo a la lista con los parámetros dados'''
    lista_etiquetas: list[str] = []
    # Si las etiquetas son una cadena
    if isinstance(etiquetas, str):
        # Si las etiquetas tienen paréntesis, los eliminamos
        if etiquetas.startswith("(") and etiquetas.endswith(")"):
            etiquetas.removeprefix("(")
            etiquetas.removesuffix(")")

        # Dividimos las etiquetas por comas y eliminamos espacios extra
        for etiqueta in etiquetas.split(","):
            etiqueta_limpia: str = etiqueta.strip()
            if etiqueta_limpia: #si ya no tiene espacios en blanco
                lista_etiquetas.append(etiqueta_limpia)
    
    else:
        # Si ya es una tupla, la convertimos a lista
        lista_etiquetas = list(etiquetas)

    # Convertimos la lista a tupla
    tupla_etiquetas = tuple(lista_etiquetas)


    producto: dict[str, any] = {"nombre": nombre, 
                                "precio": float(precio), 
                                "categoria": categoria, 
                                "etiquetas": tupla_etiquetas, 
                                "prioridad": int(prioridad),
                                "comprado": False}
    productos.append(producto)


def borrar(indice: int):
    '''Borra de la lista el producto que se encuentra en la posición indicada'''
    if 0 <= indice < len(productos):
        del productos[indice]
    else:
        print("índice fuera de rango")


def actualizar_precio(indice: int, precio: float):
    '''Actualiza el precio del producto con el índice dado'''
    if 0 <= indice < len(productos):
        producto_a_modificar: dict = productos[indice]
        producto_a_modificar["precio"] = precio
    else:
        print("índice fuera de rango")


def cambiar_estado(indice: int):
    '''Cambia el estado del producto con el índice dado entre comprado o no'''
    if 0 <= indice < len(productos):
        producto_a_modificar: dict = productos[indice]
        if producto_a_modificar["comprado"] == False:
            producto_a_modificar["comprado"] = True
        else:
            producto_a_modificar["comprado"] = False
        
    else:
        print("índice fuera de rango")


def mostrar_productos(comprados: bool =True, etiquetas: list[str] =[], categorias: list[str] =[]):
    '''Muestra los productos comprados con sus etiquetas y categorías'''
    for producto in productos:
        if not comprados and producto["comprado"]: #si el producto no coincide con el parámetro de búsqueda se pasa al siguiente objeto
            continue
       
        if etiquetas:
            if not any(etiqueta in producto["etiquetas"] for etiqueta in etiquetas): #se comprueba si al menos una etiqueta esta presente en el objeto
                continue
                
        if categorias and producto["categoria"] not in categorias:
            continue
        
        '''
        Se emite el mensaje una vez pasados los filtros
        '''

        msg: str = ''
        if producto['comprado']:
            msg += '[X] '
        else:
            msg += '[ ] '
        msg += "- "
        msg += producto['categoria']
        msg += "- "
        msg += producto["nombre"]
        msg += "- "
        msg += '*'*producto['prioridad']
        msg += "- "
        msg += str(producto["precio"])
        msg += "€ "
        msg += "- "
        msg += str(producto["etiquetas"])
        print(msg)





#Actividad 2

def ordenar():
    '''
    Se ordena la lista de productos, poniendo aquellos con mayor prioridad al principio.
    Los productos ya comprados se colocal al final.
    '''
    for i in range(1, len(productos)):
        # Guardamos el valor actual en la variable key
        producto_actual: dict = productos[i]
        j = i - 1

        # Iniciamos el bucle mientras que j sea mayor o igual a 0 y el elemento en "productos[j]" sea mayor que el producto_actual
        while j >= 0 and (productos[j]["comprado"] or (not producto_actual["comprado"] and producto_actual["prioridad"] > productos[j]["prioridad"])):
            productos[j+1] = productos[j] # Se desplaza el producto a la derecha
            j -= 1

        # Insertamos el producto actual en el lugar correcto
        productos[j + 1] = producto_actual



def prueba_manual():
    print('Insertando 3 productos')
    insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
    insertar('Garbanzos', 0.68, 'Alimentación', ('cocido', 'hummus'), 3)
    insertar('Hierbabuena', 1.5, 'Alimentación', ('cocktails', 'postres'), 1)

    seccion('Lista de la compra sin ordenar ni formatear')

    print(productos)

    seccion('Lista de la compra sin ordenar ni formatear (con cambio)')
    print('Cambiando un producto a comprado')
    cambiar_estado(0)
    print(productos)

    seccion('Lista de la compra sin ordenar')
    mostrar_productos()

    seccion('Lista de la compra filtradas')
    mostrar_productos(etiquetas=('cocido', ))

    seccion('Lista de la compra ordenadas')
    ordenar()
    mostrar_productos()


def seccion(texto):
    print()
    print('-' * 10, texto, '-' * 40)
    print()




#Actividad 3


def ayuda():
    '''Se muestran los comandos y sus respectivos comentarios'''
    for comando in comandos.keys():
        print(comando, comandos[comando].__doc__.strip())

comandos: dict[str, callable] = {
        "mostrar": mostrar_productos,
        "insertar": insertar,
        "borrar": borrar,
        "precio": actualizar_precio,
        "comprado": cambiar_estado,
        "ayuda": ayuda
    }

def menu():
    while True :
        comando: str = input("Introduce un comando: ")
        
        if comando == "salir":
            print("Saliendo del programa...")
            break
        
        lista: list = comando.split(" ", 1) #convertimos el comando en una lista de dos elementos separados, el comando y los argumentos.
        comando_lista: str = lista[0]
        
        if len(lista) > 0 :
            lista_argumentos: list[str] = lista[1].split(";") if len(lista) > 1 else [] #si la lista tiene argumentos, creamos una lista con argumentos y si no la dejamos vacia

        if comando_lista in comandos:
            funcion = comandos[comando_lista]
            funcion(*lista_argumentos)
    
        else:
            print("Comando no reconocido. Usa el comando 'ayuda' para ver todos los comandos disponiblles.")





if __name__ == "__main__":
    menu()