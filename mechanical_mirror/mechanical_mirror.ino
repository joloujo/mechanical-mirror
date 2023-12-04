/*
Command list:
g (number of any length): go to step
h: set home
s (number of any length): step 
m (number, length = HEIGHT): set servo motors
l: go to limit switch
b: wait for button press, send pings
*/

#include <Servo.h>

const int HEIGHT = 5;
const int WIDTH = 5;

String data;

Servo servos[HEIGHT];
int pins[HEIGHT] = {11, 10, 9, 6, 5};

int step_pin = 3;
int dir_pin = 2;
int ls_pin = 4;
int shutter_pin = 7;

int current_step = 0;
int first_col_step = 30;
int steps_per_col = 1912;

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < HEIGHT; i++) {
    servos[i].attach(pins[i]);
  }

  pinMode(step_pin, OUTPUT);
  digitalWrite(step_pin, HIGH);
  pinMode(dir_pin, OUTPUT);
  pinMode(ls_pin, INPUT_PULLUP);
  pinMode(shutter_pin, INPUT_PULLUP);
}

String step(int n) {
  int dir;
  if (n > 0) dir = 1; else dir = -1;

  digitalWrite(dir_pin, (dir+1));
  for (int i = 0; i < abs(n); i++) {
    digitalWrite(step_pin, LOW);
    delay(1);
    digitalWrite(step_pin, HIGH);
    delay(1);
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
      for (int j = 0; j < 200; j++) {
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
  if (states.length() != HEIGHT) return "length of input does not match HEIGHT";

  for(int i = 0; i < HEIGHT; i++ ) {
    String c = states.substring(i, i+1);
    int value = c.toInt();
    servos[i].write(value * 20);
  }

  return "";
}

// String combined(String command) {
//   String response = "";

//   if (data.length() != HEIGHT + 2) {
//     response = "data must be " + String(2 + HEIGHT) + " (HEIGHT = " + String(HEIGHT) + ") characters long";
//     return response;
//   }

//   String col_str = data.substring(0, 2);
//   String row_str = data.substring(2);
//   int col = col_str.toInt();

//   goToCol(col);
//   setServos(row_str);
//   return response;
// }

String wait4Press() {
  int i = 0;
  while (digitalRead(shutter_pin) == 1) {
    if (i >= 1000) {
      Serial.println("ping");
      i = 0;
    }
    i += 1;
    delay(1);
  }

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
