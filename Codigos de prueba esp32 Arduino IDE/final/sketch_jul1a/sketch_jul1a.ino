 #include <mcp_can.h>
#include <SPI.h>
#include <ThingerESP32.h>
#include <SD.h>

// Definir los IDs de interés
#define ID_VELOCIDAD 0x4F2
#define ID_FRENADO 0x2A2
#define ID_ACELERACION 0x200
#define ID_LUCES 0x018

#define CAN0_INT 2      // Pin INT para MCP2515
#define SD_CS_PIN 4     // Pin CS para tarjeta SD

MCP_CAN CAN0(5);  // Pin CS para MCP2515

ThingerESP32 thing("andresf5597", "esp32", "123456");

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
  thing.add_wifi("HUAWEI", "1234abcd");

  // Ejemplo de control de pin digital
  //thing["GPIO_16"] << digitalPin(16);

  // Ejemplo de salida de recurso
  //thing["millis"] >> outputValue(millis());
}

void loop() {
  thing.handle();  // Manejar la comunicación con Thinger.io
  pson data; // se crea un objeto para enviar la información  al dashboad

/*
// ejemplo para uso de tuhiger.io, enviar datos a la nube
    data["velocidad"]=12;
    data["frenado"]=13.40;
    data["aceleracion"]=25.056;
    data["luces"]=50.40;
    thing.set_property("kiasoul2016", data, true); // nombre del identificador del dashobard, se envian todos los datos usados 
*/

  if (!digitalRead(CAN0_INT)) {  // Si el pin CAN0_INT está bajo, lee el búfer de recepción
    long unsigned int rxId;
    unsigned char len = 0;
    unsigned char rxBuf[8];

    CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Lee los datos: len = longitud de los datos, buf = byte(s) de datos

    if (rxId == ID_VELOCIDAD) {
      int velocidad = rxBuf[1];  // el byte 1 contiene los datos de velocidad del kiasoul2016
      Serial.print("Velocidad: ");
      Serial.println(velocidad);

      // Crear un objeto pson y enviar los datos
      //pson data; // basta con crearlo antes de los condicionales 
      data["velocidad"] = velocidad; 
      thing.set_property("kiasoul2016", data, true); //se envia la velocidad 
    } else if (rxId == ID_FRENADO) {
      int frenado = rxBuf[7];  // el byte 7 contiene los datos de que tan presionado esta el pedal de freno  
      Serial.print("Frenado: ");
      Serial.println(frenado);

      // Crear un objeto pson y enviar los datos
      //pson data;
      data["frenado"] = frenado;
      thing.set_property("kiasoul2016", data, true); //se envia el frenado
    } else if (rxId == ID_ACELERACION) {
      int aceleracion = rxBuf[4];  // El byte 4 contiene que tan presionado esta el pedal de aceleración
      Serial.print("Aceleración: ");
      Serial.println(aceleracion);

      // Crear un objeto pson y enviar los datos
      //pson data;
      data["aceleracion"] = aceleracion;
      thing.set_property("kiasoul2016", data, true); // se envia la aceleracion 
    } else if (rxId == ID_LUCES) {
      int luces = rxBuf[5];  // el byte 5 contiene la información del uso de las direccionales y parqueo
      Serial.print("Luces: ");
      Serial.println(luces);

      // Crear un objeto pson y enviar los datos
      //pson data;
      data["luces"] = luces;
      thing.set_property("kiasoul2016", data, true);
    }
  }
}