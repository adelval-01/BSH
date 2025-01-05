import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Cargar el archivo CSV
data = pd.read_csv('lavados-etiquetados.csv')  # Asegúrate de que el archivo tenga las columnas correctas

# Separar entradas y salidas
X = data[['Algodon', 'Poliester', 'Lana', 'Elastano', 'Viscosa', 'Nylon', 'Seda', 'Fibra', 'Peso']]
y_class = data['Programa']
y_reg = data[['Agua', 'Jabon', 'Temperatura']]

# Codificar la salida categórica (Programa)
le = LabelEncoder()
y_class_encoded = le.fit_transform(y_class)

# Separar los primeros 8000 para entrenamiento y los últimos 2000 para prueba
X_train = X.iloc[:8000]
X_test = X.iloc[8000:]
y_class_train = y_class_encoded[:8000]
y_class_test = y_class_encoded[8000:]
y_reg_train = y_reg.iloc[:8000]
y_reg_test = y_reg.iloc[8000:]

# Modelos
clf = RandomForestClassifier(random_state=42)
reg = RandomForestRegressor(random_state=42)

# Entrenar los modelos con los datos de entrenamiento
clf.fit(X_train, y_class_train)
reg.fit(X_train, y_reg_train)

# Guardar los modelos entrenados y el codificador
joblib.dump(clf, 'modelo_clasificacion.pkl')
joblib.dump(reg, 'modelo_regresion.pkl')
joblib.dump(le, 'codificador_programa.pkl')

print("Modelos entrenados y guardados correctamente.")
