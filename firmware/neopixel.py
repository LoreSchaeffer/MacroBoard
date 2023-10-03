from neopixel import Neopixel
import utime

numpix = 13
strip = Neopixel(numpix, 0, 7, "RGB")

red = (255, 0, 0)

delay = 0.004

utime.sleep(delay)

strip.brightness(42)
blank = (0, 0, 0)

n = 0

while True:
    print("Update" + str(n))
    n += 1

    strip.show()
    ############ Left to Right ##################
    for x in range(11):
        strip.set_pixel(x + 1, red)
        strip.show()
        utime.sleep(delay)
        strip.set_pixel(x, red)
        strip.show()
        utime.sleep(delay)
        strip.set_pixel(x + 2, red)
        strip.show()
        utime.sleep(delay)
        strip.set_pixel(x, blank)
        utime.sleep(delay)
        strip.set_pixel(x + 1, blank)
        utime.sleep(delay)
        strip.set_pixel(x + 2, blank)
        strip.show()

    ############ Left to Right ##################
    for x in reversed(range(11)):
        strip.set_pixel(x + 1, red)
        utime.sleep(delay)
        strip.show()
        strip.set_pixel(x, red)
        utime.sleep(delay)
        strip.show()
        strip.set_pixel(x + 2, red)
        utime.sleep(delay)
        strip.show()
        strip.set_pixel(x, blank)
        utime.sleep(delay)
        strip.set_pixel(x + 1, blank)
        utime.sleep(delay)
        strip.set_pixel(x + 2, blank)
        strip.show()



