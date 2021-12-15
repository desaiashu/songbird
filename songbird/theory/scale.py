from songbird.notes.note import number_from_note, note_from_number

# scale structures
base_scale = [2,2,1,2,2,2,1]
dissonants = [1, 5]
dissonants_wide_scale = [5, 9]
wide_scale_root = 4

root_offset = {
    "major": 0,
    "dorian": 1,
    "phrygian": 2,
    "lydian": 3,
    "mixolydian": 4,
    "minor": 5,
    "locrian": 6
}

class Scale:
    def __init__(
        self,
        root_note="C",
        octave=4,
        mode="minor",
        type="wide",
    ):
        self.root_note = root_note
        self.root = number_from_note(root_note, octave)
        self.offset = root_offset[mode]
        self.dissonants = []
        self.mode = mode
        self.octave = octave
        self.type = type

        if type == "wide":
            self.gen_wide_scale(),
        else:
            self.gen_scale()

    def name(self):
        return self.root_note + " " + self.mode

    def gen_scale(self):
        self.notes = [self.root]
        distance = 0
        for x in range(7):
            distance += base_scale[(x+self.offset) % 7]
            self.notes.append(self.root + distance)
        self.dissonants = dissonants

    def gen_wide_scale(self):
        self.gen_scale()
        lower_root = self.root - 12
        lower_third_distance = self.notes[2]-self.notes[0]
        lower_fifth_distance = self.notes[4]-self.notes[0]
        self.notes = [lower_root-12, lower_root, lower_root+lower_third_distance, lower_root+lower_fifth_distance] + self.notes
        self.dissonants = dissonants_wide_scale
