import shlex

class Habilidad:
    '''Abstracción del concepto de habilidad en un asistente.'''

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion or self.__doc__ #si no se da descripcion, usa la documentación
       
    def invocar(self):
        """Invocar la habilidad. No acepta parámetros"""
        print(f'Se ha invocado la habilidad {self.nombre}')

    def ayuda(self):
        """Devolver la descripción de la habilidad"""
        texto = self.descripcion or self.invocar.__doc__
        print(texto)

class Divisas(Habilidad):
    '''Conversión de divisas'''
    def __init__(self, *args, tasa=0.85, **kwargs):
         # La clase padre (Habilidad, en este caso) se encargará de inicializar los atributos por nosotros
        super().__init__(*args, **kwargs)
        # Una vez han sido inicializados los atributos, añadimos los específicos de esta clase (Divislisa)
        self.tasa = tasa

    def invocar(self, cantidad):
        '''Convertir una cantidad la divisa original a la divisa objetivo'''
        cantidad = float(cantidad)
        resultado = round(cantidad * self.tasa, 2)
        print(resultado)

class Menu:
    '''Menú interactivo de gestión de habilidades.'''

    def __init__(self, habilidades: list[Habilidad]):
        # habilidades es una LISTA
        # self.habilidades es un diccionario de nombre -> habilidad
        self.habilidades: dict[str, Habilidad] = {}
        for habilidad in habilidades:
            self.habilidades[habilidad.nombre] = habilidad

    def ayuda(self, habilidad=None):
        '''
        Muestra ayuda del uso del menú. Si no se especifica una habilidad,
        se muestra la ayuda general. Esta ayuda general muestra la lista
        de habilidades, una por línea, y la descripción de cada habilidad.

        Si se especifica una habilidad, se muestra su ayuda específica.
        '''
        if not habilidad:
            print('Habilidades disponibles:')
            for hab in self.habilidades.values():
                print(f'\t{hab.nombre}:\t{hab.descripcion}')
            return
    
        if habilidad not in self.habilidades:
            print(f'Habilidad no encontrada: {habilidad}')
            return
        
        self.habilidades[habilidad].ayuda() #se devuelve la documentación

    def lanzar(self):
        '''Recibe instrucciones del usuario en bucle.'''
        while True:
            linea = input('> ')
            if self.ejecutar(linea):
                break

    def convertir_linea(self, linea):
        '''Convierte una línea del usuario en comando + argumentos'''
        tokens: list[str] = shlex.split(linea)
        comando: str = tokens[0]
        args: list[str] = tokens[1:]
        string_args: str = " ".join(args)
        return comando, string_args

    def ejecutar(self, linea):
        '''
        Recibe una línea del usuario y ejecuta la acción requerida

        Devuelve True cuando se desea parar la ejecución.
        '''
        comando, string_args = self.convertir_linea(linea)
    
        if comando == "salir":
            return True
        elif comando == "ayuda":
            if string_args:
                self.ayuda(string_args)
            else:
                self.ayuda()
        elif comando in self.habilidades:
            habilidad = self.habilidades[comando]
            if isinstance(habilidad, HabilidadSubcomandos):
                # Separar el subcomando y sus argumentos
                args_list = string_args.split()
                if args_list:
                    subcomando = args_list[0]
                    sub_args = args_list[1:]
                    habilidad.invocar(subcomando, *sub_args)
                else:
                    print("Faltan argumentos para el subcomando.")
            else:
                # Si no es un subcomando, pasar todos los argumentos
                habilidad.invocar(*string_args.split())
                
        else:
            print(f"Habilidad no encontrada: {self.habilidades[comando].nombre}")

    def emular(self, linea):
        print('>', linea)
        self.ejecutar(linea)


# # Apartado de Menús alternativos - 9

class MenuComas(Menu):
    def convertir_linea(self, linea):
        tokens: list[str] = linea.split(",")
        comando: str = tokens[0]
        args: str = tokens[1:]
        string_args: str = " ".join(args)
        return comando, string_args

