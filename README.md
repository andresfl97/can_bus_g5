# CAN_GATEWAY_G5

The growing number of smart cars worldwide has driven the development of new technologies for scanning and obtaining information. In this project, it was proposed to obtain data from a car's ECUs, such as speed values, acceleration, turn signals, pedals, and others, which can be identified through IDs.  For the development of our project, a CAN-Gateway prototype was implemented, allowing for the monitoring of information parameters through memory storage. To identify the IDs corresponding to each section, tests were conducted on a KIA car. Once the IDs and parameters to be captured were identified, a neural network was implemented to determine the type of driver (aggressive or defensive) based on the established parameters. Finally, a 3D model was developed that encompasses the electronic structure of the project, featuring an innovative design.

# Códigos

Los códigos que son presentados fueron probados de manera minuciosa en un ESP32 de 38 pines, tales códigos funcionan unicamente con la libreria CAN que se encuentra dentro del directorio.
Los códigos permiten testear de manera individual y grupal la comunicación SPI de los módulos micro SD y MCP2515.

# Asignación de pines


| SPI  | MOSI     | MISO     | SCLK     | CS     |
|------|----------|----------|----------|--------|
| SD_CARD | GPIO 23  | GPIO 19  | GPIO 18  | GPIO 4 |
| MCP2515 | GPIO 23  | GPIO 19  | GPIO 18  | GPIO 5 |


![ODB2](/Terminales-de-Conector-OBDII.jpg)


# Esquemático
![Esquematico](/arquitectura.png)


# DBC File example

Se presenta los archivos de DATA BASE CAN (.dbc), que logran decodificar unos cuantos ID's del vehiculo KIA SOUL 2016, estos archivos son cargados en SavvyCAN.
Una base de datos de vehiculos propietarios que pueden ser tomados como referencia se encuentra en el siguiente link, el cual descarga un pack de archivos .DBC al registrar el correo previa a su descarga.


[Enlace de descarga: ](https://www.csselectronics.com/pages/obd2-data-pack-car-dbc)

# Modelo 3D

Se presenta un diseño 3D que contiene un esp32, un regulador de voltaje, mcp2515, módulo micro sd, conector ODB 2.

![Logo del Proyecto](/MODELO%203D%20final/fig_3d.png)

# Machine learning

Se presenta códigos de:
**Red Neuronal Profunda (DNN)** es un modelo de aprendizaje automático que consiste en múltiples capas de neuronas artificiales que procesan información de manera secuencial, permitiendo aprender representaciones complejas para tareas como reconocimiento de imágenes y procesamiento de lenguaje natural. 
**Random Forest** es un algoritmo basado en la combinación de múltiples árboles de decisión generados a partir de submuestras aleatorias del conjunto de datos, proporcionando predicciones robustas y precisas para clasificación y regresión, además de manejar bien datos ruidosos y faltantes. Ambos algoritmos son útiles para análisis y predicción en sistemas de monitoreo vehicular.
