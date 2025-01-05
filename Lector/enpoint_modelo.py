from flask import Flask, jsonify , request
from flask_cors import CORS
import json
import subprocess
import joblib
import pandas as pd
from collections import Counter

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Carga de modelos
clf = joblib.load('../modelo_IA/modelo_clasificacion.pkl')  
reg = joblib.load('../modelo_IA/modelo_regresion.pkl')  
le = joblib.load('../modelo_IA/codificador_programa.pkl') 


def calcular_porcentajes(materiales):
    contador = Counter(materiales)
    total_materiales = len(materiales)

    porcentajes = {material: (cantidad / total_materiales) * 100 for material, cantidad in contador.items()}

    materiales_posibles = ['Algodon', 'Poliester', 'Lana', 'Elastano', 'Viscosa', 'Nylon', 'Seda', 'Fibra']
    for material in materiales_posibles:
        if material not in porcentajes:
            porcentajes[material] = 0.0

    return porcentajes, total_materiales

def estimar_peso(numero_prendas, peso_promedio_prenda=0.7):
    return numero_prendas * peso_promedio_prenda

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
    programa = le.inverse_transform(programa_pred)[0]

    agua_pred, jabon_pred, temperatura_pred = reg.predict(df)[0]

    resultado = {
        'Programa': programa,
        'Agua': agua_pred,
        'Jabon': jabon_pred,
        'Temperatura': temperatura_pred
    }

    return resultado

@app.route('/predict-program', methods=['POST'])
def predict_program():
    try:
        data = request.get_json()
        materiales = data.get('materiales', [])
        print("Materiales recibidos: " + str(materiales))
        if not materiales:
            return jsonify({"error": "No se proporcionaron materiales"}), 400

        input_df = preparar_datos(materiales)
        resultado = predecir_lavado(input_df)

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)