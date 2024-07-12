import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import random
import time
import matplotlib.pyplot as plt

# Configurar la semilla
SEED = 1234

# Configurar la semilla en random
random.seed(SEED)

# Configurar la semilla en NumPy
np.random.seed(SEED)

# Función para leer el archivo de texto y extraer las columnas de tiempo y velocidad
def leer_archivo(file_path):
    try:
        df = pd.read_csv(file_path, delimiter='\t', decimal=',')
        if df.shape[1] < 2:
            raise ValueError("El archivo no contiene suficientes columnas.")
        tiempo = df.iloc[:, 0].values
        velocidad = df.iloc[:, 1].values
        tiempo_segundos = tiempo / 1_000_000
        velocidad_mps = velocidad / 3.6
        return tiempo_segundos, velocidad_mps
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None, None

# Función para calcular la aceleración cada 100 milisegundos (5 muestras)
def calcular_aceleracion(tiempo, velocidad, intervalo=5):
    aceleracion = []
    for i in range(0, len(velocidad) - intervalo, intervalo):
        delta_velocidad = velocidad[i + intervalo] - velocidad[i]
        delta_tiempo = tiempo[i + intervalo] - tiempo[i]
        delta_tiempo = np.round(delta_tiempo, 1)
        aceleracion.append(delta_velocidad / delta_tiempo)
    aceleracion = np.round(np.array(aceleracion), 2)
    return np.array(aceleracion)

# Función para etiquetar la agresividad en base a la aceleración y la velocidad
def etiquetar_agresividad(aceleracion, velocidad, intervalo=5):
    etiquetas = []
    for i in range(0, len(velocidad) - intervalo, intervalo):
        acc_brusca = False
        vel_excesiva = False
        
        if i < len(aceleracion) and (aceleracion[i] > 3 or aceleracion[i] < -3):
            acc_brusca = True
        
        vel_sub_inter = velocidad[i:i+intervalo]
        if np.sum(vel_sub_inter > 50 / 3.6) >= 1:
            vel_excesiva = True
        
        if acc_brusca or vel_excesiva:
            etiquetas.append(1)
        else:
            etiquetas.append(0)
    
    return np.array(etiquetas)

# Leer y procesar datos
file_path = 'prueba4_1.txt'
tiempo, velocidad = leer_archivo(file_path)

if tiempo is not None and velocidad is not None:
    # Calcular la aceleración cada 100 milisegundos
    aceleracion = calcular_aceleracion(tiempo, velocidad)
    
    # Etiquetar la agresividad del conductor
    etiquetas = etiquetar_agresividad(aceleracion, velocidad)
    
    # Crear la matriz de entrada combinando velocidad y aceleración
    X = np.column_stack((velocidad[:-5:5], aceleracion))
    y = etiquetas
    
    # Normalizar los datos
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=SEED)
    
    # Crear el modelo de Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=SEED)
    
    # Capturar el tiempo antes de entrenar
    start_time = time.time()

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Capturar el tiempo después de entrenar
    end_time = time.time()

    # Calcular el tiempo total de entrenamiento
    training_time = end_time - start_time
    print(f"Tiempo total de entrenamiento: {training_time:.2f} segundos")

    # Evaluar el modelo
    accuracy = model.score(X_test, y_test)
    print(f"Precisión del modelo: {accuracy * 100:.2f}%")
    
    # Leer nuevos datos desde un archivo de texto usando pandas
    tiempo_nuevos, velocidad_nuevos = leer_archivo('prueba2_1.txt')
    aceleracion_nuevos = calcular_aceleracion(tiempo_nuevos, velocidad_nuevos)
    nuevos_datos = np.column_stack((velocidad_nuevos[:-5:5], aceleracion_nuevos))
    
    # Normalizar los nuevos datos usando el mismo escalador
    nuevos_datos_scaled = scaler.transform(nuevos_datos)
    
    # Hacer predicciones con los nuevos datos
    predicciones = model.predict(nuevos_datos_scaled)
    
    # Contar cuántos términos de clasificación son 0 y cuántos son 1
    num_pasivos = np.sum(predicciones == 0)
    num_agresivos = np.sum(predicciones == 1)
    
    print(f"Número de conducciones pasivas (0): {num_pasivos}")
    print(f"Número de conducciones agresivas (1): {num_agresivos}")
    porcentaje_agresivo = num_agresivos * 100 / len(predicciones)
    porcentaje_agresivo = np.round(porcentaje_agresivo)
    if porcentaje_agresivo >= 10:
        print(f"El porcentaje de agresividad fue de: {porcentaje_agresivo} % \nConductor sobrepasa límite ---> Conductor agresivo")
    else:
        print(f"El porcentaje de agresividad fue de: {porcentaje_agresivo} % \nConductor no sobrepasa límite ---> Conductor pasivo")
    
    # Graficar la aceleración en función del tiempo (cada 100 ms)
    tiempo_pred = np.arange(0, len(aceleracion_nuevos) * 0.1, 0.1)  # Intervalos de 100 ms
    plt.figure(figsize=(10, 5))
    plt.plot(tiempo_pred, aceleracion_nuevos, marker='o')
    plt.title('Aceleración en función del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (m/s^2)')
    plt.grid(True)
    plt.show()


    # Graficar la velocidad en función del tiempo en km/h
    velocidad_nuevos_kmh = velocidad_nuevos * 3.6  # Convertir de m/s a km/h
    plt.figure(figsize=(10, 5))
    plt.plot(tiempo_nuevos, velocidad_nuevos_kmh, marker='o')
    plt.title('Velocidad en función del tiempo')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (km/h)')
    plt.grid(True)
    plt.show()


else:
    print("No se pudieron leer los datos del archivo.")