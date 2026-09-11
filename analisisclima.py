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
