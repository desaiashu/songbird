from .midi_note import start_note, end_note

class Midi_instrument:
    def __init__(
        self,
        out_channel=1
    ):
        self.channel = out_channel

    def start_note(self, note, velocity):
        start_note(note, velocity, self.channel)

    def end_note(self, note):
        end_note(note, self.channel)
