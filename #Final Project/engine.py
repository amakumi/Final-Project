
# THE ENGINE/LOGIC FOR THIS PROJECT

import aubio
import numpy as np
import pyaudio

import time
import argparse

import queue

import music21

# to analyze via command line and to add help; define what argument it wants
parser = argparse.ArgumentParser()
parser.add_argument("-input", required = False, type = int, help = "Audio Input Device")
args = parser.parse_args()

# if the user did not put any input devices
if args.input is None:
    print("""No input device specified. Here are the available input devices to use:
-----------------------------------------------------------------------------------------------------
          """)
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number "+ (str(i)) + ": " + p.get_device_info_by_index(i).get('name'))
    print("""-----------------------------------------------------------------------------------------------------
If you're hopeless, I'd recommend you to type -input 1, or the number of the input you'd like to use.
          """)

    exit()

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream; switching on the mic
stream = p.open(
                format = pyaudio.paFloat32,
                channels = 1,
                rate = 44100,
                input = True,
                input_device_index = args.input,
                frames_per_buffer = 2048
                )
time.sleep(1)

# Aubio's launching and pitch detection
pitch_detection = aubio.pitch("default", 2048, 2048 // 2, 44100)
# Set unit and its silent noise count
pitch_detection.set_unit("Hz")
pitch_detection.set_silence(-40)

q = queue.Queue() # queues the data so it won't overlap one another


def listen(volume_thresh = 1, printOut = False):
    # the main function to record voices from the user
    # Returns the Note Currently Played on the q object when audio is present
    # volume_thresh --> the volume threshold for input (sensitivity of the mic)
    # printOut --> whether or not to print to the terminal

    current_pitch = music21.pitch.Pitch()

    while True:
        # initial data on reading and recording voices using the microphone
        data = stream.read(1024, exception_on_overflow = False)
        samples = np.fromstring(data, dtype = aubio.float_type)
        pitch = pitch_detection(samples)[0]

        # Compute the energy/volume of the current frame
        volume = np.sum(samples ** 2) / len(samples) * 100

        # microphone adjusting so it won't be too loud nor too quiet
        # TOO LOUD = sound unreadable
        # TOO QUIET = sound could not appear
        if pitch and volume > volume_thresh:
            current_pitch.frequency = pitch
        else:
            continue
        # if being asked to print the pitch
        if printOut:
            print(current_pitch)
        # to print the musical note after being 'converted'/'rounded-off' with Cents
        else:
            current = current_pitch.nameWithOctave
            q.put({"Note": current, "Cents": current_pitch.microtone.cents})

if __name__ == "__main__": # to execute the function
    listen(volume_thresh = 1, printOut = True)





########################################################################################################################
# SPECIAL THANKS TO ALL FRIENDS WHO HAVE ACCOMPANIED THE DEV TO CREATE THIS CODE...
#
# Kirk Kaiser - for giving insights and ideas about developing this project --- [https://www.makeartwithpython.com]
# Alifio Rasyid - for giving ideas to develop this code
# Michael Berlian - for giving ideas and tips to develop this code
# Jason Chandra - for giving ideas as well as samples to create codes
# Python Crash Course Book
# Ms. Monica Hidajat - for nurturing and guiding me until now plus giving great tips, tricks and ways to complete tasks
# Kevin Dimas - for doing nothing much really, though you did gave me support, a little
########################################################################################################################