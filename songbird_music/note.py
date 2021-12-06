
note_index = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#","B"]
middle_c_offset = 60

gen_octave_offset = lambda octave: 12*octave

def number_from_note(note, octave):
    note_num = note_index.index(note)
    return note_num + gen_octave_offset(octave)

def note_from_number(num):
    note_num = num % 12
    return note_index[note_num]
