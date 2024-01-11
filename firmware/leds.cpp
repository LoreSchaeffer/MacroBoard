#include <Adafruit_NeoPixel.h>
#include "leds.h"

Leds::Leds(int pin, int numPixels) : pixels(numPixels, pin, NEO_RGB + NEO_KHZ800) {
}

void Leds::setup() {
    pixels.begin();
}

void Leds::update() {
    if (firstPixelHue < 5 * 65536) {
        for (int i = 0; i < 13; i++) {
            int pixelHue = firstPixelHue + (i * 65536L / pixels.numPixels());
            pixels.setPixelColor(i, pixels.gamma32(pixels.ColorHSV(pixelHue)));
        }

        pixels.show();
        firstPixelHue += 256;
    } else {
        firstPixelHue = 0;
    }
}