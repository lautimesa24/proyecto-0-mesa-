import sys
#agrego de manejo de argumentos con sys

def separar_viento(campo_viento: str) -> tuple:
    partes = campo_viento.split()
    
    if partes[0] == "Calma":
        return ("Calma", 0)
    direccion = " ".join(partes[:-1]) # se toma todos los elementos excepto el último como dirección. 
    velocidad = float(partes[-1])
    return (direccion, velocidad)

# prueba para ver si anda
#print(separar_viento("Sur  5"))
#print(separar_viento("Calma"))
#print(separar_viento("Noroeste  12")) 


def convertir_sen_termica(valor: str):
    if valor == "" or valor == "No se calcula": # 
        return None # lo deje como none por que es  none por que es un dato que no esta y no hay forma de calcularlo como para dejarlo en 0. 
    return float(valor)

def leer_observaciones(ruta:str)->dict:
    observaciones= {}
    lineas_invalidas = 0
    try:      
        with open(ruta, "r", encoding="latin-1") as archivo:
            for linea in archivo:
                linea = linea.strip()
                campos = linea.split(";")
        
                if len(campos) != 10:
                    lineas_invalidas += 1
                    continue
            
                ciudad = campos[0].strip()
                
                if ciudad == "":
                    # si no hay un nombre de ciudad no se puede usar como clave asi que se cuenta como linea invalida, esto evita que se rompa el programaa
                    lineas_invalidas += 1
                    continue
                
                if campos[8].strip() == "":
                    direccion, velocidad = None, None
                else:
                     direccion, velocidad = separar_viento(campos[8]) # 8 son los campos en horizontal
                
                temperatura = None # se sobrescribe por lo que pase en el if/else
                
                if campos[5].strip() == "":
                    temperatura = None 
                else:
                    temperatura = float(campos[5]) 
                sensacion_termica = convertir_sen_termica(campos[6].strip())
            
                fecha = campos[1].strip() if campos[1].strip() != "" else None
                hora = campos[2].strip() if campos[2].strip() != "" else None
                condicion = campos[3].strip() if campos[3].strip() != "" else None
                visibilidad = campos[4].strip() if campos[4].strip() != "" else None
                humedad = campos[7].strip() if campos[7].strip() != "" else None
                presion = campos[9].strip() if campos[9].strip() != "" else None
            
            
                datos_ciudad = {
                    "fecha": fecha,
                    "hora":hora,
                    "condicion": condicion,
                    "visibilidad": visibilidad,
                    "temperatura": temperatura,
                    "sensacion_termica": sensacion_termica,
                    "humedad": humedad,
                    "direccion_viento": direccion,
                    "velocidad_viento": velocidad,
                    "presion": presion
                }
            
                observaciones[ciudad] = datos_ciudad

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta}'.")
        sys.exit(1)

    return observaciones
    


# agrego de funcion de cantidad de ciudades completas, es decir, que tengan sensacion termica calculada. 
def cantidad_ciudades_completas(observaciones: dict) -> int:
    contador = 0
    for datos in observaciones.values(): # values devuelve los valores del diccionario, que en este caso son los diccionarios de cada ciudad. 
        if datos["sensacion_termica"] is not None: # para comparar con none se pone is not None o is None, no se puede usar == o !=
            #por que no es un valor sino un objeto.
            contador += 1
    return contador

def cantidad_ciudades(observaciones: dict) -> int:
    return len(observaciones) # devuelve la cantidad de ciudades leidas.



# ------------------------------------------------------------------------------

def temperatura_maxima(observaciones: dict) -> list:
    maximo = None
    
    for ciudad, datos in observaciones.items(): # recorre el diccionario grande y cada vuelta la ciudad y los datos
        temperatura = datos["temperatura"]
        if maximo is None or temperatura > maximo: # si la temperatura es mayor que el maximo, se actualiza el maximo 
            maximo = temperatura 

    ciudades = []
    for ciudad, datos in observaciones.items():
        if datos["temperatura"] == maximo: # comparamos la temperatura de cada ciudad con el maximo encontrado
            ciudades.append(ciudad) # lo agregamos a la lista de ciudades que tienen la temperatura maxima 

    return ciudades 

def temperatura_minima(observaciones: dict) -> list:
    # copiá temperatura_maxima entera y cambiá el > por
    minimo = None
    
    for ciudad, datos in observaciones.items(): # recorre el diccionario grande y cada vuelta la ciudad y los datos
        temperatura = datos["temperatura"]
        if minimo is None or temperatura < minimo: # si la temperatura es menor que el minimo, se actualiza el minimo
            minimo = temperatura 

    ciudades = []
    for ciudad, datos in observaciones.items():
        if datos["temperatura"] == minimo: # comparamos la temperatura de cada ciudad con el minimo encontrado
            ciudades.append(ciudad) # lo agregamos a la lista de ciudades que tienen la temperatura minima

    return ciudades 

