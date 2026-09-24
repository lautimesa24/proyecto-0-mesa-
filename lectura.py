import sys
#agrego de manejo de argumentos con sys
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


def columnas_faltantes(cantidad_campos: int) -> int:
    return len(CAMPOS_ESPERADOS) - cantidad_campos


def separar_viento(campo_viento: str) -> tuple:
    partes = campo_viento.split()
    
    if partes[0] == "Calma":
        return ("Calma", 0)
    direccion = " ".join(partes[:-1]) # se toma todos los elementos excepto el último como dirección. 
    velocidad = float(partes[-1])
    return (direccion, velocidad)


def convertir_fecha_y_hora(campo_fecha: str, campo_hora: str):
    """Combina los campos de fecha ('10-septiembre-2026') y hora ('14:00')
    en un único objeto datetime.datetime. Si alguno de los dos falta, devuelve None."""
    
    
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
    if valor == "" or valor == "No se calcula": # 
        return None # lo deje como none por que es un dato que no esta y no hay forma de calcularlo como para dejarlo en 0. 
    return float(valor)



def leer_observaciones(ruta:str)->dict:
    observaciones= {}
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
                # campos[x].strip dentro del if es el valor que se va a guardar si la condicion es verdadera.  
                fecha_y_hora = convertir_fecha_y_hora(campos[1], campos[2])  
                condicion = campos[3].strip() if campos[3].strip() != "" else None # esto va a valer esto campos[3].strip(), si campos[3].strip()es distino a vacio "" y si esta vacio fecha o cualquier otra cosa va a valer None.
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