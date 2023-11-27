import requests
import json
import matplotlib.pyplot as plt
import statistics
import pandas as pd

def consultar_api(opcion):
    url = f'https://swapi.dev/api/{opcion}/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error en la consulta a la API ({response.status_code})")
        return None


def guardar_en_archivo(nombre_archivo, contenido):
    try:
        with open(nombre_archivo, 'w') as file:
            file.write(json.dumps(contenido, indent=2))
        print(f"Información guardada en {nombre_archivo}")
        df = pd.DataFrame(contenido.get('results', []))
        excel_nombre_archivo = f"{nombre_archivo}.xlsx"
        df.to_excel(excel_nombre_archivo, index=False)
        print(f"Información guardada en {excel_nombre_archivo}")
    except FileNotFoundError:
        print(f"El directorio o archivo {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al guardar la información: {e}")
    with open(nombre_archivo, 'w') as file:
        file.write(json.dumps(contenido, indent=2))


def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            contenido = json.load(file)
        return contenido
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe.")
        return None

def analizar_datos(datos):
    resultados = datos.get('results', [])

    if resultados:
        
        if any('height' in persona for persona in resultados):
            alturas = [int(persona['height']) for persona in resultados if 'height' in persona]
            promedio_alturas = statistics.mean(alturas)
            print(f"Promedio de alturas: {promedio_alturas} cm")
        else:
            print("La información no contiene datos de altura.")
    else:
        print("La información no contiene resultados.")

def generar_graficas(datos):
    resultados = datos.get('results', [])

    if resultados:
        if any('height' in persona for persona in resultados):
            personas_con_altura = [persona for persona in resultados if 'height' in persona]
            alturas = [int(persona['height']) for persona in personas_con_altura]
            plt.hist(alturas, bins=20, color='blue', edgecolor='black')
            plt.title('Histograma de Alturas de Personajes de Star Wars')
            plt.xlabel('Altura (cm)')
            plt.ylabel('Frecuencia')
            plt.show()
        else:
            print("La información no contiene datos de altura.")
    else:
        print("La información no contiene resultados.")

while True:
    print("\nMenú Principal:")
    print("1. Consultar información de la API")
    print("2. Consultar información almacenada")
    print("3. Salir")

    opcion_menu = input("Seleccione una opción: ")

    if opcion_menu == '1':
        print("Opciones disponibles para consultar:")
        print(" - people")
        print(" - films")
        print(" - starships")
        print(" - vehicles")
        print(" - species")
        print(" - planets")
        
        opcion_api = input("Ingrese la opción de la API que desea consultar: ")
        datos_api = consultar_api(opcion_api)

        if datos_api:
            print("Información consultada:")
            print(json.dumps(datos_api, indent=2))

            decision = input("¿Desea guardar la información? (Si/No): ")
            if decision.lower() == 'si':
                nombre_archivo = f"{opcion_api}_consulta.txt"
                guardar_en_archivo(nombre_archivo, datos_api)
                print(f"Información guardada en {nombre_archivo}")

    elif opcion_menu == '2':
        nombre_archivo = input("Ingrese el nombre del archivo que desea consultar: ")
        datos_almacenados = leer_archivo(nombre_archivo)

        if datos_almacenados:
            print("Información almacenada:")
            print(json.dumps(datos_almacenados, indent=2))

            analizar_datos(datos_almacenados)
            generar_graficas(datos_almacenados)

    elif opcion_menu == '3':
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
