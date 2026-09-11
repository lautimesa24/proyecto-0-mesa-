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

#prueba para ver si anda
#print(separar_viento("Sur  5"))
#print(separar_viento("Calma"))
#print(separar_viento("Noroeste  12")) 

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
            datos_ciudad = {
                "fecha": campos[1],
                "hora": campos[2],
                "condicion": campos[3],
                "visibilidad": campos[4],
                "temperatura": campos[5],
                "sensacion_termica": campos[6],
                "humedad": campos[7],
                "direccion_viento": direccion,
                "velocidad_viento": velocidad,
                "presion": campos[9]
            }
            observaciones[ciudad] = datos_ciudad
        return observaciones
    

observaciones = leer_observaciones("estado_tiempo20260910.txt")
print(f"Ciudades leídas: {len(observaciones)}")
print(f"Observaciones: {observaciones}")
