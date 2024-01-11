#include "kpd.h"
#include <Keypad.h>

unsigned long debounceDelay;

KPD::KPD(byte numRows, byte numCols, char *userKeymap, byte *row, byte *col, unsigned long debounceDelay)
    : keypad(userKeymap, row, col, numRows, numCols),
      debounceDelay(debounceDelay) {}

void KPD::setup() {}

void KPD::update() {
  static unsigned long last_press_time = 0;

  if (keypad.getKeys()) {
    for (int i = 0; i < LIST_MAX; i++) {
      unsigned long current_time = millis();
      if (current_time - last_press_time > debounceDelay) {
        String msg;

        if (keypad.key[i].stateChanged) {
          switch (keypad.key[i].kstate) {
          case PRESSED:
            msg = " PRESSED ";
            break;
          case HOLD:
            msg = " HOLD ";
            break;
          case RELEASED:
            msg = " RELEASED ";
            break;
          case IDLE:
            msg = " IDLE ";
            break;
          }

          Serial.print("Key ");
          Serial.print(keypad.key[i].kchar);
          Serial.println(msg);

          last_press_time = current_time;
        }
      }
    }
  }
}