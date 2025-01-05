from flask import Flask, jsonify , request
from flask_cors import CORS
import json
import subprocess
import joblib
import pandas as pd
from collections import Counter

# Carga de modelos
clf = joblib.load('modelo_IA/modelo_clasificacion.pkl')  
reg = joblib.load('modelo_IA/modelo_regresion.pkl')  
le = joblib.load('modelo_IA/codificador_programa.pkl') 


def calcular_porcentajes(materiales):
    contador = Counter(materiales)
    total_materiales = len(materiales)

    porcentajes = {material: (cantidad / total_materiales) * 100 for material, cantidad in contador.items()}

    materiales_posibles = ['Algodon', 'Poliester', 'Lana', 'Elastano', 'Viscosa', 'Nylon', 'Seda', 'Fibra']
    for material in materiales_posibles:
        if material not in porcentajes:
            porcentajes[material] = 0.0

    return porcentajes, total_materiales

def estimar_peso(numero_prendas, peso_promedio_prenda=0.2):
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


app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/read-id', methods=['GET'])
def read_tid_1():
    try:
        # Ejecuta el script serial_port.py
        result = subprocess.run(
            ['python3', 'read_epc.py'], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Muestra la salida en la consola de Flask
        print("stdout:", result.stdout)  # Aquí se verá cualquier print del script
        print("stderr:", result.stderr)  # Aquí se verá cualquier error

        # Analiza la salida del script
        if result.returncode == 0:
            print(f'La salida del serial_port es {result}')
            return jsonify(json.loads(result.stdout)), 200
        else:
            return jsonify({"error": "Failed to read EPC"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/read-multi-id', methods=['GET'])
def read_multi_id_1():
    try:
        # Ejecuta el script read_multi_epc.py
        result = subprocess.run(
            ['python3', 'read_multi_epc.py'], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Muestra la salida en la consola de Flask
        print("stdout:", result.stdout)  # Aquí se verá cualquier print del script
        print("stderr:", result.stderr)  # Aquí se verá cualquier error

        # Analiza la salida del script
        if result.returncode == 0:
            print(f'La salida del serial_port es {result}')
            return jsonify(json.loads(result.stdout)), 200
        else:
            return jsonify({"error": "Failed to read EPC"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/predict-program', methods=['POST'])
def predict_program():
    try:
        data = request.get_json()
        materiales = data.get('materiales', [])

        if not materiales:
            return jsonify({"error": "No se proporcionaron materiales"}), 400

        input_df = preparar_datos(materiales)
        resultado = predecir_lavado(input_df)

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
