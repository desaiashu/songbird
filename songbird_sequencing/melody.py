# Melodic sequencing

import random
from songbird_theory.note import note_from_number, number_from_note
from songbird_theory.scale import gen_wide_scale, dissonants_wide_scale, wide_scale_root
from songbird_theory.circle_of_fifths import minor_fifths
from .patterns import e_pattern

class MelodicSequencer:
    def __init__(
        self,
        scale=gen_wide_scale("C", 4, "minor"),
        pattern=e_pattern
    ):
        self.scale = scale
        self.root = scale[wide_scale_root]
        self.note = self.root
        self.pattern_index = 0
        self.pattern = pattern

    def change_scale(self, scale):
        self.scale = scale
        self.root = scale[wide_scale_root]
        self.note = self.root

    def get_last_note(self):
        return self.note

    def get_next_note(self):
        note_index = self.scale.index(self.note)
        if note_index in dissonants_wide_scale:
            self.note = scale[note_index-1]
        elif self.note < self.root:
            self.note = self.scale[random.choice([4, 6, 8])]
        else:
            scale_index = note_index + self.pattern[self.pattern_index]
            if scale_index > 3:
                scale_index = scale_index % 4
            self.pattern_index += 1
            if self.pattern_index == 30:
                self.pattern_index = 0
            self.note = self.scale[scale_index]
        return self.note
