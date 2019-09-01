#include <SPI.h>
#include <Ethernet.h>

int analogPinA0 = A0;

int val = 0;  // variable to store the value read
int con = 0;// connection status


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0x90, 0xA2, 0xDA, 0x00, 0xFE, 0xAC
};
IPAddress ip(192, 168, 1, 21);

// Enter the IP address of the server you're connecting to:
IPAddress server(192, 168, 1, 2);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 23 is default for telnet;
// if you're using Processing's ChatServer, use port 10002):
EthernetClient client;

void setup() {

  pinMode(7,OUTPUT);

  // You can use Ethernet.init(pin) to configure the CS pin
  //Ethernet.init(10);  // Most Arduino shields
  //Ethernet.init(5);   // MKR ETH shield
  //Ethernet.init(0);   // Teensy 2.0
  //Ethernet.init(20);  // Teensy++ 2.0
  //Ethernet.init(15);  // ESP8266 with Adafruit Featherwing Ethernet
  //Ethernet.init(33);  // ESP32 with Adafruit Featherwing Ethernet

  // start the Ethernet connection:
  Ethernet.begin(mac, ip);

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1); // do nothing, no point running without Ethernet hardware
    }
  }
//  while (Ethernet.linkStatus() == LinkOFF) {
//    Serial.println("Ethernet cable is not connected.");
//    delay(500);
//  }
  if (Ethernet.linkStatus() == Unknown) {
//    Serial.println("Link status unknown. Link status detection is only available with W5200 and W5500.");
  }
  else if (Ethernet.linkStatus() == LinkON) {
    Serial.println("Link status: On");
  }
  else if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Link status: Off");
  }
  // give the Ethernet shield a second to initialize:
  delay(1000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, 65432)) {
    Serial.println("connected");
    digitalWrite(7, HIGH);
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}

void loop() {

  val = analogRead(analogPinA0);  // read the input pin
//  Serial.println(val);          // debug value
  if (client.connected()) {
    client.println(val);
  }
  Serial.println(val);

  if (!client.connected()) {
    digitalWrite(7, LOW);
    if (client.connect(server, 65432)) {
        Serial.println("connected");
        digitalWrite(7, HIGH);
        con = 0;
    } else {
      if(con==0){
        Serial.println("Waiting connection...");
        con = 1;
      }
      delay(1);
    }
  }
  delay(1000);
}