class MenuPrompt(Menu):
    def __init__(self, habilidades, prompt="> "):
        super().__init__(habilidades)
        self.prompt = prompt

    def lanzar(self):
        '''Sobrescribe lanzar para usar un prompt personalizado.'''
        while True:
            linea = input(self.prompt)
            if self.ejecutar(linea):
                break

class MenuPreguntas(Menu):
    def convertir_linea(self):
        comando: str = input("Introduce el comando: ").strip()
        if comando == "salir":
            return comando, ""  # No necesita argumentos.

        if comando not in self.habilidades and comando != "ayuda":
            print(f"Comando no válido: {comando}")
            return None, None  # Señal de comando inválido.

        argumentos = []
        while True:
            argumento: str = input("Introduce un argumento (deja vacío para terminar): ").strip()
            if not argumento:
                break
            argumentos.append(argumento)

        string_args = " ".join(argumentos)
        return comando, string_args
            
    
    def ejecutar(self):
        '''
        Recibe una línea del usuario y ejecuta la acción requerida

        Devuelve True cuando se desea parar la ejecución.
        '''
        comando, string_args = self.convertir_linea() #recibe dos strings
        
        if comando == "salir":
            print("Saliendo del menú...")
            return True
    
        elif comando == "ayuda":
            if string_args:
                self.ayuda(string_args)
                self.lanzar() #volvemos a llamar a la función
            else:
                self.ayuda()
                self.lanzar() #volvemos a llamar a la función

        elif comando in self.habilidades:
            habilidad = self.habilidades[comando]
            if isinstance(habilidad, HabilidadSubcomandos):
                # Separar el subcomando y sus argumentos
                args_list = string_args.split()
                subcomando = args_list[0]
                sub_args = args_list[1:]
                print(subcomando, sub_args)
                habilidad.invocar(subcomando, *sub_args)
                self.lanzar() #volvemos a llamar a la función
                
            else:
                # Si no es un subcomando, pasar todos los argumentos
                habilidad.invocar(*string_args.split())
                self.lanzar() #volvemos a llamar a la función
        else:
            print(f"Habilidad no encontrada: {comando}")

    def lanzar(self):
        """
        Ciclo principal del menú. Solicita al usuario comandos y ejecuta
        habilidades hasta que se introduce el comando 'salir'.
        """
        print("Introduce 'salir' para salir del menú.")
        self.ejecutar()

    
    def ayuda(self, habilidad=None):
        if not habilidad:
            print('Habilidades disponibles:')
            for hab in self.habilidades.values():
                print(f'\t{hab.nombre}:\t{hab.descripcion}')
            return

        if habilidad not in self.habilidades:
            print(f'Habilidad no encontrada: {habilidad}')
            return

        self.habilidades[habilidad].ayuda()  # Muestra la documentación específica.
    

