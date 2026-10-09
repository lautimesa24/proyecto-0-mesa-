import sys
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


def leer_observaciones(ruta: str):
    observaciones = {}
    lineas_invalidas = 0
    detalle_lineas_invalidas = []

    try:
        with open(ruta, "r", encoding="latin-1") as archivo:
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


# PROGRAMA 

if len(sys.argv) < 2:
    print("Error: falta indicar la ruta del archivo.")
    print("Uso: python analisisclima.py datos/estado_tiempo20260924.txt")
    sys.exit(1)

ruta = sys.argv[1]
observaciones, lineas_invalidas, detalle_lineas_invalidas = leer_observaciones(ruta)

if len(observaciones) == 0:
    print(f"Error: el archivo '{ruta}' está vacío o no tiene datos válidos.")
    sys.exit(1)

mostrar_resumen(observaciones, lineas_invalidas, detalle_lineas_invalidas) 

# para correrlo:
# python analisisclima.py datos/estado_tiempo20260924.txt