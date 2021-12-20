# a composer that only composes for one instrument and a chorus, mostly for testing

import songbird.clock.clock as clock
from songbird.notes.note import note_from_number, number_from_note
from songbird.theory.circle_of_fifths import minor_fifths
from songbird.sequencing.melody import MelodicSequencer
from .composer import Composer
from songbird.theory.scale import Scale
from songbird.voices.instrument import Instrument

class BasicComposer(Composer):
# Scale initialization
    def __init__(
        self,
        step_callback=None,
        scale=Scale()
    ):
        super().__init__(scale)
        self.sequencer = MelodicSequencer(scale)
        self.sequencer.step_callback = step_callback
        self.instrument = Instrument(2)
        self.sequencer.instrument = self.instrument

        clock.register_sequencer(self.sequencer)

    def change_scale(self):
        new_index = (minor_fifths.index(self.scale.root_note)+1) % len(minor_fifths)
        new = minor_fifths[new_index]
        self.scale = Scale(new, 4, "minor", "wide")
        self.sequencer.change_scale(self.scale)
        return self.scale.name()