class ListaDeLaCompra(Habilidad):
    """Gestión muy simple de lista de la compra"""
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.productos = []

    def invocar(self, *args):
        comando: str = args[0]
        args: tuple = args[1:] 
        args: list = list(args)
        i= 0

        for i in range (0, len(args)-1):
            if args[i].startswith('(') and args[i+1].endswith(')'):
                etiquetas: str = args[i] + ' ' + args[i+1]
                del args[i+1]
                args[i]= etiquetas
    
        if comando == "insertar":
            self.insertar(*args)
        if comando == "borrar":
            self.borrar(*args)
        if comando == "mostrar":
            if len(args) >0:
                print(args)
                self.mostrar(*args)
            else:
                self.mostrar()
        if comando == "cantidad":
            self.cantidad()
    
    def insertar(self, nombre: str, precio: float = 0, categoria: str = "Sin categoría", etiquetas: str =(), prioridad: int =3):
        print(nombre)
        lista_etiquetas: list[str] = []
        # Si las etiquetas son una cadena
        if isinstance(etiquetas, str):
            etiquetas = etiquetas.strip("()").split(",")

            # Dividimos las etiquetas por comas y eliminamos espacios extra
            for etiqueta in etiquetas:
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
        self.productos.append(producto)
    
    def borrar(self, indice: int):
        indice= int(indice)
        if -1 < indice < len(self.productos) - 1:
            del self.productos[indice]
        else:
            print("índice fuera de rango")
    
    def mostrar(self, comprados: bool =True, etiquetas: list[str] =[], categorias: list[str] =[]):
        """Muestra los productos comprados con sus etiquetas y categorías"""
        for producto in self.productos:
            if not comprados and producto["comprado"]: #si comprados ha sido marcado como False, todos los productos que hayan sido comprados no aparecen en el mensaje
                continue
        
            if etiquetas:
                if not any(etiqueta in producto["etiquetas"] for etiqueta in etiquetas): #se comprueba si al menos una etiqueta esta presente en el objeto
                    continue
              
            if categorias and producto["categoria"] not in categorias:
                continue
            
            
            """Se emite el mensaje una vez pasados los filtros"""
            

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
    
    def cantidad(self) -> int:
        cantidad: int = len(self.productos) 
        print(cantidad)
        return cantidad
    
    def ordenar(self):
        '''
        Se ordena la lista de productos, poniendo aquellos con mayor prioridad al principio.
        Los productos ya comprados se coloca al final.
        '''
        for i in range(1, len(self.productos)):
            # Guardamos el valor actual en la variable key
            producto_actual: dict = self.productos[i]
            j = i - 1

            # Iniciamos el bucle mientras que j sea mayor o igual a 0 y el elemento en "productos[j]" sea mayor que el producto_actual
            while j >= 0 and (self.productos[j]["comprado"] or (not producto_actual["comprado"] and producto_actual["prioridad"] > self.productos[j]["prioridad"])):
                self.productos[j+1] = self.productos[j] # Se desplaza el producto a la derecha
                j -= 1

            # Insertamos el producto actual en el lugar correcto
            self.productos[j + 1] = producto_actual

    def ayuda(self):
        print("Acepta las acciones: insertar, borrar, listar y cantidad")


# # Apartado de Subcomandos - 7
class HabilidadSubcomandos(Habilidad):
    '''Un tipo de habilidad que permite invocar varios sub-comandos'''

    def subcomandos(self):
        '''
        Devuelve un diccionario de subcomandos a funciones.
        
        p.e.:
            {
            'insertar': self.insertar_producto,
            'borrar': self.borrar_producto,
            }
        '''
        return {}

    def invocar(self, subcomando: str, *args):
        subcomandos = self.subcomandos()
        if subcomando in subcomandos:
            metodo = subcomandos[subcomando]
            metodo(*args)
        else: 
            print(f"El subcomando '{subcomando}' introducido no se encuentra disponible.")

    def ayuda(self):
        print('Comando:\t', self.nombre)
        print('Descripción:\t', self.descripcion)
        print('Subcomandos:')
        # Muestra información de cada uno de los subcomandos
        for subcomando, funcion in self.subcomandos().items():
            print(f"  {subcomando}: {funcion.__doc__}")


# # Apartado de Refactorización - 8
class Contador(Habilidad):
    '''Devuelve el número de vocales que tiene el texto dado.'''   
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      
    def invocar(self, texto):
        texto: str = texto.lower() #Convierte el texto a minúsculas
        vocales: str = "aeiou" #Lista de vocales
        contador: int = 0

        for vocal in texto : #Se recorren todas las letras del texto
                if vocal in vocales :
                    contador += 1 #Se suma una unidad al contador si se encuentra una vocal
        print(contador)            
        return contador


