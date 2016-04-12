import RPi.GPIO as GPIO
import spidev
import os
import glob
import time
import threading

LED_PIN = 23
SWITCH_PIN = 24
LIGHT_ADC = 0

# Set up SPI
spi = spidev.SpiDev()
spi.open(0, 0)

# Set up Dallas 1-wire
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


class PiThing(object):
    """Raspberry Pi Internet 'Thing'."""

    def __init__(self):
        # Set up GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)  # LED as an output.
        GPIO.setup(SWITCH_PIN, GPIO.IN)  # Switch as an input.
        self._lock = threading.Lock()
        self._temperature = None
        self._light = None
        # Create and start sensor reading thread in the background.
        self._sensor_thread = threading.Thread(target=self._sensor_update)
        self._sensor_thread.daemon = True
        self._sensor_thread.start()

    def read_switch(self):
        """Read the state of the switch and return it (as a boolen).
        """
        with self._lock:
            return GPIO.input(SWITCH_PIN)

    def set_led(self, value):
        """Change the LED to the passed in value, either True for on or False
        for off.
        """
        with self._lock:
            GPIO.output(LED_PIN, value)

    def get_temperature(self):
        with self._lock:
            return self._temperature

    def get_light(self):
        with self._lock:
            return self._light

    def _sensor_update(self):
        """Main function for updating sensors."""
        while True:
            with self._lock:
                self._temperature = self._read_temp()
                self._light = self._read_light()
            time.sleep(2.0)

    def _read_temp(self):
        """Read the current temperature and return it.
        """
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            # time.sleep(0.2)
            lines = read_temp_raw
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def _read_temp_raw(self):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_light(self):
        """Read the current light level and return it.
        """
        return self._readadc(LIGHT_ADC)

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def _readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        r = spi.xfer2([1, (8 + adcnum) << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout
