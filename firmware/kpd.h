#ifndef KPD_h
#define KPD_h

#include <Keypad.h>

class KPD {
public:
  KPD(byte numRows, byte numCols, char *userKeymap, byte *row, byte *col,
      unsigned long debounceDelay);

  void setup();
  void update();

private:
  Keypad keypad;
  unsigned long debounceDelay;
};

#endif