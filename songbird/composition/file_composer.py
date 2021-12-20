from MIDIFile import MIDIFile

import songbird.clock.clock as clock
from songbird.notes.note import note_from_number, number_from_note
from songbird.theory.circle_of_fifths import minor_fifths
from songbird.sequencing.midi_file import FileSequencer
from songbird.sequencing.melody import MelodicSequencer
from .composer import Composer
from songbird.theory.scale import Scale
from songbird.voices.instrument import Instrument

class FileComposer(Composer):
# Scale initialization
    def __init__(
        self,
        file,
        step_callback=None,
        scale=Scale()
    ):
        super().__init__(scale)

        self.file = file
        self.parse_midi()

        melodic_seq = MelodicSequencer(scale)
        melodic_seq.step_callback = step_callback
        melodic_seq.instrument = Instrument(2)

        file_seq = FileSequencer(scale)
        file_seq.instrument = Instrument(15)

        self.sequencers = [melodic_seq, file_seq]

        for s in self.sequencers:
            clock.register_sequencer(s)


    def parse_midi(self):
        m = MIDIFile(self.file)
        m.parse()
        for idx, track in enumerate(m):
            track.parse()
            print(f'Track {idx}:')
        self.midi_data = m

    # need to store this at the composer level and send down
    def change_scale(self):
        new_index = (minor_fifths.index(note_from_number(self.sequencer.root))+1) % len(minor_fifths)
        new = minor_fifths[new_index]
        self.sequencer.change_scale(Scale(new, 4, "minor", "wide"))
        return self.sequencer.scale.name()
