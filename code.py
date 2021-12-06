# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# midi_UARToutdemo.py - demonstrates sending MIDI notes

import time
from time import sleep
import random
import board
import busio
import adafruit_midi

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock
from songbird_music.note import note_from_number
from songbird_interface.display import Display
import songbird_music.scale


# LED code here

display = Display("Cminor", "")

# Midi code below

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART
midi_in_channel = 2
midi_out_channel = 2
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=False,
)
note_hold = 0.85
rest = note_hold / 5

print("MIDI Out demo")
print("Default output channel:", midi.out_channel + 1)


note = 59
root = 60
step = -1
playing = False

scale = [-24, -12, -9, -5, 0, 2, 3, 5, 7, 8, 10, 12]
unstable = [-24, -12, -9, -5, 2, 5, 8, 10]
stable = [-24, -12, -9, -5, 0, 3, 7, 12]

# fib = [1, 1, 2, 3, 5, 8]
fib = [2,7,1,8,2,8,1,8,2,8,4,5,9,0,4,5,2,3,5,3,6,0,2,8,7,4,7,1,3,5,2,7]
fib_index = 0

def get_last_note():
    return note

def get_next_note():
    global note
    global root
    global fib_index
    dist = note - root
    if dist in stable:
        scale_index = scale.index(dist) + fib[fib_index]
        if scale_index > 3:
            scale_index = scale_index % 4
        fib_index += 1
        if fib_index == 30:
            fib_index = 0
        note = root + scale[scale_index]
        note = random.choice([note])
    elif dist in unstable:
        if dist < 0:
            note = root
        elif dist < 8:
            note = note-2
        elif dist < 10:
            note = note-1
        else:
            note = note+2
        #note = note + random.choice((-1, 1))
    else:
        note = root + random.choice(stable)
        note = random.choice([note])
    print(note)
    return note

def msg_handler(message):
    global step
    global playing
    global display
    if isinstance(message, TimingClock) and playing:
        last_note = get_last_note()
        if last_note > 0:
          midi.send(NoteOff(last_note, 0))
        step = step + 1
        if step % 6 == 0:
            send = random.choice([1, 1, 1])
            if send == 1:
                next_note = get_next_note()
                if next_note > 0:
                  vel = random.choice([64, 90, 127])
                  midi.send(NoteOn(next_note, vel))
                  display.setLabel2(note_from_number(next_note))
    elif isinstance(message, Start):
        step = -1
        playing = True
        print('start')
    elif isinstance(message, Stop):
        playing = False
        print('stop')

while True:
    msg = midi.receive()
    if msg is not None:
        msg_handler(msg)
    time.sleep(0.005)
