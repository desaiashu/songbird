# This will control playing and pausing melodies along with tempo

import random
import adafruit_midi

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock

class Transport:
    def __init__(
        self,
        midi=None,
        sequencers=[]
    ):
        self.step = -1
        self.playing = False
        self.midi = midi
        self.sequencers = sequencers

    def msg_handler(self, message, step_callback):
        if isinstance(message, TimingClock) and self.playing:
            for sequencer in self.sequencers:
                last_note = sequencer.get_last_note()
                if last_note > 0:
                  self.midi.send(NoteOff(last_note, 0))
                self.step = self.step + 1
                if self.step % 6 == 0:
                    next_note = sequencer.get_next_note()
                    if next_note > 0:
                        vel = random.choice([64, 90, 127])
                        self.midi.send(NoteOn(next_note, vel))
                        if step_callback:
                          step_callback(next_note)
        elif isinstance(message, Start):
            self.step = -1
            self.playing = True
            print('start')
        elif isinstance(message, Stop):
            self.playing = False
            print('stop')
