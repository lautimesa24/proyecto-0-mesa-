# Análisis de observaciones meteorológicas del SMN

Herramienta de línea de comandos en Python que lee las observaciones actuales
del Servicio Meteorológico Nacional, las guarda en un diccionario por
ciudad y las convierte a json.

## Cómo obtener los datos

1. Entrar a https://www.smn.gob.ar/descarga-de-datos
2. Descargar el archivo comprimido (.rar) de "Observaciones actuales".
3. Descomprimirlo (con WinRAR, 7-Zip o similar).
4. Guardar el .txt que queda adentro en la carpeta `datos/`.

## Modo de uso

Con un .txt del SMN (se detecta si está en utf-8 o latin-1, se convierte
a json y se guarda en `obs_json/`, que se crea si no existe):

    python smn.py datos/estado_tiempo20260924.txt

Con un .json ya convertido (informa la cantidad de ciudades):

    python smn.py obs_json/estado_tiempo20260924.json
   Ejemplo con un .json:

    archivo json, leyendo...
    lectura completada.
    ciudades en el archivo: 121
    ciudades informadas: 17
    
Sin argumentos (avisa e informa cuántos .txt y .json hay):

    python smn.py

Con más de un argumento, avisa y termina sin hacer nada.

## Ejemplo de salida

    archivo del SMN, leyendo observaciones...
    lectura completada.
    archivo del SMN, convirtiendo a json...
    conversión completada.
    guardando obs_json\estado_tiempo20260924.json...
    guardado completado.
    ciudades en el archivo: 121
    ciudades informadas: 17