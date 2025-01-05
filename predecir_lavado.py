import json
from typing import Counter
import joblib
import pandas as pd

# Primero cargamos los modelos
clf = joblib.load('modelo_IA/modelo_clasificacion.pkl')  
reg = joblib.load('modelo_IA/modelo_regresion.pkl')  
le = joblib.load('modelo_IA/codificador_programa.pkl') 

def calcular_porcentajes(materiales):
    contador = Counter(materiales)
    
    total_materiales = len(materiales)
    
    # Calcular el porcentaje de cada material
    porcentajes = {material: (cantidad / total_materiales) * 100 for material, cantidad in contador.items()}
    
    # Asegurarse de que todos los materiales posibles tengan un porcentaje (incluso si no están en el vector)
    materiales_posibles = ['Algodon', 'Poliester', 'Lana', 'Elastano', 'Viscosa', 'Nylon', 'Seda', 'Fibra']
    for material in materiales_posibles:
        if material not in porcentajes:
            porcentajes[material] = 0.0
    
    return porcentajes, total_materiales

# Función para estimar el peso en función del número de prendas
def estimar_peso(numero_prendas,peso_promedio_prenda=0.2):
    peso_estimado = numero_prendas * peso_promedio_prenda  
    return peso_estimado

def preparar_datos(materiales):

    porcentajes, numero_prendas = calcular_porcentajes(materiales)
    
    peso_estimado = estimar_peso(numero_prendas)
    
    input_df = pd.DataFrame([{
        'Algodon': porcentajes['Algodon'],
        'Poliester': porcentajes['Poliester'],
        'Lana': porcentajes['Lana'],
        'Elastano': porcentajes['Elastano'],
        'Viscosa': porcentajes['Viscosa'],
        'Nylon': porcentajes['Nylon'],
        'Seda': porcentajes['Seda'],
        'Fibra': porcentajes['Fibra'],
        'Peso': peso_estimado  
    }])
    
    return input_df



def predecir_lavado(df):
    
    
    programa_pred = clf.predict(df)
    programa = le.inverse_transform(programa_pred)[0]  # Convertir el valor codificado al nombre del programa
    
    # Realizar las predicciones de cantidad de agua, jabón y temperatura (regresión)
    agua_pred, jabon_pred, temperatura_pred = reg.predict(df)[0]
    
    # Crear un diccionario con las predicciones
    resultado = {
        'Programa': programa,
        'Agua': agua_pred,
        'Jabon': jabon_pred,
        'Temperatura': temperatura_pred
    }
    
    # Convertir el diccionario a JSON y devolverlo
    return json.dumps(resultado, indent=4)



# Ejemplo de entrada
materiales = ['Algodon', 'Algodon', 'Lana', 'Lana', 'Algodon', 'Poliester', 'Lana']

# Preparar los datos para la predicción
input_df = preparar_datos(materiales)

# Realizar la predicción
resultado_json = predecir_lavado(input_df)

# Mostrar el resultado
print(resultado_json)