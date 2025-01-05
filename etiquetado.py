import pandas as pd

# === CONFIGURACIÓN ===
FILE_PATH = 'lavados.csv'
OUTPUT_FILE_PATH = 'lavados-etiquetados.csv'

# === FUNCIONES ===
def cargar_datos(file_path):
    """Carga los datos desde un archivo CSV y maneja posibles errores."""
    try:
        print("Cargando datos...")
        data = pd.read_csv(file_path)
        print("Datos cargados correctamente.")
        return data
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'. Verifica la ruta.")
        exit()
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        exit()

def limpiar_datos(data):
    """
    Limpia el conjunto de datos eliminando filas con valores no numéricos
    y columnas clave con valores nulos o incorrectos.
    """
    print("Limpiando datos...")
    columnas_clave = ['Algodon', 'Peso']
    data_cleaned = data.dropna(subset=columnas_clave)
    
    # Validar que los valores sean numéricos y positivos
    for columna in columnas_clave:
        data_cleaned = data_cleaned[data_cleaned[columna].apply(lambda x: str(x).replace('.', '', 1).isdigit())]
        data_cleaned = data_cleaned[data_cleaned[columna].astype(float) > 0]
    
    # Convertir todas las columnas necesarias a numérico
    columnas_a_convertir = ['Algodon', 'Poliester', 'Lana', 'Elastano',
                            'Viscosa', 'Nylon', 'Seda', 'Fibra', 'Peso']
    data_cleaned[columnas_a_convertir] = data_cleaned[columnas_a_convertir].apply(pd.to_numeric)
    
    print("Datos limpiados correctamente.")
    return data_cleaned

def recomendar_programa(row):
    """
    Selecciona un programa de lavado basado en la composición de los materiales.
    Prioriza los programas en el siguiente orden: Algodón > Lana > Delicados > Sintéticos > Mixto.
    """
    if row['Algodon'] >= 70:
        return 'Algodón'
    elif row['Lana'] >= 50:
        return 'Lana'
    elif row['Seda'] >= 30 or row['Viscosa'] >= 30:
        return 'Delicados'
    elif row['Poliester'] >= 50 or row['Nylon'] >= 50:
        return 'Sintéticos'
    else:
        return 'Mixto'

def calcular_agua(row):
    """Calcula la cantidad de agua en litros basada en el peso y la composición."""
    return 30 + (row['Peso'] * 6)  # Base: 30L + 6L por kg

def calcular_jabon(row):
    """Calcula la cantidad de jabón en mililitros basada en el peso."""
    return 15 + (row['Peso'] * 2.5)  # Base: 15ml + 2.5ml por kg

def calcular_temperatura(row):
    """
    Determina la temperatura ideal de lavado según la composición:
    - Algodón: 60°C
    - Lana, Seda: 30°C
    - Sintéticos: 40°C
    - Mixto: 40°C
    """
    if row['Algodon'] >= 70:
        return 60
    elif row['Lana'] >= 50 or row['Seda'] >= 30:
        return 30
    elif row['Poliester'] >= 50:
        return 40
    else:
        return 40

# === FLUJO PRINCIPAL ===
if __name__ == "__main__":
    # 1. Cargar datos
    datos = cargar_datos(FILE_PATH)
    
    # 2. Limpiar datos
    datos_limpiados = limpiar_datos(datos)
    
    # 3. Calcular nuevas columnas
    print("Procesando datos...")
    datos_limpiados['Programa Recomendado'] = datos_limpiados.apply(recomendar_programa, axis=1)
    datos_limpiados['Cantidad Agua (L)'] = datos_limpiados.apply(calcular_agua, axis=1)
    datos_limpiados['Cantidad Jabon (ml)'] = datos_limpiados.apply(calcular_jabon, axis=1)
    datos_limpiados['Temperatura (°C)'] = datos_limpiados.apply(calcular_temperatura, axis=1)
    
    # 4. Exportar datos procesados
    datos_limpiados.to_csv(OUTPUT_FILE_PATH, index=False)
    print(f"Datos procesados y exportados a '{OUTPUT_FILE_PATH}'.")