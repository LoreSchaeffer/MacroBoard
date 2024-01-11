#ifndef ADC_h
#define ADC_h

#include <Adafruit_MCP3008.h>
#include <SimpleKalmanFilter.h>

class ADC {
public:
  ADC(uint8_t sck, uint8_t mosi, uint8_t miso, uint8_t cs, boolean c5, boolean c6, boolean c7);

  void setup();
  void update();

private:
  float toPercentage(float value);

  Adafruit_MCP3008 adc;
  uint8_t sck;
  uint8_t mosi;
  uint8_t miso;
  uint8_t cs;
  float** values;
  float* lastValues;
  boolean c5;
  boolean c6;
  boolean c7;
  SimpleKalmanFilter* filters;
};

#endif