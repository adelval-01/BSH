import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

# Cargar el archivo CSV con los datos originales
data = pd.read_csv('lavados-etiquetados.csv')

# Separar entradas y salidas para los datos de prueba (últimos 2000)
X_test = data[['Algodon', 'Poliester', 'Lana', 'Elastano', 'Viscosa', 'Nylon', 'Seda', 'Fibra', 'Peso']].iloc[8000:]
y_class_test = data['Programa'].iloc[8000:]
y_reg_test = data[['Agua', 'Jabon', 'Temperatura']].iloc[8000:]

# Cargar los modelos entrenados y el codificador
clf = joblib.load('modelo_clasificacion.pkl')
reg = joblib.load('modelo_regresion.pkl')
le = joblib.load('codificador_programa.pkl')

# Codificar la salida categórica (Programa) para la prueba
y_class_test_encoded = le.transform(y_class_test)

# Realizar predicciones
y_class_pred = clf.predict(X_test)
y_reg_pred = reg.predict(X_test)

# Evaluar el clasificador
accuracy = accuracy_score(y_class_test_encoded, y_class_pred)
print(f"Exactitud del clasificador (Programa): {accuracy:.2f}")

# Evaluar el regresor
mse = mean_squared_error(y_reg_test, y_reg_pred)
r2 = r2_score(y_reg_test, y_reg_pred)
print(f"Error cuadrático medio (Agua, Jabon, Temperatura): {mse:.2f}")
print(f"Coeficiente de determinación R^2: {r2:.2f}")

# Mostrar algunos ejemplos de predicciones
for i in range(5):  # Muestra 5 ejemplos
    print("\nEjemplo:")
    print(f"Entrada: {X_test.iloc[i].to_dict()}")
    print(f"Programa real: {y_class_test.iloc[i]}, Predicho: {le.inverse_transform([y_class_pred[i]])[0]}")
    print(f"Valores reales (Agua, Jabon, Temperatura): {y_reg_test.iloc[i].values}")
    print(f"Valores predichos: {y_reg_pred[i]}")
