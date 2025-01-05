from flask import Flask, jsonify
from flask_cors import CORS
import json
import subprocess

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
