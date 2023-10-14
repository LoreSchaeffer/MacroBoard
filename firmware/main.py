import machine
from picozero import pico_led as led
from picozero import pico_temp_sensor as temp
import _thread
import uasyncio as asyncio
from config import Config
from leds import Leds
from keypad import Keypad
from adc import ADC, KalmanFilter
import communication.protocol

defConfig = {
    'mode': {
        'wifi': False,
        'bluetooth': False
    },
    'wifi': {
        'ssid': '',
        'password': ''
    },
    'bluetooth': {
        'device_id': ''
    },
    'frequency': 240000000
}
config = Config('config.json', defConfig)

leds = Leds(13, 6)

keymap = [
    ['F9', 'F10', 'F11', 'F12'],
    ['F5', 'F6', 'F7', 'F8'],
    ['F1', 'F2', 'F3', 'F4'],
    ['SL', '', '', '']
]
keypad = Keypad([11, 10, 9, 8], [15, 14, 13, 12], keymap)

adc = ADC(2, 3, 4, 22)
adcChannels = 5
channels = {}


async def ledRoutine():
    while True:
        leds.update()
        await asyncio.sleep_ms(20)


async def keypadRoutine():
    while True:
        key = keypad.scanKeys()
        if key != None:
            print('You have pressed:', key)
        await asyncio.sleep_ms(1)


async def sliderRoutine():
    while True:
        for channel in range(adcChannels):
            rawValue = adc.read(channel)
            filteredValue = round(channels[channel][0].update(rawValue))
            
            if filteredValue != channels[channel][1]:
                channels[channel][1] = filteredValue
                print(f'Channel {channel}: {filteredValue}')
        await asyncio.sleep_ms(10)


def core1():
    print("Hello from core 1")


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(ledRoutine())
    loop.create_task(keypadRoutine())
    loop.create_task(sliderRoutine())
    loop.run_forever()


def init():
    print('Initializing...')
    if config.exists():
        config.load()
    else:
        config.save()

    machine.freq(config.get('frequency'))
    print(f'Core frequency: {machine.freq() // 1000000} MHz')

    for channel in range(adcChannels):
        currentValue = adc.read(channel)
        channels[channel] = [
            KalmanFilter(currentValue, 0.002, 1.0),
            currentValue
        ]

    print('Initialization completed')

    if (config.get('mode.wifi')):
        print('Starting in WiFi mode')
    elif (config.get('mode.bluetooth')):
        print('Starting in Bluetooth mode')
    else:
        print('Starting in cable mode')


init()
_thread.start_new_thread(core1, ())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
