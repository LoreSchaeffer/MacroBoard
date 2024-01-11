#include "adc.h"

#include <Adafruit_MCP3008.h>

#define WINDOW_SIZE 75

ADC::ADC(uint8_t sck, uint8_t mosi, uint8_t miso, uint8_t cs, boolean c5,
         boolean c6, boolean c7)
    : adc(), sck(sck), mosi(mosi), miso(miso), cs(cs), c5(c5), c6(c6), c7(c7) {}

void ADC::setup() {
  adc.begin(sck, mosi, miso, cs);

  values = new float *[8];
  lastValues = new float[8];

  for (int i = 0; i < 8; i++) {
    values[i] = new float[WINDOW_SIZE];
    for (int j = 0; j < WINDOW_SIZE; j++) {
      values[i][j] = (i <= 4 || c5 && i == 5 || c6 && i == 6 || c7 && i == 7)
                         ? (float)adc.readADC(i)
                         : 0;
    }

    lastValues[i] = values[i][0];
  }
}

void ADC::update() {
  for (int c = 0; c < 8; c++) {
    if (!c5 && c == 5)
      continue;
    if (!c6 && c == 6)
      continue;
    if (!c7 && c == 7)
      continue;

    float oldValue = values[c][WINDOW_SIZE - 1];
    float newValue = adc.readADC(c);

    for (int i = WINDOW_SIZE - 1; i > 0; i--) {
      values[c][i] = values[c][i - 1];
    }

    values[c][0] = newValue;

    float valuePercentage = toPercentage(values[c][0]);
    float oldValuePercentage = toPercentage(oldValue);

    if (abs(lastValues[c] - valuePercentage) >= 0.01) {
      Serial.print("Channel ");
      Serial.print(c);
      Serial.print(": ");
      Serial.print(String(oldValuePercentage, 2));
      Serial.print(" -> ");
      Serial.println(String(valuePercentage, 2));

      lastValues[c] = valuePercentage;
    }
  }
}

float ADC::toPercentage(float value) { return value / 1023; }