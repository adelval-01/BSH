import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import export_graphviz
from subprocess import call
from IPython.display import Image
import joblib
from IPython.display import display

# Cargar datos y modelos
data = pd.read_csv('lavados-etiquetados.csv')
clf = joblib.load('modelo_clasificacion.pkl')
reg = joblib.load('modelo_regresion.pkl')
le = joblib.load('codificador_programa.pkl')

# Separar datos de prueba
X_test = data[['Algodon', 'Poliester', 'Lana', 'Elastano', 'Viscosa', 'Nylon', 'Seda', 'Fibra', 'Peso']].iloc[8000:]
y_class_test = data['Programa'].iloc[8000:]
y_reg_test = data[['Agua', 'Jabon', 'Temperatura']].iloc[8000:]

# Codificar la salida categórica
y_class_test_encoded = le.transform(y_class_test)
y_class_pred = clf.predict(X_test)
y_reg_pred = reg.predict(X_test)

# Función 1: Visualizar un árbol del bosque
def visualizar_arboles():
    # Iterar sobre todos los árboles en el Random Forest
    for i, tree in enumerate(clf.estimators_):
        # Exportar cada árbol a un archivo .dot
        export_graphviz(
            tree,
            out_file=f'tree_{i}.dot',  # Guardar cada árbol con un nombre único
            feature_names=X_test.columns,
            class_names=le.classes_,
            filled=True,
            rounded=True,
            special_characters=True
        )

        # Convertir el archivo .dot a .png usando Graphviz
        call(['dot', '-Tpng', f'tree_{i}.dot', '-o', f'tree_{i}.png', '-Gdpi=300'])

        # Mostrar la imagen (si usas Jupyter, si no, omite esta línea)
        img = Image(filename=f'tree_{i}.png')
        display(img)

# Función 2: Importancia de características
def importancia_caracteristicas():
    feature_importances = clf.feature_importances_
    features = X_test.columns
    plt.figure(figsize=(10, 6))
    plt.barh(features, feature_importances, color='skyblue')
    plt.xlabel('Importancia de la característica')
    plt.title('Importancia de las características (Clasificador)')
    plt.savefig('importancia_caracteristicas.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Gráfico de importancia de características guardado como 'importancia_caracteristicas.png'")


# Función 3: Matriz de confusión
def matriz_confusion():
    cm = confusion_matrix(y_class_test_encoded, y_class_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    disp.plot(cmap='Blues')
    plt.title('Matriz de Confusión (Clasificador)')
    plt.savefig('matriz_confusion.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Matriz de confusión guardada como 'matriz_confusion.png'")


# Función 4: Comparación real vs predicho
def comparacion_real_predicho():
    for i, col in enumerate(y_reg_test.columns):
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=y_reg_test[col], y=y_reg_pred[:, i], color='blue', alpha=0.6)
        plt.plot([y_reg_test[col].min(), y_reg_test[col].max()], 
                 [y_reg_test[col].min(), y_reg_test[col].max()], 
                 color='red', linestyle='--')
        plt.xlabel(f'Valores reales ({col})')
        plt.ylabel(f'Valores predichos ({col})')
        plt.title(f'Valores reales vs predichos ({col})')
        plt.savefig(f'comparacion_real_predicho_{col}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Gráfico de comparación real vs predicho guardado como 'comparacion_real_predicho_{col}.png'")


def distribucion_errores():
    errores = y_reg_test - y_reg_pred
    for i, col in enumerate(errores.columns):
        plt.figure(figsize=(8, 6))
        sns.histplot(errores[col], kde=True, color='purple', bins=30)
        plt.xlabel(f'Error ({col})')
        plt.title(f'Distribución de errores ({col})')
        plt.savefig(f'distribucion_errores_{col}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Distribución de errores guardada como 'distribucion_errores_{col}.png'")


# Llamar a todas las funciones
if __name__ == '__main__':
    visualizar_arboles()
    # importancia_caracteristicas()
    # matriz_confusion()
    # comparacion_real_predicho()
    # distribucion_errores()
