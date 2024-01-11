#include "kpd.h"
#include "leds.h"
#include "adc.h"
#include "pico/stdlib.h"
#include <Keypad.h>

#define SCK_PIN 2
#define MOSI_PIN 3
#define MISO_PIN 4
#define CS_PIN 22

#define LED_PIN 6
#define NUM_PIXELS 13

const byte KP_ROWS = 4;
const byte KP_COLS = 4;
const char KP_KEYMAP[KP_ROWS][KP_COLS] = {{'0', '1', '2', '3'},
                                          {'4', '5', '6', '7'},
                                          {'8', '9', 'A', 'B'},
                                          {'C', 'D', 'E', 'F'}};
byte KP_ROW_PINS[KP_ROWS] = {11, 10, 9, 8};
byte KP_COL_PINS[KP_COLS] = {15, 14, 13, 12};

Leds leds(LED_PIN, NUM_PIXELS);
KPD keypad(KP_ROWS, KP_COLS, makeKeymap(KP_KEYMAP), KP_ROW_PINS, KP_COL_PINS, 25);
ADC adc(SCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN, false, false, false);

void setup() {
  Serial.begin(11520);
  keypad.setup();
  adc.setup();
  leds.setup();
}

void setup1() {}

void loop() {
  keypadRoutine();
  sliderRoutine();
  ledRoutine();
}

void loop1() {}

long ledRoutineDelay = 20;
long ledRoutineLast = 0;
void ledRoutine() {
  if (ledRoutineLast + ledRoutineDelay < millis()) {
    ledRoutineLast = millis();
    leds.update();
  }
}

long keypadRoutineDelay = 1;
long keypadRoutineLast = 0;
void keypadRoutine() {
  if (keypadRoutineLast + keypadRoutineDelay < millis()) {
    keypadRoutineLast = millis();
    keypad.update();
  }
}

long sliderRoutineDelay = 10;
long sliderRoutineLast = 0;
void sliderRoutine() {
  if (sliderRoutineLast + sliderRoutineDelay < millis()) {
    sliderRoutineLast = millis();
    adc.update();
  }
}