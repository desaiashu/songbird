# Melodic sequencing
import random
from songbird.notes.note import note_from_number, number_from_note
from songbird.theory.scale import Scale
from songbird.theory.circle_of_fifths import minor_fifths
from .patterns import e_pattern

from .sequencer import Sequencer

class MelodicSequencer(Sequencer):
    def __init__(
        self,
        scale=Scale(),
        pattern=e_pattern,
    ):
        super().__init__(scale)
        self.pattern_index = 0
        self.pattern = pattern
        self.instrument = None
        self.step = -1

    def get_last_note(self):
        return self.note

    def get_next_note(self):
        note_index = self.scale.notes.index(self.note)
        if note_index in self.scale.dissonants:
            self.note = scale.notes[note_index-1]
        elif self.note < self.root:
            self.note = self.scale.notes[random.choice([4, 6, 8])]
        else:
            scale_index = note_index + self.pattern[self.pattern_index]
            if scale_index > 3:
                scale_index = scale_index % 4
            self.pattern_index += 1
            if self.pattern_index == 30:
                self.pattern_index = 0
            self.note = self.scale.notes[scale_index]
        return self.note

    def step(self):
        self.step = self.step + 1
        if self.step % 6 == 0:
            last_note = self.get_last_note()
            if last_note > 0:
                if self.instrument:
                    self.instrument.end_note(last_note)
            next_note = self.get_next_note()
            if next_note > 0:
                vel = random.choice([64, 90, 127])
                if self.instrument:
                    self.instrument.start_note(next_note, vel)
                    if self.step_callback:
                        self.step_callback(note_from_number(next_note))

    def stop(self):
        self.step = -1