class DetectorPalindromos(Habilidad):
    '''Detecta si un texto es palíndromo o no'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = args

    def invocar(self, *texto) -> bool:
        texto = " ".join(texto)    
        texto_sin_espacios = texto.lower().replace(" ", "") #Quitamos espacios y mayúsculas
        if texto_sin_espacios == texto_sin_espacios[::-1]: #Comparación entre los dos textos
            print(f" {texto} es palíndromo.")
            return True
        else :
            print(f" {texto} no es palíndromo.")
            return False
        

class ListaCompraP2(HabilidadSubcomandos):
    '''Gestión muy simple de lista de la compra'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productos = []

    def subcomandos(self):
        return {
      'insertar': self.insertar,
      'borrar': self.borrar,
      'cantidad': self.cantidad,
      'mostrar': self.mostrar,
      'ordenar': self.ordenar
      }

    def insertar(self, nombre: str, precio: float = 0, categoria: str = "Sin categoría", etiquetas: str =(), prioridad: int =3):
        print(nombre)
        lista_etiquetas: list[str] = []
        # Si las etiquetas son una cadena
        if isinstance(etiquetas, str):
            etiquetas = etiquetas.strip("()").split(",")

            # Dividimos las etiquetas por comas y eliminamos espacios extra
            for etiqueta in etiquetas:
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
        self.productos.append(producto)
    
    def borrar(self, indice: int):
        indice= int(indice)
        if -1 < indice < len(self.productos) - 1:
            del self.productos[indice]
        else:
            print("índice fuera de rango")
    
    def mostrar(self, comprados: bool =True, etiquetas: list[str] =[], categorias: list[str] =[]):
        """Muestra los productos comprados con sus etiquetas y categorías"""
        for producto in self.productos:
            if not comprados and producto["comprado"]: #si comprados ha sido marcado como False, todos los productos que hayan sido comprados no aparecen en el mensaje
                continue
        
            if etiquetas:
                if not any(etiqueta in producto["etiquetas"] for etiqueta in etiquetas): #se comprueba si al menos una etiqueta esta presente en el objeto
                    continue
              
            if categorias and producto["categoria"] not in categorias:
                continue
            
            
            """Se emite el mensaje una vez pasados los filtros"""
            

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
    
    def cantidad(self) -> int:
        cantidad: int = len(self.productos) 
        print(cantidad)
        return cantidad
    
    def ordenar(self):
        '''
        Se ordena la lista de productos, poniendo aquellos con mayor prioridad al principio.
        Los productos ya comprados se coloca al final.
        '''
        for i in range(1, len(self.productos)):
            # Guardamos el valor actual en la variable key
            producto_actual: dict = self.productos[i]
            j = i - 1

            # Iniciamos el bucle mientras que j sea mayor o igual a 0 y el elemento en "productos[j]" sea mayor que el producto_actual
            while j >= 0 and (self.productos[j]["comprado"] or (not producto_actual["comprado"] and len(producto_actual["nombre"]) > len(self.productos[j]["nombre"]))):
                self.productos[j+1] = self.productos[j] # Se desplaza el producto a la derecha
                j -= 1

            # Insertamos el producto actual en el lugar correcto
            self.productos[j + 1] = producto_actual

    def ayuda(self):
        print("Acepta las acciones: insertar, borrar, listar y cantidad")


# Menu con todas las habilidades
habilidades: list[Habilidad] = [
    Divisas("bitcoin2euro", descripcion="Conversión de bitcoins a euros", tasa=49929.38),
    Divisas("euro2bitcoin", descripcion="Conversión de euros a bitcoins", tasa=1/49929.38),
    ListaCompraP2("listadelacompra"),
    Contador("contador", descripcion="Contar las vocales en un texto."),
    DetectorPalindromos("palindromo", descripcion="Detectar si un texto es un palíndromo.")
]
m = Menu(habilidades)

# Pruebas
def prueba_menu_subcomandos():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38),
        Divisas('euro2bitcoin', tasa=1/49929.38),
        ListaCompraP2('listadelacompra', 'Gestión de la lista de la compra')
        ]
    m = Menu(habilidades)
    m.emular('ayuda')
    m.emular('ayuda listadelacompra')
    m.emular('listadelacompra insertar plátanos 5.25 Alimentación frutas,postre')
    m.emular('listadelacompra insertar Pimientos 1.50 Alimentación')
    m.emular('listadelacompra listar')
    m.emular('listadelacompra borrar 0')
    m.emular('listadelacompra listar')

def prueba_menu_simple():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38, descripcion='Conversión de bitcoins a euros'),
        Divisas('euro2bitcoin', tasa=1/49929.38, descripcion='Conversión de euros a bitcoins'),
    ]
    m = Menu(habilidades)
    m.emular('ayuda')
    m.emular('bitcoin2euro 1')
    m.emular('euro2bitcoin 1000')
    m.emular('ayuda noexiste')
    m.emular('ayuda bitcoin2euro')

