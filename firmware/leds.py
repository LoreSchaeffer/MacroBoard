from neopixel import Neopixel
import uasyncio as asyncio

class Leds:
    def __init__(self, numpix, pin, brightness=100):
        self.numpix = numpix
        self.neopixel = Neopixel(numpix, 0, pin, "RGB")
        self.neopixel.brightness(brightness)
        self.firstPixelHue = 0

    def update(self):
        for i in range(self.numpix):
            pixelHue = self.firstPixelHue + (i * 65536 // self.numpix)
            self.neopixel.set_pixel(i, self.neopixel.colorHSV(pixelHue, 255, 255))
        self.neopixel.show()
        self.firstPixelHue += 256
        if self.firstPixelHue >= 5 * 65536:
            self.firstPixelHue = 0

    