#include <Servo.h>

// Create a Servo object
Servo myservo;

// Define the servo pin
const int servoPin = 6;
bool inductionState = 0;
bool prevInductionState = 1;

void setup() {
  // Start the serial communication
  Serial.begin(2000000);
  while (!Serial) {
    ; // Wait for serial port to connect. Needed for native USB port only
  }
  myservo.attach(servoPin);
  myservo.write(180);
}


void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming byte as a string
    String receivedData = Serial.readStringUntil('\n');
    // Convert the received string to an integer
    int receivedInt = receivedData.toInt();
    // Print the received integer
    // Serial.print("Received: ");
    // Serial.println(receivedInt);

    if(receivedInt)
    {
      myservo.write(85);
      delay(500);
      myservo.write(180);
    }


  }
}
