# Proyecto: Detector de Matrículas con AWS Rekognition y Docker

Este proyecto consiste en una aplicación de Inteligencia Artificial que analiza imágenes de forma automática para detectar vehículos y extraer sus matrículas utilizando el servicio **AWS Rekognition**.

## Estructura del Proyecto

-   **app/**: Contiene el script principal `main.py` y el archivo de dependencias `requirements.txt`.
    
-   **imagenes/**: Carpeta local donde se almacenan las fotos a analizar (11 imágenes).
    
-   **docker-compose.yml**: Configuración para orquestar el contenedor y montar los volúmenes.
    
-   **.env**: Archivo (no incluido en el repositorio por seguridad) con las credenciales de AWS.
    

## Requisitos Previos

1.  Tener instalados **Docker** y **Docker Compose**.
    
2.  Disponer de credenciales activas de **AWS Learner Lab** (Access Key, Secret Key y Session Token).
    

## Cómo ejecutar la aplicación

1.  **Configurar credenciales**: Copia tus claves de AWS en el archivo `.env` en la raíz del proyecto.
    
2.  **Construir y arrancar el contenedor**: Ejecuta el siguiente comando en la terminal: `docker compose up --build`
    
3.  **Resultados**: El programa detectará automáticamente la carpeta `/data` (mapeada a `./imagenes`) y mostrará el análisis de cada foto en la terminal.
    

## Lógica de Filtrado de Matrículas

Para asegurar la validez de los datos detectados, se aplican los siguientes filtros:

-   **Confianza**: Superior al 90%.
    
-   **Longitud**: Entre 5 y 10 caracteres.
    
-   **Formato**: Debe contener al menos una letra y un número.
