#include <Servo.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>


int pin = 6;
Servo ejector;

#define CE_PIN 7
#define CSN_PIN 8

RF24 radio(CE_PIN, CSN_PIN);

const byte address[6] = "00001";
const int buffer=20;

float avg[20];

Adafruit_BMP280 bmp;


float ref;
float time;
float previous;
float sum;
float average;
float alt;
float malt;
float pressure;
float temperature;

int cindex=0;

void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  ejector.attach(pin);
  bmp.begin(0x76);

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     
                  Adafruit_BMP280::SAMPLING_X1,     
                  Adafruit_BMP280::SAMPLING_X2,    
                  Adafruit_BMP280::FILTER_X2,      
                  Adafruit_BMP280::STANDBY_MS_1);

    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_LOW);
    radio.stopListening();
    ref=bmp.readAltitude();
    ejector.write(110);
    Serial.println("done");
    for (int i = 0;i<20;i++){
      avg[i]=bmp.readAltitude();
    };
    previous= millis();
    time=previous;
}

void loop() {
    time = millis();
    malt = bmp.readAltitude()-ref;
    pressure = bmp.readPressure();
    temperature = bmp.readTemperature();
    addReading(malt);
    find_avg();
    if (time-previous>=100){
      previous=time;
      String payload = String(time / 1000) + "," + 
                      String(malt) + "," + 
                      String(pressure) + "," + 
                      String(temperature);
      char text[payload.length() + 1];
      payload.toCharArray(text, sizeof(text));    
      radio.write(&text, sizeof(text));
    }

  
    if (malt>=alt){
      alt=bmp.readAltitude()-ref;
    }
    if ((alt-average)>15){
      ejector.write(20);
      String payload = "average: "+String(average)+",: "+String(alt);
      char text[payload.length() + 1];
      payload.toCharArray(text, sizeof(text));    
      radio.write(&text, sizeof(text));
      digitalWrite(2,HIGH);
    }

}

void addReading(float newReading) {
  avg[cindex] = newReading;  
  cindex = (cindex + 1) % buffer;  
}

void find_avg(){
  sum=0;
  for (int i=0;i<20;i++){
      sum+=avg[i];
  }
   average=sum/20;
}
