from lectura import leer_observaciones # MODULO AGREGADO 
import sys 

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


def faltantes_por_campo(observaciones: dict) -> dict:
    campos_internos = [
        "fecha_y_hora", "condicion", "visibilidad", "temperatura",
        "sensacion_termica", "humedad", "direccion_viento",
        "velocidad_viento", "presion"
    ]

    resultado = {}

    for campo in campos_internos:
        ciudades_con_faltante = []
        for ciudad, datos in observaciones.items():
            if datos[campo] is None:
                ciudades_con_faltante.append(ciudad)
        resultado[campo] = ciudades_con_faltante

    return resultado

def horarios_reportados(observaciones: dict) -> list:
    """devuelve una lista de los horarios a los que las estaciones reportaron en la observación dada.
    La lista tendrá horas en el formato string "HH:MM", será sin repetir y ordenadas de menor a mayor"""
    horarios = set()  # el set es para que no se repitan solos

    for ciudad, datos in observaciones.items():
        fecha_y_hora = datos["fecha_y_hora"]
        if fecha_y_hora is None:
            continue  # si a esta ciudad le falta la fecha/hora, la salteamos

        hora_texto = fecha_y_hora.strftime("%H:%M")  # formatea el datetime como "HH:MM"
        horarios.add(hora_texto)

    return sorted(horarios)  # sorted convierte el set en lista y de paso lo ordena

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


def top_n_ciudades(observaciones: dict, campo: str, n: int, orden: str) -> list:
    lista = []
    for ciudad, datos in observaciones.items():
        lista.append((ciudad, datos[campo]))

    resultado = []

    for _ in range(n):
        if len(lista) == 0:
            break

        mejor_indice = 0
        for i in range(1, len(lista)):
            if orden == "mayor" and lista[i][1] > lista[mejor_indice][1]:
                mejor_indice = i
            elif orden == "menor" and lista[i][1] < lista[mejor_indice][1]:
                mejor_indice = i

        ciudad_elegida, valor_elegido = lista[mejor_indice]
        resultado.append(ciudad_elegida)
        lista.pop(mejor_indice)

    return resultado


def mostrar_resumen(observaciones: dict, lineas_invalidas: int, detalle_lineas_invalidas: list) -> None:
    print("=== RESUMEN OBSERVACIONES SMN ===")
    print(f"Cantidad de ciudades leídas: {cantidad_ciudades(observaciones)}")
    print(f"Ciudades con datos completos: {cantidad_ciudades_completas(observaciones)}")
    print()
    print(f"Temperatura máxima en: {temperatura_maxima(observaciones)}")
    print(f"Temperatura mínima en: {temperatura_minima(observaciones)}")
    print(f"Viento máximo en: {velocidad_viento_maxima(observaciones)}")
    print(f"Viento mínimo en: {velocidad_viento_minima(observaciones)}")
    print(f"Top 5 ciudades más cálidas: {top_n_ciudades(observaciones, 'temperatura', 5, 'mayor')}")
    print(f"Top 5 ciudades más frías: {top_n_ciudades(observaciones, 'temperatura', 5, 'menor')}")
    print(f"Top 5 ciudades con más viento: {top_n_ciudades(observaciones, 'velocidad_viento', 5, 'mayor')}")
    print(f"Top 5 ciudades con menos viento: {top_n_ciudades(observaciones, 'velocidad_viento', 5, 'menor')}")
    print(f"Líneas inválidas encontradas: {lineas_invalidas}")
    for detalle in detalle_lineas_invalidas:
        print(f" --- {detalle}")
    print(horarios_reportados(observaciones))
    print("=== DATOS FALTANTES POR CAMPO ===")
    faltantes = faltantes_por_campo(observaciones)
    for campo, ciudades in faltantes.items():
        if len(ciudades) > 0:
            print(f"{campo}: faltan {len(ciudades)} ({', '.join(ciudades[:5])}{'...' if len(ciudades) > 5 else ''})")



if len(sys.argv) < 2:
    print("Error: falta indicar la ruta del archivo.")
    print("Uso: python analisisclima.py datos/observaciones_smn.txt")
    sys.exit(1)
        # para que no me salga error de indexacion cuando solo le paso el script de python analisisclima.py,
        # le agrego este bloque para que entre al if y me imprima que es lo que falta (en caso de que falte)
    
# para llamarlo desde la terminal
# python analisisclima.py datos\estado_tiempo20260924.tx
 
ruta = sys.argv[1]# --> [1] es el primer argumento que se escribio, es decir que en este caso  es la ruta del archivo.
observaciones, lineas_invalidas, detalle_lineas_invalidas = leer_observaciones(ruta)

# por si el archivo esta vacio, es decir len(observaciones) == 0
if len(observaciones) == 0:
    print(f"Error: el archivo '{ruta}' está vacío o no tiene datos válidos.")
    sys.exit(1)
    
mostrar_resumen(observaciones, lineas_invalidas, detalle_lineas_invalidas)