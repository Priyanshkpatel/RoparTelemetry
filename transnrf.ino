#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 40;
const int LOADCELL_SCK_PIN = 41;

HX711 scale;


#define CE_PIN 39
#define CSN_PIN 5
#define SCK_PIN 38
#define MISO_PIN 37
#define MOSI_PIN 6

RF24 radio(CE_PIN, CSN_PIN);

const byte address[6] = "00001";

long start;
long current;

void setup() {
    Serial.begin(115200);
    SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, CSN_PIN);  // Define SPI pins
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_LOW);
    radio.stopListening();
    scale.set_scale(-14.6666666667);
    scale.tare(); 
    start = millis();
}

void loop() {
    current = millis()-start;
    String payload = "M,"+String(current)+","+String(scale.get_units());
    char text[payload.length() + 1];
    payload.toCharArray(text, sizeof(text));    
    radio.write(&text, sizeof(text));
    Serial.println("Sent");
    delay(100);
}
