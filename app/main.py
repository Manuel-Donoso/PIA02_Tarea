import boto3
import os

# Configuración del cliente de AWS Rekognition
# Nota: Las credenciales se cargarán automáticamente desde las variables de entorno de Docker
rekognition = boto3.client('rekognition', region_name='us-east-1')

def es_matricula_valida(texto, confianza):
    """
    Filtros solicitados:
    - Confianza > 90%
    - Longitud entre 5 y 10 caracteres
    - Al menos una letra y un número
    """
    texto_limpio = texto.replace(" ", "").replace("-", "")
    
    tiene_letra = any(c.isalpha() for c in texto_limpio)
    tiene_numero = any(c.isdigit() for c in texto_limpio)
    
    return confianza > 90 and 5 <= len(texto_limpio) <= 10 and tiene_letra and tiene_numero

def analizar_carpeta(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        print(f"❌ Error: La ruta '{ruta_carpeta}' no es accesible.")
        return

    # Listar archivos de imagen
    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"📂 Encontradas {len(archivos)} imágenes en {ruta_carpeta}\n" + "-"*40)

    for nombre_archivo in archivos:
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        
        with open(ruta_completa, 'rb') as image_file:
            imagen_bytes = image_file.read()

        # 1. PASO: Detectar si hay vehículos
        respuesta_labels = rekognition.detect_labels(
            Image={'Bytes': imagen_bytes},
            MinConfidence=90
        )

        # Filtramos por las etiquetas solicitadas
        etiquetas_vehiculo = {"Car", "Vehicle", "Automobile"}
        hay_vehiculo = any(label['Name'] in etiquetas_vehiculo for label in respuesta_labels['Labels'])

        if hay_vehiculo:
            print(f"🔍 {nombre_archivo}: VEHÍCULO DETECTADO. Buscando matrícula...")
            
            # 2. PASO: Detectar texto para encontrar matrículas
            respuesta_texto = rekognition.detect_text(Image={'Bytes': imagen_bytes})
            
            matriculas_encontradas = []
            for deteccion in respuesta_texto['TextDetections']:
                texto = deteccion['DetectedText']
                confianza = deteccion['Confidence']
                tipo = deteccion['Type']

                if tipo == 'LINE' and es_matricula_valida(texto, confianza):
                    matriculas_encontradas.append(texto)

            if matriculas_encontradas:
                # Usamos set() para evitar duplicados si Rekognition lee lo mismo varias veces
                print(f"   ✅ MATRÍCULAS: {', '.join(set(matriculas_encontradas))}")
            else:
                print("   ⚠️ No se detectaron matrículas que cumplan los requisitos.")
        else:
            print(f"🔍 {nombre_archivo}: No se detectaron coches.")

if __name__ == "__main__":
    print("--- AWS Rekognition - Detector de Matrículas ---")
    # Al usar Docker, la ruta será /data (mapeada a la carpeta 'imagenes')
    ruta = input("Introduce la ruta de la carpeta de imágenes (en Docker usa /data): ")
    analizar_carpeta(ruta)