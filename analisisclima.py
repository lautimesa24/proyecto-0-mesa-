#requerimiento:
# separación del viento 
# direccion--> texto 
# velocidad --> numero (a mi parecer seria 0 ya que  expresarlo con el 0 representaria la velocidad minima del viento, es decir, que no hay viento)
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
    if valor == "No se calcula": # 
        return None # lo deje como none por que es  none por que es un dato que no esta y no hay forma de calcularlo como para dejarlo en 0. 
    return float(valor)

def leer_observaciones(ruta:str)->dict:
    observaciones= {}
    lineas_invalidas = 0
    with open("estado_tiempo20260910.txt", "r", encoding="latin-1") as archivo:
        for linea in archivo:
            linea = linea.strip()
            campos = linea.split(";")
        
            if len(campos) != 10:
                lineas_invalidas += 1
                continue
            
            ciudad = campos[0].strip()
            direccion, velocidad = separar_viento(campos[8]) # 8 son los campos en horizontal
            temperatura = float(campos[5])
            sensacion_termica = convertir_sen_termica(campos[6].strip())
            
            datos_ciudad = {
                "fecha": campos[1],
                "hora": campos[2],
                "condicion": campos[3],
                "visibilidad": campos[4],
                "temperatura": temperatura,
                "sensacion_termica": sensacion_termica,
                "humedad": campos[7],
                "direccion_viento": direccion,
                "velocidad_viento": velocidad,
                "presion": campos[9]
            }
            
            observaciones[ciudad] = datos_ciudad

        return observaciones
    
# prueba para ver si anda
observaciones = leer_observaciones("estado_tiempo20260910.txt")

print(f"Observaciones: {observaciones}") 


# agrego de funcion de cantidad de ciudades completas, es decir, que tengan sensacion termica calculada. 
def cantidad_ciudades_completas(observaciones: dict) -> int:
    contador = 0
    for datos in observaciones.values(): # values devuelve los valores del diccionario, que en este caso son los diccionarios de cada ciudad. 
        if datos["sensacion_termica"] is not None: # para comparar con none se pone is not None o is None, no se puede usar == o !=
            #por que no es un valor sino un objeto.
            contador += 1
    return contador

print(f"Ciudades leídas: {len(observaciones)}")
print(f"Ciudades completas: {cantidad_ciudades_completas(observaciones)}")


