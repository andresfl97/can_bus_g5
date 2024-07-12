#include <mcp_can.h>
#include <SPI.h>
#include <SD.h>

long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];
char msgString[128];  // Array to store serial string

#define CAN0_INT 2      // Set INT to pin 2
#define SD_CS_PIN 4     // Set CS pin for SD card

MCP_CAN CAN0(5);  // Set CS to pin 5

void setup() {
  Serial.begin(115200);
  
  // Configura el SPI con los pines personalizados
  SPI.begin(18, 19, 23, 5);

  // Inicializa MCP2515 corriendo a 8MHz con un baudrate de 500kb/s y las máscaras y filtros deshabilitados.
  if (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
    Serial.println("MCP2515 Initialized Successfully!");
  } else {
    Serial.println("Error Initializing MCP2515...");
  }

  CAN0.setMode(MCP_NORMAL);  // Configura el modo de operación a normal para que el MCP2515 envíe acks a los datos recibidos.

  pinMode(CAN0_INT, INPUT);  // Configura el pin para la entrada /INT

  // Inicializa la tarjeta SD
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error Initializing SD card...");
    while (1);
  }
  
  Serial.println("SD card Initialized Successfully!");

  Serial.println("MCP2515 Library Receive Example...");
}

void loop() {
  if (!digitalRead(CAN0_INT)) {  // Si el pin CAN0_INT está bajo, lee el búfer de recepción
    CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Lee los datos: len = longitud de los datos, buf = byte(s) de datos
    
    if ((rxId & 0x80000000) == 0x80000000) {  // Determina si el ID es estándar (11 bits) o extendido (29 bits)
      sprintf(msgString, "Extended ID: 0x%.8lX  DLC: %1d  Data:", (rxId & 0x1FFFFFFF), len);
    } else {
      sprintf(msgString, "Standard ID: 0x%.3lX       DLC: %1d  Data:", rxId, len);
    }
  
    Serial.print(msgString);
  
    if ((rxId & 0x40000000) == 0x40000000) {  // Determina si el mensaje es un cuadro de solicitud remota
      sprintf(msgString, " REMOTE REQUEST FRAME");
      Serial.print(msgString);
    } else {
      for (byte i = 0; i < len; i++) {
        sprintf(msgString, " 0x%.2X", rxBuf[i]);
        Serial.print(msgString);
      }
    }
        
    Serial.println();
  }
}
