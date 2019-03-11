//NFC Card b5dc4543

/******************** INCLUDES ********************/
#include <ESP8266WiFi.h>          // JSON communication
#include <ESP8266HTTPClient.h>    //
#include <ArduinoJson.h>          //
#include <SPI.h>                  // RFID authorization
#include <MFRC522.h>              //

/******************** DEFINES ********************/
#define RC522_SS_PIN D8           // RFID authorization

MFRC522 mfrc522(RC522_SS_PIN); // Instance of the class

// WiFi Parameters
const char* ssid = "b9718e-2.4G";
const char* password = "";

String rfid_tag = "";

/******************** FUNCTIONS DECLARATION ********************/

String read_rfid_tag() {
  String rfid_tag="";  
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : "");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    rfid_tag = rfid_tag + String(mfrc522.uid.uidByte[i], HEX);
  }

  /*****************/
  rfid_tag = "b5dc4543";         // TESTING
  /******************/

  Serial.println(rfid_tag); 
  mfrc522.PICC_HaltA();
  return rfid_tag;
}


int get_json_data(String rfid_tag) {
  HTTPClient http;  //Object of class HTTPClient
  // Check WiFi Status
  if (WiFi.status() == WL_CONNECTED) {

    char* api_address = "http://jsonplaceholder.typicode.com/users/5";
    
    StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer 
    http.begin(api_address);      //Specify request destination
    http.addHeader("Content-Type", "application/json");  //Specify content-type header
    
    int httpCode = http.GET();   //Send the request
    
    JsonObject& response = JSONbuffer.parseObject(http.getString());

      // Parameters
      int durations[4] = { response["durations"] }; // durations of 4 pumps

      // Output to serial monitor
      Serial.print("Name:");
      Serial.println(durations[0]);
    http.end();   //Close connection
    return durations[4];
  }

}

int make_a_drink(int durations[4]) {
  Serial.println(durations[0]);
  Serial.println(durations[1]);
  Serial.println(durations[2]);
  Serial.println(durations[3]);
  return 0;
}

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  WiFi.mode(WIFI_STA);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected");
  
  SPI.begin();       // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522
  Serial.println("RFID reading UID");

}

void loop() {
  if ( mfrc522.PICC_IsNewCardPresent()) {
    if ( mfrc522.PICC_ReadCardSerial()) {
      String rfid_tag = read_rfid_tag();  
      int durations[4] = { get_json_data(rfid_tag) };
      make_a_drink(durations);
    }
  }

}
