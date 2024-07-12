import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
import random
import tensorflow 
import matplotlib.pyplot as plt
import time 

# Configurar la semilla
SEED = 1234

# Configurar la semilla en random
random.seed(SEED)

# Configurar la semilla en NumPy
np.random.seed(SEED)

# Configurar la semilla en TensorFlow
tensorflow.random.set_seed(SEED)

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
        delta_tiempo=np.round(delta_tiempo,1)
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
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
    
    '''
    # Crear el modelo de la red neuronal
    model = Sequential()
    model.add(Dense(10, input_dim=2, activation='relu'))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    '''
    # Definir la capa de entrada
    input_signal = Input(shape=(2,))

    # Añadir las capas densas
    hidden1 = Dense(5, activation='relu')(input_signal)
    hidden2 = Dense(2, activation='relu')(hidden1)
    output = Dense(1, activation='sigmoid')(hidden2)

    # Crear el modelo
    model = Model(inputs=input_signal, outputs=output)


    # Compilar el modelo
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    # Callback EarlyStopping
    early_stopping = EarlyStopping(monitor='loss', patience=2, restore_best_weights=True)
    
    # Capturar el tiempo antes de entrenar
    start_time = time.time()

    # Entrenar el modelo
    history=model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test), callbacks=[early_stopping])

    # Capturar el tiempo después de entrenar
    end_time = time.time()

    # Calcular el tiempo total de entrenamiento
    training_time = end_time - start_time
    print(f"Tiempo total de entrenamiento: {training_time:.2f} segundos")



    # Evaluar el modelo
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Precisión del modelo: {accuracy * 100:.2f}%")
    
    # Graficar la precisión y la pérdida del entrenamiento
    plt.figure(figsize=(12, 4))
    
    # Gráfica de pérdida
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], 'bo', label='Pérdida de entrenamiento')
    plt.plot(history.history['val_loss'], 'b', label='Pérdida de validación')
    plt.title('Pérdida durante el entrenamiento y la validación')
    plt.xlabel('Épocas')
    plt.ylabel('Pérdida')
    plt.legend()
    
    # Gráfica de precisión
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], 'ro', label='Precisión de entrenamiento')
    plt.plot(history.history['val_accuracy'], 'r', label='Precisión de validación')
    plt.title('Precisión durante el entrenamiento y la validación')
    plt.xlabel('Épocas')
    plt.ylabel('Precisión')
    plt.legend()
    
    plt.show()
    


    # Leer nuevos datos desde un archivo de texto usando pandas
    nuevos_datos_df = pd.read_csv('prueba2_1.txt', delimiter='\t', decimal=',')
    tiempo_nuevos, velocidad_nuevos = leer_archivo('prueba2_1.txt')
    aceleracion_nuevos = calcular_aceleracion(tiempo_nuevos, velocidad_nuevos)
    nuevos_datos = np.column_stack((velocidad_nuevos[:-5:5], aceleracion_nuevos))
    
    # Normalizar los nuevos datos usando el mismo escalador
    nuevos_datos_scaled = scaler.transform(nuevos_datos)
    
    # Hacer predicciones con los nuevos datos
    predicciones = model.predict(nuevos_datos_scaled)
    
    # Convertir las probabilidades en etiquetas de clase (0 o 1)
    clasificacion = (predicciones > 0.5).astype(int)
    
    # Contar cuántos términos de clasificación son 0 y cuántos son 1
    num_pasivos = np.sum(clasificacion == 0)
    num_agresivos = np.sum(clasificacion == 1)
    
    print(f"Número de conducciones pasivsas (0): {num_pasivos}")
    print(f"Número de conducciones agresivas (1): {num_agresivos}")
    porcentaje_agresivo=num_agresivos*100/len(clasificacion)
    porcentaje_agresivo=np.round(porcentaje_agresivo)
    if porcentaje_agresivo >= 10:
        print(f"El procentaje de agresividad fue de: {porcentaje_agresivo} % \nConductor sobrepasa límite --->  Conductor agresivo")
    else:
        print(f"El procentaje de agresividad fue de: {porcentaje_agresivo} % \nConductor no sobrepasa límite --->  Conductor pasivo")

    # Graficar la aceleración en función del tiempo (cada 100 ms)
    tiempo_pred = np.arange(0, len(aceleracion_nuevos)*0.1 , 0.1)  # Intervalos de 100 ms
    plt.figure(figsize=(10, 5))
    plt.plot(tiempo_pred, aceleracion_nuevos)
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
