import time
from time import sleep
import board
import busio

from songbird_theory.note import note_from_number, number_from_note
from songbird_theory.scale import gen_wide_scale
from songbird_theory.circle_of_fifths import minor_fifths

from songbird_sequencing.melody import MelodicSequencer
from songbird_sequencing.transport import Transport

from songbird_interface.midi import initialize_midi
from songbird_interface.display import Display
from songbird_interface.buttons import Buttons


# Scale initialization
scale = gen_wide_scale("C", 4, "minor")


# Midi and sequencer initialization
midi = initialize_midi()
melody = MelodicSequencer(scale)
transport = Transport(midi, [melody])


# Display initialization and callback
display = Display("Cminor", "")

def transport_step_callback(next_note):
    display.setLabel2(note_from_number(next_note))


# Button initialization and callback
def button_1_callback():
    global melody
    new_index = (minor_fifths.index(note_from_number(melody.root))+1) % len(minor_fifths)
    new = minor_fifths[new_index]
    melody.change_scale(gen_wide_scale(new, 4, "minor"))
    display.setLabel1(new+"minor")

buttons = Buttons(button_1_callback)


# Run loop
while True:
    msg = midi.receive()
    if msg is not None:
        transport.msg_handler(msg, transport_step_callback)
    buttons.checkClicks()
    time.sleep(0.005)
