from machine import Pin, SPI
from time import sleep, sleep_ms


class MCP3008:

    def __init__(self, spi, cs, ref_voltage=3.3):
        """
        Create MCP3008 instance

        Args:
            spi: configured SPI bus
            cs:  pin to use for chip select
            ref_voltage: r
        """
        self.cs = cs
        self.cs.value(1)  # ncs on
        self._spi = spi
        self._out_buf = bytearray(3)
        self._out_buf[0] = 0x01
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    def reference_voltage(self) -> float:
        """Returns the MCP3xxx's reference voltage as a float."""
        return self._ref_voltage

    def read(self, pin, is_differential=False):
        """
        read a voltage or voltage difference using the MCP3008.

        Args:
            pin: the pin to use
            is_differential: if true, return the potential difference between two pins,


        Returns:
            voltage in range [0, 1023] where 1023 = VREF (3V3)

        """

        self.cs.value(0)  # select
        self._out_buf[1] = ((not is_differential) << 7) | (pin << 4)
        self._spi.write_readinto(self._out_buf, self._in_buf)
        self.cs.value(1)  # turn off
        return ((self._in_buf[1] & 0x03) << 8) | self._in_buf[2]


spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4), baudrate=100000)
cs = Pin(22, Pin.OUT)
cs.value(1)  # disable chip at start

chip = MCP3008(spi, cs)

while True:
    ch0 = chip.read(0)
    ch1 = chip.read(1)
    ch2 = chip.read(2)
    ch3 = chip.read(3)
    ch4 = chip.read(4)

    print('========')
    print('Channel 1: ' + str(ch0))
    print('Channel 2: ' + str(ch1))
    print('Channel 3: ' + str(ch2))
    print('Channel 4: ' + str(ch3))
    print('Channel 5: ' + str(ch4))
    print('========')

    sleep(2)

