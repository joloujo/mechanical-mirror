/*
Command list:
g (number of any length): go to step
h: set home
s (number of any length): step 
m (number, length = HEIGHT): set servo motors
l: go to limit switch
b: wait for button press, send pings
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

const int HEIGHT = 15;
const int WIDTH = 13;

String data;

int step_pin = 3;
int dir_pin = 2;
int ls_pin = 4;
int shutter_pin = 7;

int current_step = 0;
int first_col_step = 0;
int steps_per_col = 663;

int stepDelay = 2;

Adafruit_PWMServoDriver servo_driver = Adafruit_PWMServoDriver(0x41);
uint8_t servonum = 15;

#define SERVOMIN 150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 600 // This is the 'maximum' pulse length count (out of 4096)

void setup() {
  Serial.begin(115200);

  servo_driver.begin();
  servo_driver.setOscillatorFrequency(25000000);
  servo_driver.setPWMFreq(50);  // Analog servos run at ~50 Hz updates

  pinMode(step_pin, OUTPUT);
  digitalWrite(step_pin, HIGH);

  pinMode(dir_pin, OUTPUT);

  pinMode(ls_pin, INPUT_PULLUP);

  pinMode(shutter_pin, INPUT_PULLUP);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  
}

String step(int n) {
  int dir;
  if (n > 0) dir = 1; else dir = -1;

  digitalWrite(dir_pin, (dir+1));
  for (int i = 0; i < abs(n); i++) {
    digitalWrite(step_pin, LOW);
    delay(stepDelay);
    digitalWrite(step_pin, HIGH);
    delay(stepDelay);
    current_step += dir;
  }

  return "";
}

String goToCol(String col_str) {
  float target_col = col_str.toFloat();
  int target_step = steps_per_col * target_col + first_col_step;
  int step_num = target_step - current_step;

  step(step_num);

  return "";
}

String setHome() {
  current_step = 0;
  return "";
}

String limitSwitch(int max) {
  int ls_value;
  for (int i = 0; i < max; i++) {
    ls_value = digitalRead(ls_pin);
    if (ls_value == 0) {
      for (int j = 0; j < 50; j++) {
        step(1);
      }
      setHome();
      return "";
    }
    step(-1);
  }
  return "Warning: didn't reach limit switch";
}

String setServos(String states) {
  if (states.length() != servonum) return "length of input does not match number of servos";

  for(int servo = 0; servo < servonum; servo++ ) {
    String c = states.substring(servo, servo+1);
    int value = c.toInt();

    uint16_t command_value = map(value, 0, 9, SERVOMIN, SERVOMAX);

    servo_driver.setPWM(servo, 0, command_value);
  }

  delay(500);

  return "";
}

String wait4Press() {

  digitalWrite(LED_BUILTIN, HIGH);

  int i = 0;
  while (digitalRead(shutter_pin) == 1) {
    if (i >= 1000) {
      Serial.println("ping");
      i = 0;
    }
    i += 1;
    delay(1);
  }
  while (digitalRead(shutter_pin) == 0) {
    if (i >= 1000) {
      Serial.println("ping");
      i = 0;
    }
    i += 1;
    delay(1);
  }

  digitalWrite(LED_BUILTIN, LOW);

  return "";
}

void loop() {
  if (Serial.available() == 0) return;
  data = Serial.readStringUntil('\n');
  String response = "";

  char command_id = data.charAt(0);
  String command = data.substring(1);
  switch (command_id) {
    case 'g': {
      response = goToCol(command);
      break;
    }
    case 'h': {
      response = setHome();
      break;
    }
    case 's': {
      int step_num = command.toInt();
      response = step(step_num);
      break;
    }
    case 'm': {
      response = setServos(command);
      break;
    }
    case 'l': {
      int max;
      if (command == "") {
        max = 1000; // default to 5 revolutions max
      }
      else {
        max = command.toInt();
      }
      response = limitSwitch(max);
      break;
    }
    case 'b': {
      response = wait4Press();
      break;
    }
    default: {
      response = "Command not recognized";
      break;
    }
  }

  Serial.println(response);
}
