#high level definition of an instrument which serves as a "voice" for the composition

from .midi.midi_inst import Midi_instrument

class Instrument:
    def __init__(
        self,
        midi_channel=1
    ):
        self.midi_inst = Midi_instrument(midi_channel)

    def start_note(self, note, velocity):
        self.midi_inst.start_note(note, velocity)

    def end_note(self, note):
        self.midi_inst.end_note(note)
