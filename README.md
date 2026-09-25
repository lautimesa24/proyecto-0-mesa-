analisis del clima: proyecto 0 
# Trabajo Práctico: Análisis de Observaciones Meteorológicas del SMN

Herramienta de línea de comandos desarrollada en Python para la lectura, limpieza, procesamiento y análisis estadístico de los datos en vivo de observaciones actuales del **Servicio Meteorológico Nacional (SMN)**.

---

## Descripción de lo que hace el proyecto

El programa tiene estas funcionalidades principales:

* **Lectura completa:** este programa Procesa archivos de texto plano separados por punto y coma(;), ignorando líneas mal formadas o sin ciudad válida sin interrumpir la ejecución.
* **Limpieza de datos:** Limpia los espacios en blanco sobrantes en los nombres de las estaciones y maneja los datos faltantes (como la sensación térmica con el valor "No se calcula").
* **Procesamiento de viento:** Separa el campo de viento combinado (por ejemplo, `"Sur 5"`) en dirección y velocidad independientes, contemplando correctamente el estado de `"Calma"`.
* **Cálculo de estadísticas:** Obtiene temperaturas mas altas, vientos extremos, recuento de estaciones totales y completamente completas, además de rankings (Top $n$) de ciudades más cálidas, más frías, con más y con menos viento( esto es configurable )

---

## Cómo obtener los datos de entrada

1. Ingresar a la página oficial de descarga de datos del SMN: 
   [https://www.smn.gob.ar/descarga-de-datos](https://www.smn.gob.ar/descarga-de-datos)
2. Descargar el archivo comprimido (`.rar`) correspondiente a **Observaciones actuales**.
3. Descomprimir el archivo para obtener el archivo de texto plano (por ejemplo, `estado_tiempo20260910.txt`).
4. Guardar dicho archivo dentro de la carpeta **`datos/`** de este repositorio.

---

## Modo de Uso

Ejecutar el script desde la terminal pasando como argumento la ruta del archivo de texto:
```bash
python analisisclima.py datos\estado_tiempo20260924.tx 
