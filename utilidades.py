
'''
Actividad 1
'''
def euros_a_bitcoins(euros: int | float) -> int | float:
  '''Convierte una cantidad de euros a bitcoins. 1 bitcoin = 44570.17 €'''
  bitcoin: int = euros /44471.78
  bitcoins_redondeado: int = round(bitcoin, 2)
  return bitcoins_redondeado
def bitcoins_a_euros(bitcoins: int | float) -> int | float:
  '''Convierte una cantidad de bitcoins a euros. 1 bitcoin = 44570.17 €'''
  euro: int = bitcoins * 44471.78
  euros_redondeado: int = round(euro, 2)
  return euros_redondeado


'''
Actividad 2
'''
def contar_vocales(texto: str) -> int :
  '''Devuelve el número de vocales que tiene el texto dado.'''
  x: str = texto.lower() #Convierte el texto a minúsculas
  vocales: str = "aeiou" #Lista de vocales
  contador: int = 0

  for vocal in x : #Se recorren todas las letras del texto
        if vocal in vocales :
            contador += 1 #Se suma una unidad al contador si se encuentra una vocal
  return contador
  

'''
Actividad 3
'''
def es_palindromo(texto: str) -> bool :
  '''Detecta si un texto es palíndromo o no'''
  texto_sin_espacios = texto.lower().replace(" ", "") #Quitamos espacios y mayúsculas
  if texto_sin_espacios == texto_sin_espacios[::-1]: #Comparación entre los dos textos
     return True
  else :
     return False


'''
Actividad 4
'''
def max_temperaturas(temperaturas: list[float], umbral: float) -> list[float]:
  '''Detecta qué mediciones de temperatura han superado el umbral dado'''
  nueva_lista: list[float] = [] #Se crea una nueva lista vacía donde añadir las temperaturas que superen el umbral
  for temperatura in temperaturas : #Se recorre cada elemento de la lista para comprobar si es mayor que el umbral
     if temperatura > umbral :
        nueva_lista.append(temperatura) #Se añaden dichas temperaturas
  return nueva_lista


'''
Actividad 5
'''
productos: list[str] = []

def insertar(producto: str) -> None :
  '''Añade un producto a la lista'''
  productos.append(producto)

def borrar(numero: int) -> None :
  '''Borra el producto en el índice dado de lista de productos.'''
  del productos[numero]

def mostrar_productos() -> str:
  '''Muestra la lista de productos con sus índices.'''
  if len(productos) == 0 :
    print("No hay productos.")
  else :
     for indice, producto in enumerate(productos) :
        '''print(f"{indice}: {producto}")'''
        print(str(indice) + ": " + producto)

def cantidad() -> int:
  '''Devuelve el número de productos.'''
  return len(productos)


'''
Actividad 7
'''
def menu_interactivo():
   print("Menú interactivo" + 
         "\nComandos para utilizar:" + 
         "\nconvertir euros bitcoins <cantidad>" + 
         "\nconvertir bitcoins euros <cantidad>" + 
         "\ncontar <texto>" +
         "\npalindromo <texto>" +
         "\ntemperaturas <varios números separados por comas> <umbral>" +
         "\nproductos" +
         "\nproductos nuevo <nombre>"
         "\nproductos borrar <índice>"
         "\nsalir")
   while True :
    comando: str = input("Introduce un comando: ")
    lista: list = comando.split()
    longitud = len(lista)


    if lista[0] == "convertir":
      if lista[1] == "euros":
        euros: float = float(lista[3])
        print(euros_a_bitcoins(euros))

      elif lista[1] == "bitcoins":
        bitcoins: float = float(lista[3])
        print(bitcoins_a_euros(bitcoins))
    
    elif lista [0] == "contar":
      lista_recortada: list[str] = lista[1:]
      texto: str = " ".join(lista_recortada)
      print(contar_vocales(texto)) 

    elif lista[0] == "palindromo":
       lista_recortada: list[str] = lista[1:]
       texto: str = " ".join(lista_recortada) 
       print(es_palindromo(texto))

    elif lista[0] == "temperaturas":
       lista_recortada: list[float] = lista[1:]
       longitud: int = len(lista_recortada)
       umbral: float = lista_recortada[longitud - 1]
       lista_recortada.remove(umbral)
       lista_sin_comas: list[float] = []
       for temperatura in lista_recortada:
          temperatura_sin_comas: float = temperatura.replace(",","")
          lista_sin_comas.append(temperatura_sin_comas)
       print(max_temperaturas(lista_sin_comas, umbral))

    elif lista[0] == "productos":
      longitud: int = len(lista)
      
      if longitud == 1:
        mostrar_productos()

      elif lista[1] == "nuevo":
        insertar(lista[2])
        mostrar_productos()

      elif lista[1] == "borrar":
        print(borrar(int(lista[2])))
        mostrar_productos()
    
    elif lista[0] == "salir":
      print("¡Adiós!")
      break
       
       

if __name__ == "__main__":
   menu_interactivo()
