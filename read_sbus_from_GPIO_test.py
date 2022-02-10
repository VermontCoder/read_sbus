import read_sbus_from_GPIO
import time
from statistics import mean

def connection_test(reader):
    print('Waiting for connection...')
    times = []
    try:
        while( not reader.is_connected()):
            time.sleep(.2)
    except KeyboardInterrupt:
        reader.end_listen()
        raise

    print('Connection Established.')


def ping_test(reader):
    print('Waiting for connection...')
    times = []
    try:
        while( not reader.is_connected()):
            time.sleep(.2)
    except KeyboardInterrupt:
        reader.end_listen()
        raise

    print('Timing 5 seconds of packets....')
    time_start = time.time()
    while time.time() - time_start <=5:
        time.sleep(.01) # retrieve every 10ms
        times.append(reader.get_latest_packet_age())
    
    print(f'Average Delay (ms): {mean(times)}, Max Delay (ms): {max(times)}')

def map_value(min_input,max_input,min_output,max_output,invert_mapping,input):
    #for a given input in a range, output to a normalized value in the output range

    input_delta = max_input-min_input
    output_delta = max_output-min_output
    input_percent = (input-min_input)/input_delta
    new_val = min_output+output_delta*input_percent
    if invert_mapping:
        new_val = max_output+min_output-new_val
    return new_val
     

def device_test(reader):
    #demonstrates functionality of library on a servo and two leds connected to PI
    #on GPIOs specified below.

    #servo used here is a Tower Pro Digital MG995R - different servos will require 
    #different pwm settings

    import pigpio
    
    TRANSMITTER_MIN_VAL = 172
    TRANSMITTER_MAX_VAL = 1811
    SERVO_MIN_VAL = 5
    SERVO_MAX_VAL = 30

    LED_MIN_VAL =0
    LED_MAX_VAL = 200

    SERVO_CHANNEL = 5
    SERVO_PIN = 17

    LED_ON_OFF_CHANNEL = 6
    LED_ON_OFF_PIN = 26

    LED_BRIGHTNESS_CHANNEL=1
    LED_BRIGHTNESS_PIN = 13

    LED_ON_OFF_CUTOFF = 500

    
    reader.pi.set_mode(SERVO_PIN, pigpio.OUTPUT)
    reader.pi.set_mode(LED_ON_OFF_PIN, pigpio.OUTPUT)
    reader.pi.set_mode(LED_BRIGHTNESS_PIN, pigpio.OUTPUT)
   

    reader.pi.set_PWM_frequency(SERVO_PIN,50)
    reader.pi.set_PWM_frequency(LED_BRIGHTNESS_PIN,100)
    
    print('ctrl-c to leave device_test....')
    try:
        while(True):
            if reader.is_connected():
                latest_channel_data = reader.translate_latest_packet()

                cur_servo_val = latest_channel_data[SERVO_CHANNEL-1]
                pwm = map_value(TRANSMITTER_MIN_VAL,TRANSMITTER_MAX_VAL,SERVO_MIN_VAL,SERVO_MAX_VAL, True,cur_servo_val)
                reader.pi.set_PWM_dutycycle(SERVO_PIN,pwm)

                cur_led_brightness_val = latest_channel_data[LED_BRIGHTNESS_CHANNEL-1]
                pwm = map_value(TRANSMITTER_MIN_VAL,TRANSMITTER_MAX_VAL,LED_MIN_VAL,LED_MAX_VAL, False,cur_led_brightness_val)
                reader.pi.set_PWM_dutycycle(LED_BRIGHTNESS_PIN,pwm)

                if (latest_channel_data[LED_ON_OFF_CHANNEL-1] > LED_ON_OFF_CUTOFF):
                    reader.pi.write(LED_ON_OFF_PIN,1)
                else:
                    reader.pi.write(LED_ON_OFF_PIN,0)
    except KeyboardInterrupt:
        reader.pi.write(LED_ON_OFF_PIN,0)
        reader.pi.write(LED_BRIGHTNESS_PIN,0)
        return
        

#SBUS connected to pin 4
DATA_PIN = 4

if __name__=="__main__":
    reader = read_sbus_from_GPIO.SbusReader(DATA_PIN)
    reader.begin_listen()
    
    print('Begin Tests...')

    connection_test(reader)
    print('*******')
    
    ping_test(reader)
    print('*******')

    reader.display_latest_packet()
    print('*******')
    
    reader.display_latest_packet_curses()

    device_test(reader)
    
    print('End Tests...')
    reader.end_listen()