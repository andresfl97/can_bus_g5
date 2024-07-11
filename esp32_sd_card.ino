#include <mcp_can.h>
#include <SPI.h>
#include <ThingerESP32.h>
#include <SD.h>

#define ID_VELOCIDAD 0x4F2
#define ID_FRENADO 0x2A2
#define ID_ACELERACION 0x200
#define ID_LUCES 0x018

#define CAN0_INT 2      // Pin INT para MCP2515
#define SD_CS_PIN 4     // Pin CS para tarjeta SD

MCP_CAN CAN0(5);  // Pin CS para MCP2515

ThingerESP32 thing("user id ", "device id ", "password "); // colocar credenciales de thinger io

void setup() {
  Serial.begin(115200);
  
  // Configuración del SPI con los pines personalizados
  SPI.begin(18, 19, 23, 5);

  // Inicializa MCP2515 a 8MHz con un baudrate de 500kb/s y las máscaras y filtros deshabilitados
  if (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.println("MCP2515 Inicializado con Éxito!");
  } else {
    Serial.println("Error al Inicializar MCP2515...");
    while (1);
  }

  CAN0.setMode(MCP_NORMAL);  // Modo de operación normal
  pinMode(CAN0_INT, INPUT);  // Configuración del pin para la entrada /INT

  // Inicializa la tarjeta SD
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error al Inicializar Tarjeta SD...");
    while (1);
  }
  
  Serial.println("Tarjeta SD Inicializada con Éxito!");

  // Configuración de Thinger.io
  thing.add_wifi("HUAWEI", "1234abcd"); // wifi ssid,password 

  // Crear archivo y escribir encabezados
  File dataFile = SD.open("/log.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Tiempo, Variable, Valor");
    dataFile.close();
  } else {
    Serial.println("Error al abrir log.txt");
  }
}

void logData(const char* variable, int value) {
  File dataFile = SD.open("/log.txt", FILE_APPEND);
  if (dataFile) {
    unsigned long time = millis();  // Obtener tiempo en milisegundos desde el inicio del programa
    dataFile.print(time);
    dataFile.print(", ");
    dataFile.print(variable);
    dataFile.print(", ");
    dataFile.println(value);
    dataFile.close();
  } else {
    Serial.println("Error al abrir log.txt para escribir");
  }
}

void loop() {
  thing.handle();  // Manejar la comunicación con Thinger.io

  pson data;  // Crear un objeto pson para enviar la información a Thinger.io

  if (!digitalRead(CAN0_INT)) {  // Si el pin CAN0_INT está bajo, lee el búfer de recepción
    long unsigned int rxId;
    unsigned char len = 0;
    unsigned char rxBuf[8];

    CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Lee los datos: len = longitud de los datos, buf = byte(s) de datos

    if (rxId == ID_VELOCIDAD) {
      int velocidad = rxBuf[1]*0.5;  // el byte 1 contiene los datos de velocidad
      Serial.print("Velocidad: ");
      Serial.println(velocidad);
      data["velocidad"] = velocidad; 
      thing.set_property("kiasoul2016", data, true);  // Enviar la velocidad a Thinger.io
      logData("Velocidad", velocidad);  // Registrar datos en la tarjeta SD
    } else if (rxId == ID_FRENADO) {
      int frenado = rxBuf[7];  // el byte 7 contiene los datos de frenado
      Serial.print("Frenado: ");
      Serial.println(frenado);
      data["frenado"] = frenado;
      thing.set_property("kiasoul2016", data, true);  // Enviar los datos de frenado a Thinger.io
      //logData("Frenado", frenado);  // Registrar datos en la tarjeta SD
    } else if (rxId == ID_ACELERACION) {
      int aceleracion = rxBuf[4];  // el byte 4 contiene los datos de aceleración
      Serial.print("Aceleración: ");
      Serial.println(aceleracion);
      data["aceleracion"] = aceleracion;
      thing.set_property("kiasoul2016", data, true);  // Enviar los datos de aceleración a Thinger.io
      //logData("Aceleración", aceleracion);  // Registrar datos en la tarjeta SD
    } 
    /*
    else if (rxId == ID_LUCES) {
      int luces = rxBuf[5];  // el byte 5 contiene los datos de luces
      Serial.print("Luces: ");
      Serial.println(luces);
      data["luces"] = luces;
      thing.set_property("kiasoul2016", data, true);  // Enviar los datos de luces a Thinger.io
      //logData("Luces", luces);  // Registrar datos en la tarjeta SD
    }
  }
}
