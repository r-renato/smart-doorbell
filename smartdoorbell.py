# import the library
import os
from pickle import FALSE, TRUE
import subprocess
import time
import configparser
import OPi.GPIO as GPIO

AUDIO_DIRECTORY = '/home/pi/doorbell/audio'
CHANNEL = 'PA7'
IN_EXECUTION = FALSE

def get_audio_clips():
    """Returns paths to all available audio clips"""
    list_of_clips = []
    for file in os.listdir(AUDIO_DIRECTORY):
        if file.endswith('.mp3'):
            list_of_clips.append(os.path.join(AUDIO_DIRECTORY, file))
    return list_of_clips


def play_clip():
    clips = get_audio_clips()
    if not clips:
        print('No audio clips available')
        exit(1)
    random_clip = random.choice(clips)
    print('playing clip {}'.format(random_clip))
    subprocess.call(['mpg321', random_clip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def button_pressed_callback(channel):
    global IN_EXECUTION

    if IN_EXECUTION == FALSE:
        IN_EXECUTION = TRUE

        print('Button Pressed')

        IN_EXECUTION = FALSE

def button_released_callback(channel):
    print('Button release')



if __name__ == '__main__':
# GPIO setup
    GPIO.setmode(GPIO.SUNXI)
    GPIO.setwarnings(False)
    GPIO.setup(CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(CHANNEL, GPIO.RISING)
    GPIO.add_event_callback(CHANNEL, button_pressed_callback)
    GPIO.add_event_callback(CHANNEL, button_released_callback)
    
# INI load
    config = configparser.ConfigParser()
    config.read('smartdoorbell.ini')

# loop
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
	    GPIO.cleanup()


