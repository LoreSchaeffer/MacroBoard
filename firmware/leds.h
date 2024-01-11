#ifndef Leds_h
#define Leds_h

#include <Adafruit_NeoPixel.h>

class Leds {
    public:
        Leds(int pin, int numPixels);

        void setup();
        void update();
    private:
        Adafruit_NeoPixel pixels;
        long firstPixelHue = 0;
};

#endif