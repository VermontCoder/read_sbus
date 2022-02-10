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
- A Raspberry Pi (The Library was developed on a Raspberry 3)
- A SBus protocol using RC receiver (Library was tested on an [FrSky XM+ Receiver](https://www.getfpv.com/frsky-xm-sbus-mini-receiver.html))
- An RC transmitter compatible with the RC receiver (Library was tested using a [Taranis Q X7](https://www.frsky-rc.com/product/taranis-q-x7-2/))

In order to connect the receiver with the Rasperry Pi, it is necessary to solder on a 3 pin header (5v, gnd, and SBUS), which came included with xm+ used here.
Then it is plugable into a breadboard or can be directly connected via jumper cables to the Pi.

The transmitter and the receiver must first be "bound" together. To do this binding for the XM+ receiver and the Taranis, there is this [video](https://www.youtube.com/watch?v=ZOBwwNpjNrY). The process can be different for different transmitter/receiver combos, but generally they are similar. In this case there is no actual drone, so rather than
hooking up a battery, simply attach the 5v and gnd leads from the receiver to the Raspberry Pi.

## Software Requirements

read_sbus makes use of two libraries (and optionally a third).

- the [pigpio](https://abyz.me.uk/rpi/pigpio/) library. Installation instructions are in the link. The pigpio daemon must be running. After doing the install, the daemon is configured to startup on reboot.

- the [bitarray](https://pypi.org/project/bitarray/) library. Can be installed via [pip](https://pip.pypa.io/en/stable/).

- (optional) curses library, also installable via pip, though later Raspberian OS installations seem to have this by default. This is only used by the function "display_latest_packet_curses()" in the module. If you do not use this function, you do not need curses.


## Files

3 .py files are in this repository

- **read_sbus_from_GPIO.py** - This is the module. Drop it with your files and import it to use it.
- **read_sbus_from_GPIO_test** - Runs some test code to see if things are behaving correctly. Waits for transmitter to connect before running tests. Device tests assumes hardware is set up as in this [video](https://www.youtube.com/watch?v=pWE8LxcFq9Y). However, if there is no hardware set up, simply nothing will happen.
- **read_sbus_from_GPIO_template** - Basic template which can be modified to quickly get up and running with the library. Copy this file and put your code in the designated section.

## Usage

Basic usage should be done as demonstrated in **read_sbus_from_GPIO_template**. **read_sbus_from_GPIO_test** has additional examples of use.

Before the module can do anything, something like the following code needs to be executed:

```python
import read_sbus_from_GPIO

SBUS_PIN = 4 #pin where sbus wire is plugged in, BCM numbering

reader = read_sbus_from_GPIO.SbusReader(SBUS_PIN)
reader.begin_listen()
```

## Reference
The following methods are supported:
- **SbusReader(SBus_Pin)** - An SbusReader object needs to be created to use the library, passing a BCM pin to listen for SBus frames on. All methods are called on this created object.

- **begin_listen()** - Call before doing anything else with the library.
- **end_listen()** - For clean termination, call after done with the library. Use try/except blocks to call this on error or Keyboard Interrupt is advisable, as shown in examples.
- **display_latest_packet()** - Will print the state of all 16 channels, the age of the latest packet in ms and whether there is a connection or not. It is important to note that this information will not be valid until AFTER a good packet comes in, at least 10ms after a connection has been established between the transmitter and the receiver.
- **display_latest_packet_curses()** - Same as display_latest_packet, but loops continuously updating in a single window. Updates every 50ms. Curses library must be installed via pip to use this method.
- **get_latest_packet_age()** - Returns the age of the latest packet in ms. Note that when receiver is disconnected, it sends the same information over and over again, so the packets are always "fresh" but do not have good information. Use is_connected() to make sure you are connected.
- **is_connected()** - Returns true if the receiver is connected to a transmitter, false otherwise.
- **retrieve_latest_packet()** - Returns the raw bits of latest packet.
- **translate_latest_packet()** - Returns 16 element list containing ints which represent the current channel values. Note that the list index starts at 0, channels start at one, so to retrieve channel#X, look at list index X-1.
- **translate_packet(packet)** - same as translate_latest_packet() except takes a raw bit array as a parameter to turn into a channel list.

## Performance Notes ##

Testing was performed on a fairly unloaded Pi. Aside from typical load, the PI was also running a VNC Server. The device test controlled three different devices simultaneously. Average ms delay was typically around 10ms, with occasional spikes up to around 60ms, especially when servo operations were being done.

While the transmitter/receiver combo is getting packets at a 10ms packet rate, due to the time slicing on the pi, some packet loss is innevitable as the running code does not have exclusive access to the processor. However, for most purposes, this ping rates are probably acceptable. Performance would no doubt degrade if the Pi is more heavily loaded or a less capable Pi is used.

## License
[MIT](https://choosealicense.com/licenses/mit/)
