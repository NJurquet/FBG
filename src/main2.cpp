// #include <Arduino.h>
// #include <Adafruit_MotorShield.h>
// #include <SPI.h>
// #include <Wire.h>

// // Motor shield and motors
// Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Adafruit_DCMotor *leftMotor = AFMS.getMotor(3);
// Adafruit_DCMotor *rightMotor = AFMS.getMotor(4);

// // Ultrasonic sensor pins
// const int trigPin = 11;
// const int echoPin = 12;

// // State machine states
// enum State
// {
//     INIT,
//     WAIT,
//     CHECK_OBSTACLE,
//     MOVE_FORWARD,
//     ROTATE,
//     STOP
// };
// State currentState;

// // Timer variables
// unsigned long rotateStartTime = 0;
// const unsigned long rotateDuration = 500; // 500ms
// const unsigned long startDelay = 85000;   // 85 seconds in milliseconds
// const unsigned long stopTime = 100000;    // 100 seconds in milliseconds

// // Function declarations
// void moveForward();
// void checkObstacle();
// void rotate();
// void stopMotors();
// long readUltrasonicDistance(int trigPin, int echoPin);

// void setup()
// {
//     Serial.begin(9600);
//     AFMS.begin();

//     pinMode(trigPin, OUTPUT);
//     pinMode(echoPin, INPUT);

//     // Initial state
//     currentState = INIT;
// }

// void loop()
// {
//     switch (currentState)
//     {
//     case INIT:
//         currentState = WAIT;
//         break;
//     case WAIT:
//         if (millis() > startDelay)
//         {
//             currentState = CHECK_OBSTACLE;
//         }
//         break;
//     case CHECK_OBSTACLE:
//         if (millis() < stopTime)
//             checkObstacle();
//         else
//             currentState = STOP;
//         break;
//     case MOVE_FORWARD:
//         if (millis() < stopTime)
//         {
//             moveForward();
//             currentState = CHECK_OBSTACLE;
//         }
//         else
//             currentState = STOP;
//         break;
//     case ROTATE:
//         if (millis() < stopTime)
//         {
//             rotate();
//             currentState = CHECK_OBSTACLE;
//         }
//         else
//             currentState = STOP;
//         break;
//     case STOP:
//         stopMotors();
//         break;
//     }
// }

// void moveForward()
// {
//     leftMotor->setSpeed(30);
//     rightMotor->setSpeed(30);
//     leftMotor->run(FORWARD);
//     rightMotor->run(FORWARD);
// }

// void checkObstacle()
// {
//     long distance = readUltrasonicDistance(trigPin, echoPin);
//     if (distance < 20) // If obstacle is closer than 20 cm
//     {
//         currentState = ROTATE;
//         rotateStartTime = millis(); // Record the start time of rotation
//     }
//     else
//     {
//         currentState = MOVE_FORWARD;
//     }
// }

// void rotate()
// {
//     if (millis() - rotateStartTime < rotateDuration)
//     {
//         leftMotor->setSpeed(30);
//         rightMotor->setSpeed(30);
//         leftMotor->run(BACKWARD);
//         rightMotor->run(FORWARD);
//     }
//     else
//         currentState = MOVE_FORWARD;
// }

// void stopMotors()
// {
//     leftMotor->run(RELEASE);
//     rightMotor->run(RELEASE);
// }

// long readUltrasonicDistance(int trigPin, int echoPin)
// {
//     digitalWrite(trigPin, LOW); // Clears the trigPin
//     delayMicroseconds(2);

//     // Sets the trigPin on HIGH state for 10 micro seconds
//     digitalWrite(trigPin, HIGH);
//     delayMicroseconds(10);
//     digitalWrite(trigPin, LOW);

//     long duration = pulseIn(echoPin, HIGH);
//     long distance = (duration / 2) * 0.034; // Speed of sound wave divided by 2 (go and back)
//     return distance;
// }