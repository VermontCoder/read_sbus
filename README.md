# read_sbus
read_sbus is a module for the Rasperry Pi to read SBus protocol input. SBus is a protocol used by many RC receivers to send data to flight controllers to control RC aircraft,
quadcopters or cars. SBus has an advantage over standard PWM in that up to 16 channels of data can be sent over a single data line.

The basic architecture here is as follows:
- Transmitter sends out 16 channels of data over a wireless link approximately every 10ms.
- Receiver receives the data and sends it out via the sbus protocol on the data wire.
- Raspberry Pi sees this as high/low pulses which are translated into bits by sampling the state every 10 microseconds.
- Lots of pulse activity followed by a continuous signal for about 6ms comprises a single packet of data.
- Raspberry Pi program loops over and over using the read_sbus library to pickup the data sent by transmitter.
- As the user adjusts the transmitter, the values for a particular channel change. The mapping of the transmitter control to the channel is controlled by the transmitter.
- In the loop, the programmer puts code to react to whatever values are coming through

## Hardware Requirements
- A Rasperry Pi (The Library was developed on a Rasperry 3)
- A SBus protocol using RC receiver (Library was tested on an [FrSky XM+ Receiver](https://www.getfpv.com/frsky-xm-sbus-mini-receiver.html))
- An RC transmitter compatible with the RC receiver (Library was tested using a [Taranis Q X7](https://www.frsky-rc.com/product/taranis-q-x7-2/))

In order to connect the receiver with the Rasperry Pi, it is necessary to solder on a 3 pin header (5v, gnd, and SBUS), which came included with xm+ used here.
Then it is plugable into a breadboard or can be directly connected via jumper cables to the Pi.

The transmitter and the receiver must first be "bound" together. To do this binding for the XM+ receiver and the Taranis, there is this [video](https://www.youtube.com/watch?v=ZOBwwNpjNrY). The process can be different for different transmitter/receiver combos, but generally they are similar. In this case there is no actual drone, so rather than
hooking up a battery, simply attach the 5v and gnd leads from the receiver to the Raspberry Pi.

## Software Requirements

read_sbus makes use of two libraries (and optionally a third).

- the [pigpio](https://abyz.me.uk/rpi/pigpio/) library. Installation instructions are in the link. The pigpio daemon must be running. After doing the install, the daemon is configured to startup on reboot.

- the bitarray(https://pypi.org/project/bitarray/) library. Can be installed via [pip] (https://pip.pypa.io/en/stable/).

- (optional) curses library, also installable via pip, though later Raspberian OS installations seem to have this by default. This is only used by the function "display_latest_packet_curses()" in the module. If you do not use this function, you do not need curses.


## Files

3 .py files are in this repository

- **read_sbus_from_GPIO.py** - This is the module. Drop it with your files and import it to use it.
- **read_sbus_from_GPIO_test** - Runs some test code to see if things are behaving correctly. Waits for transmitter to connect before running tests. Device tests assumes hardware is set up as in this [video](TBD). However, if there is no hardware set up, simply nothing will happen.
- **read_sbus_from_GPIO_template** - Basic template which can be modified to quickly get up and running with the library. Copy this file and put your code in the designated section.

## Usage

Basic usage should be done as demonstrated in **read_sbus_from_GPIO_template**. **read_sbus_from_GPIO_test** has additional examples of use.

Before the module can do anything, something like the following code needs to be executed:

```python
import read_sbus_from_GPIO

SBUS_PIN = 4 #pin where sbus wire is plugged in, whatever wire

reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
reader.begin_listen()

## Reference



## License
[MIT](https://choosealicense.com/licenses/mit/)
