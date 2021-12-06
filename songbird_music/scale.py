from .note import number_from_note, note_from_number

# scale structures
base_scale = [2,2,1,2,2,2,1]

root_offset = {
    "major": 0,
    "dorian": 1,
    "phrygian": 2,
    "lydian": 3,
    "mixolydian": 4,
    "minor": 5,
    "locrian": 6
}

def gen_scale(root, octave, mode):
    midi_root = number_from_note(root, octave)
    scale = [midi_root]

    distance = 0
    offset = root_offset[mode]
    for x in range(7):
        distance += base_scale[(x+offset) % 7]
        scale.append(midi_root + distance)

    return scale

scale = ""
for n in gen_scale("C", 4, "minor"):
    scale = scale + note_from_number(n) + " "
print(scale)
