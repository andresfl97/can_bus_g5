#define THINGER_SERIAL_DEBUG

#include <ThingerESP32.h>
#include "arduino_secrets.h"




ThingerESP32 thing("andresf5597", "esp32", "123456");

void setup() {
  // open serial for debugging
  Serial.begin(115200);

  pinMode(16, OUTPUT);

  thing.add_wifi("HUAWEI", "1234abcd");

  // digital pin control example (i.e. turning on/off a light, a relay, configuring a parameter, etc)
  thing["GPIO_16"] << digitalPin(16);

  // resource output example (i.e. reading a sensor value)
  thing["millis"] >> outputValue(millis());

  // more details at http://docs.thinger.io/arduino/
}

                    /*set property value*/
void loop(){
thing.handle();



    //create a pson with new values
    pson data;
    data["longitude"]=-4.056;
    data["latitude"]=41.40;

    //sending new values to platform
    thing.set_property("location", data, true);
  
}