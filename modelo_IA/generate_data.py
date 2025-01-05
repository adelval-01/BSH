import pandas as pd
import numpy as np

def generar_lavados_realistas(n=10000):
    lavados = []

    for _ in range(n):
        # Elegir un tipo de lavado
        tipo_lavado = np.random.choice(['Algodón', 'Mixto', 'Delicado', 'Deportivo', 'Sábanas/Toallas'])

        if tipo_lavado == 'Algodón':
            algodon = np.random.uniform(60, 100)  # Algodón alto
            poliester = np.random.uniform(0, 20)  # Un poco de poliéster
            lana = 0
            elastano = np.random.uniform(0, 5)  # Puede tener algo de elastano
            viscosa = np.random.uniform(0, 10)
            nylon = 0
            seda = 0
            fibra = np.random.uniform(0, 5)
            peso = np.random.uniform(3, 7)  # Lavados más pesados

        elif tipo_lavado == 'Mixto':
            algodon = np.random.uniform(30, 70)
            poliester = np.random.uniform(20, 50)
            lana = np.random.uniform(0, 5)
            elastano = np.random.uniform(0, 5)
            viscosa = np.random.uniform(0, 10)
            nylon = np.random.uniform(0, 5)
            seda = 0
            fibra = np.random.uniform(0, 5)
            peso = np.random.uniform(2.5, 5.5)

        elif tipo_lavado == 'Delicado':
            algodon = np.random.uniform(0, 30)
            poliester = np.random.uniform(0, 30)
            lana = np.random.uniform(10, 40)
            elastano = np.random.uniform(0, 5)
            viscosa = np.random.uniform(0, 10)
            nylon = np.random.uniform(0, 10)
            seda = np.random.uniform(5, 30)
            fibra = 0
            peso = np.random.uniform(1, 3)

        elif tipo_lavado == 'Deportivo':
            algodon = np.random.uniform(0, 30)
            poliester = np.random.uniform(30, 70)
            lana = 0
            elastano = np.random.uniform(5, 20)  # Más elastano en ropa deportiva
            viscosa = np.random.uniform(0, 5)
            nylon = np.random.uniform(5, 20)
            seda = 0
            fibra = np.random.uniform(0, 5)
            peso = np.random.uniform(2, 4)

        elif tipo_lavado == 'Sábanas/Toallas':
            algodon = np.random.uniform(70, 100)
            poliester = np.random.uniform(0, 10)
            lana = 0
            elastano = 0
            viscosa = 0
            nylon = 0
            seda = 0
            fibra = 0
            peso = np.random.uniform(4, 8)  # Pesos más altos

        # Normalizar para que los porcentajes sumen aproximadamente 100%
        total = algodon + poliester + lana + elastano + viscosa + nylon + seda + fibra
        algodon = (algodon / total) * 100
        poliester = (poliester / total) * 100
        lana = (lana / total) * 100
        elastano = (elastano / total) * 100
        viscosa = (viscosa / total) * 100
        nylon = (nylon / total) * 100
        seda = (seda / total) * 100
        fibra = (fibra / total) * 100

        # Guardar el lavado generado
        lavados.append({
            'Algodon': round(algodon, 2),
            'Poliester': round(poliester, 2),
            'Lana': round(lana, 2),
            'Elastano': round(elastano, 2),
            'Viscosa': round(viscosa, 2),
            'Nylon': round(nylon, 2),
            'Seda': round(seda, 2),
            'Fibra': round(fibra, 2),
            'Peso': round(peso, 2),
        })

    return pd.DataFrame(lavados)

# Generar 1000 lavados
lavados_df = generar_lavados_realistas(10000)

# Guardar en un archivo CSV
lavados_df.to_csv('lavados.csv', index=False)

print("Archivo 'lavados_realistas.csv' generado con éxito.")
