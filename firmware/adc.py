from machine import Pin, SPI

class KalmanFilter:
    def __init__(self, initial_estimate, process_variance, measurement_variance):
        self.estimate = initial_estimate
        self.estimate_error = process_variance

        self.process_variance = process_variance
        self.measurement_variance = measurement_variance

    def update(self, measurement):
        prediction = self.estimate
        prediction_error = self.estimate_error + self.process_variance

        kalman_gain = prediction_error / (prediction_error + self.measurement_variance)
        self.estimate = prediction + kalman_gain * (measurement - prediction)
        self.estimate_error = (1 - kalman_gain) * prediction_error

        return self.estimate


class MCP3008:
    def __init__(self, spi, cs, ref_voltage=3.3):
        self.cs = cs
        self.cs.value(1)
        self._spi = spi
        self._out_buf = bytearray(3)
        self._out_buf[0] = 0x01
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    def read(self, pin, is_differential=False):
        self.cs.value(0)
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        self._spi.write_readinto(self._out_buf, self._in_buf)
        self.cs.value(1)
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]


class ADC:
    def __init__(self, sck, mosi, miso, cs, baudrate=100000):
        cs = Pin(cs, Pin.OUT)
        cs.value(1)
        self.adc = MCP3008(SPI(0, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso), baudrate=baudrate), cs)

    
    def read(self, channel):
        return self.adc.read(channel)

