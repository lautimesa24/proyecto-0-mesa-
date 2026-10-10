import os
import sys
import json
import datetime


MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

CAMPOS_ESPERADOS = [
    "ciudad", "fecha", "hora", "condicion", "visibilidad",
    "temperatura", "sensacion_termica", "humedad", "viento", "presion"
]

CARPETA_JSON = "obs_json"

#  LECTURA 

def columnas_faltantes(cantidad_campos: int) -> int:
    return len(CAMPOS_ESPERADOS) - cantidad_campos


def separar_viento(campo_viento: str) -> tuple:
    partes = campo_viento.split()

    if partes[0] == "Calma":
        return ("Calma", 0)
    direccion = " ".join(partes[:-1])  # todo menos el último elemento es la dirección
    velocidad = float(partes[-1])
    return (direccion, velocidad)


def convertir_fecha_y_hora(campo_fecha: str, campo_hora: str):
    """Combina fecha ('10-septiembre-2026') y hora ('14:00') en un datetime.
    Si alguno de los dos falta, devuelve None."""
    if campo_fecha.strip() == "" or campo_hora.strip() == "":
        return None

    dia_str, mes_str, anio_str = campo_fecha.strip().split("-")
    mes_numero = MESES[mes_str.lower()]  # traducimos el nombre del mes a número

    hora_str, minuto_str = campo_hora.strip().split(":")

    return datetime.datetime(
        int(anio_str), mes_numero, int(dia_str),
        int(hora_str), int(minuto_str)
    )


def convertir_sen_termica(valor: str):
    if valor == "" or valor == "No se calcula":
        return None  # dato que falta: no se puede reemplazar por 0
    return float(valor)

