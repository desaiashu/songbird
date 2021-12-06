from .note import number_from_note, note_from_number

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

def gen_scale(root, octave, mode):
    midi_root = number_from_note(root, octave)
    scale = [midi_root]

    distance = 0
    offset = root_offset[mode]
    for x in range(7):
        distance += base_scale[(x+offset) % 7]
        scale.append(midi_root + distance)

    return scale

def gen_wide_scale(root, octave, mode):

    scale = gen_scale(root, octave, mode)

    lower_root = number_from_note(root, octave-1)
    lower_third_distance = scale[2]-scale[0]
    lower_fifth_distance = scale[4]-scale[0]

    wide_scale = [lower_root-12, lower_root, lower_root+lower_third_distance, lower_root+lower_fifth_distance] + scale

    return wide_scale