# ---------------------------------------------------------------------------

# esta funcion queda casi identica solo le cambie el nombre de la variable de temperatura a velocidad del viento, y el nombre de la funcion.
def velocidad_viento_maxima(observaciones: dict) -> list:
    maximo = None
    
    for ciudad, datos in observaciones.items():
        velocidad = datos["velocidad_viento"] 
        if maximo is None or velocidad > maximo: 
            maximo = velocidad 

    ciudades = []
    for ciudad, datos in observaciones.items():
        if datos["velocidad_viento"] == maximo:
            ciudades.append(ciudad) 

    return ciudades 


def velocidad_viento_minima(observaciones: dict) -> list:
    minimo = None
    
    for ciudad, datos in observaciones.items():
        velocidad = datos["velocidad_viento"] 
        if minimo is None or velocidad < minimo: 
            minimo = velocidad 

    ciudades = []
    for ciudad, datos in observaciones.items():
        if datos["velocidad_viento"] == minimo:
            ciudades.append(ciudad) 

    return ciudades 


# def top_n_ciudades lo converti a lista y ordene esas listas. 
# aca busca primero el mas alto en cada ronda 
def top_n_mayores(observaciones: dict, campo: str, n: int) -> list:
    lista = []
    for ciudad, datos in observaciones.items():
        lista.append((ciudad, datos[campo]))

    resultado = []

    for _ in range(n):
        if len(lista) == 0:
            break

        mejor_indice = 0
        for i in range(1, len(lista)):
            if lista[i][1] > lista[mejor_indice][1]:
                mejor_indice = i

        ciudad_elegida, valor_elegido = lista[mejor_indice]
        resultado.append(ciudad_elegida)
        lista.pop(mejor_indice)

    return resultado

# y este busca el mas bajo en cada ronda
def top_n_menores(observaciones: dict, campo: str, n: int) -> list:
    lista = []
    for ciudad, datos in observaciones.items():
        lista.append((ciudad, datos[campo]))

    resultado = []

    for _ in range(n):
        if len(lista) == 0:
            break

        mejor_indice = 0
        for i in range(1, len(lista)):
            if lista[i][1] < lista[mejor_indice][1]:
                mejor_indice = i

        ciudad_elegida, valor_elegido = lista[mejor_indice]
        resultado.append(ciudad_elegida)
        lista.pop(mejor_indice)

    return resultado


def mostrar_resumen(observaciones: dict) -> None:
    print("=== RESUMEN OBSERVACIONES SMN ===")
    print(f"Cantidad de ciudades leídas: {cantidad_ciudades(observaciones)}")
    print(f"Ciudades con datos completos: {cantidad_ciudades_completas(observaciones)}")
    print()
    print(f"Temperatura máxima en: {temperatura_maxima(observaciones)}")
    print(f"Temperatura mínima en: {temperatura_minima(observaciones)}")
    print()
    print(f"Viento máximo en: {velocidad_viento_maxima(observaciones)}")
    print(f"Viento mínimo en: {velocidad_viento_minima(observaciones)}")
    print(f"Top 5 ciudades más cálidas: {top_n_mayores(observaciones, 'temperatura', 5)}")
    print(f"Top 5 ciudades más frías: {top_n_menores(observaciones, 'temperatura', 5)}")
    print(f"Top 5 ciudades con más viento: {top_n_mayores(observaciones, 'velocidad_viento', 5)}")
    print(f"Top 5 ciudades con menos viento: {top_n_menores(observaciones, 'velocidad_viento', 5)}")
    


# ------

if len(sys.argv) < 2:
    print("Error: falta indicar la ruta del archivo.")
    print("Uso: python analisisclima.py datos/observaciones_smn.txt")
    sys.exit(1)
        # para que no me salga error de indexacion cuando solo le paso el script de python analisisclima.py,
        # le agrego este bloque para que entre al if y me imprima que es lo que falta (en caso de que falte)
    


# para llamarlo desde la terminal
#  python analisisclima.py datos\estado_tiempo20260910.txt 
ruta = sys.argv[1]# --> [1] es el primer argumento que se escribio, es decir que en este caso  es la ruta del archivo.

observaciones = leer_observaciones(ruta)

# por si el archivo esta vacio, es decir len(observaciones) == 0
if len(observaciones) == 0:
    print(f"Error: el archivo '{ruta}' está vacío o no tiene datos válidos.")
    sys.exit(1)

mostrar_resumen(observaciones)