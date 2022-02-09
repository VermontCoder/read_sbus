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

The transmitter and the receiver must first be "bound" together. To do this binding for the XM+ receiver and the Taranis, there is this [video]

## Software Requirements

- read_sbus 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
