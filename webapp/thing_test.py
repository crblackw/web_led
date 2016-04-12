import time

from thing import PiThing

# Create an instance of my pi thing.
pi_thing = PiThing()

# Get the current switch state and print it out.
switch = pi_thing.read_switch()
print('Switch: {0}'.format(switch))

# Blink the LED forever.
print('Blinking LED (Ctrl-C to stop)...')
while True:
    pi_thing.set_led(True)
    time.sleep(0.5)
    pi_thing.set_led(False)
    time.sleep(0.5)
    # Get the current temp and light and print it out.
    light = pi_thing.get_light()
    temp = pi_thing.get_temperature()
    print ('Temp: {0:0.2F}  Light: {1}'.format(temp, light))