def prueba_menu_simple_lista_de_la_compra():
    habilidades = [ListaDeLaCompra('listadelacompra', descripcion= 'Gestión de la lista de la compra')]
    menu = Menu(habilidades)

    print("\nPrueba: Insertar productos")
    menu.emular('listadelacompra insertar "Manzanas" 2.5 "Frutas" "(fresca, dulce)" 2')
    menu.emular('listadelacompra insertar "Pan" 1.2 "Panadería" "(integral)" 3')
    menu.emular('listadelacompra insertar "Leche" 1.0 "Lácteos" "(desnatada)" 1')
    
    print("\nPrueba: Mostrar productos")
    menu.emular('listadelacompra mostrar')
    
    print("\nPrueba: Borrar un producto")
    menu.emular('listadelacompra borrar 1')
    menu.emular('listadelacompra mostrar')
    
    print("\nPrueba: Mostrar cantidad de productos")
    menu.emular('listadelacompra cantidad')
    
    print("\nPrueba: Ordenar productos por prioridad")
    menu.emular('listadelacompra ordenar')
    menu.emular('listadelacompra mostrar')
    
    print("\nPrueba: Mostrar ayuda")
    menu.emular('ayuda listadelacompra')
    
    print("\nPrueba: Salir del menú")
    menu.emular('salir')

def prueba_menu_comas():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38),
        Divisas('euro2bitcoin', tasa=1/49929.38),
        ListaCompraP2('listadelacompra', 'Gestión de la lista de la compra')
        ]
    m = MenuComas(habilidades)
    m.emular('ayuda')
    m.emular('ayuda, listadelacompra')
    m.emular('listadelacompra, insertar, plátanos, 5.25, , "frutas,postre"')
    m.emular('listadelacompra, insertar, Pimientos, 1.50, Alimentación')
    m.emular('listadelacompra, listar')
    m.emular('listadelacompra, borrar, 0')
    m.emular('listadelacompra, listar')

def prueba_menu_prompt():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38),
        Divisas('euro2bitcoin', tasa=1/49929.38),
        ListaCompraP2('listadelacompra', 'Gestión de la lista de la compra')
        ]
    prompt: str = "# "
    m = MenuPrompt(habilidades, prompt)
    m.lanzar()

def prueba_menu_preguntas():
    habilidades = [
        Divisas('bitcoin2euro', tasa=49929.38),
        Divisas('euro2bitcoin', tasa=1/49929.38),
        ListaCompraP2('listadelacompra', 'Gestión de la lista de la compra')
        ]
    m = MenuPreguntas(habilidades)
    m.lanzar()

def prueba_contador_palindromo():
    habilidades: list[Habilidad] = [
    Divisas("bitcoin2euro", descripcion="Conversión de bitcoins a euros", tasa=49929.38),
    Divisas("euro2bitcoin", descripcion="Conversión de euros a bitcoins", tasa=1/49929.38),
    ListaCompraP2("listadelacompra"),
    Contador("contador", descripcion="Contar las vocales en un texto."),
    DetectorPalindromos("palindromo", descripcion="Detectar si un texto es un palíndromo.")
    ]
    m = Menu(habilidades)
    m.emular('ayuda')
    print("PRUEBA CONTADOR")
    m.emular('contador hola')
    print("PRUEBA PALINDROMOS")
    m.emular('palindromo hello')
    m.emular('palindromo alola')


if __name__ == '__main__':
    print("### PRUEBAS ###")
    ### print('#' * 10, 'Prueba menú simple')
    ## prueba_menu_simple()
    ## prueba_menu_simple_lista_de_la_compra()
    ## Descomentar para probar el apartado de subcomandos
    ## print('#' * 10, 'Prueba menú con subcomandos')
    ## prueba_menu_subcomandos()
    ## prueba_menu_comas()
    ## prueba_menu_prompt()
    ## prueba_menu_preguntas()
    ## prueba_contador_palindromo()
    m.lanzar()