# agregado de la función para detectar codificación 
def detectar_codificacion(ruta: str) -> str:
    """Devuelve 'utf-8' si el archivo se puede leer como utf-8, si no 'latin-1'."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            archivo.read()
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"



def leer_observaciones(ruta: str):
    observaciones = {}
    lineas_invalidas = 0
    detalle_lineas_invalidas = []

    try:
        codificacion = detectar_codificacion(ruta)
        #print("codificación detectada:", codificacion) # para saber que codificación se detectó... 
        with open(ruta, "r", encoding=codificacion) as archivo:
            for linea in archivo:
                linea = linea.strip()
                campos = linea.split(";")

                if len(campos) != 10:
                    lineas_invalidas += 1
                    faltan = columnas_faltantes(len(campos))
                    detalle_lineas_invalidas.append(f"Línea con {len(campos)} campos (le faltan {faltan} columnas)")
                    continue

                ciudad = campos[0].strip()

                if ciudad == "":
                    # sin nombre no se puede usar como clave: línea inválida
                    lineas_invalidas += 1
                    continue

                if campos[8].strip() == "":
                    direccion, velocidad = None, None
                else:
                    direccion, velocidad = separar_viento(campos[8])

                if campos[5].strip() == "":
                    temperatura = None
                else:
                    temperatura = float(campos[5])

                sensacion_termica = convertir_sen_termica(campos[6].strip())
                fecha_y_hora = convertir_fecha_y_hora(campos[1], campos[2])
                condicion = campos[3].strip() if campos[3].strip() != "" else None
                visibilidad = campos[4].strip() if campos[4].strip() != "" else None
                humedad = campos[7].strip() if campos[7].strip() != "" else None
                presion = campos[9].strip() if campos[9].strip() != "" else None

                datos_ciudad = {
                    "fecha_y_hora": fecha_y_hora,
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

    return observaciones, lineas_invalidas, detalle_lineas_invalidas


# CARACTERIZACIÓN 

def cantidad_ciudades(observaciones: dict) -> int:
    return len(observaciones)


def cantidad_ciudades_completas(observaciones: dict) -> int:
    contador = 0
    for datos in observaciones.values():
        if datos["sensacion_termica"] is not None:
            contador += 1
    return contador


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
    """Devuelve los horarios "HH:MM" en que reportaron las estaciones,
    sin repetir y ordenados de menor a mayor."""
    horarios = set()

    for ciudad, datos in observaciones.items():
        fecha_y_hora = datos["fecha_y_hora"]
        if fecha_y_hora is None:
            continue
        horarios.add(fecha_y_hora.strftime("%H:%M"))

    return sorted(horarios)


def top_n_ciudades(observaciones: dict, campo: str, n: int, orden: str) -> list:
    # lista de pares (ciudad, valor del campo)
    lista = []
    for ciudad, datos in observaciones.items():
        lista.append((ciudad, datos[campo]))

    resultado = []

    # selection sort: en cada vuelta se saca el mejor de los que quedan
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

    # si hay empate con el último valor que entró al top, se agregan también
    if len(resultado) > 0:
        ultimo_valor = None
        for ciudad, datos in observaciones.items():
            if ciudad == resultado[-1]:
                ultimo_valor = datos[campo]
                break

        for ciudad, valor in lista:
            if valor == ultimo_valor:
                resultado.append(ciudad)

    return resultado


# convertir a json 

def observaciones_a_json(observaciones: dict) -> dict:
    """Copia el diccionario pasando cada datetime a texto ISO 8601 sin segundos."""
    resultado = {}
    for ciudad, datos in observaciones.items():
        copia = dict(datos)  # copia, para no modificar el diccionario original
        if copia["fecha_y_hora"] is not None:
            copia["fecha_y_hora"] = copia["fecha_y_hora"].isoformat(timespec="minutes")
        resultado[ciudad] = copia
    return resultado


def ruta_json_de(ruta_txt: str) -> str:
    nombre = os.path.basename(ruta_txt)            # estado_tiempo20260924.txt
    nombre_sin_ext = os.path.splitext(nombre)[0]   # estado_tiempo20260924
    return os.path.join(CARPETA_JSON, nombre_sin_ext + ".json")


def mostrar_cantidades(observaciones: dict) -> None:
    print(f"ciudades en el archivo: {cantidad_ciudades(observaciones)}")
    print(f"ciudades informadas: {cantidad_ciudades_completas(observaciones)}")


def convertir_txt_a_json(ruta_txt: str) -> None:
    print("archivo del SMN, leyendo observaciones...")
    observaciones, lineas_invalidas, detalle = leer_observaciones(ruta_txt)
    if len(observaciones) == 0:
        print("no se pudo completar: el archivo está vacío o no tiene datos válidos.")
        return
    print("lectura completada.")

    print("archivo del SMN, convirtiendo a json...")
    datos_json = observaciones_a_json(observaciones)
    print("conversión completada.")

    if not os.path.exists(CARPETA_JSON):
        print(f"el directorio {CARPETA_JSON} no existe, creándolo...")
        try:
            os.makedirs(CARPETA_JSON)
        except OSError:
            print("no se pudo crear el directorio, no se guardó el json.")
            return
        print("directorio creado.")

    ruta_salida = ruta_json_de(ruta_txt)
    print(f"guardando {ruta_salida}...")
    
    try:
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            json.dump(datos_json, archivo, ensure_ascii=False, indent=2)
    except OSError:
        print("no se pudo guardar el archivo json.")
        return
    print("guardado completado.")

    mostrar_cantidades(observaciones)
    
def procesar_json(ruta_json: str) -> None:
    print("archivo json, leyendo...")
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            observaciones = json.load(archivo)
    except FileNotFoundError:
        print("no se pudo completar: el archivo no existe.")
        return
    except json.JSONDecodeError:
        print("no se pudo completar: el archivo json está mal formado.")
        return
    print("lectura completada.")
    mostrar_cantidades(observaciones)


def contar_archivos(carpeta: str, extension: str) -> int:
    if not os.path.isdir(carpeta):
        return 0  # si la carpeta no existe, hay 0 archivos
    contador = 0
    for nombre in os.listdir(carpeta):
        if nombre.endswith(extension):
            contador += 1
    return contador


def main() -> None:
    if len(sys.argv) > 2:
        print("Error: se pasó más de un parámetro. No se hace nada.")
        print("Uso: python smn.py datos/estado_tiempo20260924.txt")
        return

    if len(sys.argv) == 1:
        print("No se indicó ningún archivo. Uso: python smn.py datos/estado_tiempo20260924.txt")
        print(f"archivos .txt en datos/: {contar_archivos('datos', '.txt')}")
        print(f"archivos .json en {CARPETA_JSON}/: {contar_archivos(CARPETA_JSON, '.json')}")
        return

    ruta = sys.argv[1]
    if ruta.endswith(".txt"):
        convertir_txt_a_json(ruta)
    elif ruta.endswith(".json"):
        procesar_json(ruta)
    else:
        print("Error: solo se aceptan archivos .txt del SMN o .json.")


main()

# parte de PRESENTACIÓN 

def mostrar_resumen(observaciones: dict, lineas_invalidas: int, detalle_lineas_invalidas: list) -> None:
    print("=== RESUMEN OBSERVACIONES SMN ===")
    print(f"Cantidad de ciudades leídas: {cantidad_ciudades(observaciones)}")
    print(f"Ciudades con datos completos: {cantidad_ciudades_completas(observaciones)}")
    print()
    print(f"Temperatura máxima en: {top_n_ciudades(observaciones, 'temperatura', 1, 'mayor')}")
    print(f"Temperatura mínima en: {top_n_ciudades(observaciones, 'temperatura', 1, 'menor')}")
    print(f"Viento máximo en: {top_n_ciudades(observaciones, 'velocidad_viento', 1, 'mayor')}")
    print(f"Viento mínimo en: {top_n_ciudades(observaciones, 'velocidad_viento', 1, 'menor')}")
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

# para correrlo:
# python analisisclima.py datos/estado_tiempo20260924.txt 


