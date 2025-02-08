#include <Servo.h>

#include <RF24.h>
#include <RF24_config.h>
#include <nRF24L01.h>
#include <printf.h>

#define CE_PIN 14
#define CSN_PIN 9
#define SCK_PIN 13
#define MISO_PIN 12
#define MOSI_PIN 10


RF24 radio(CE_PIN, CSN_PIN);

const byte address[6] = "00001";

void setup() {
    Serial.begin(115200);
    SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, CSN_PIN);  // Define SPI pins
    radio.begin();
    radio.openReadingPipe(0, address);
    radio.setPALevel(RF24_PA_LOW);
    radio.startListening();
}

void loop() {
    if (radio.available()) {
        char receivedText[32] = "";
        radio.read(&receivedText, sizeof(receivedText));
        Serial.println(receivedText);
    }
}
