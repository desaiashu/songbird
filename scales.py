import numpy as np

# scale structures
major = np.array([2,2,1,2,2,2,1])
minor = np.array([2,1,2,2,1,2,2])
chromatic = np.array([1,1,1,1,1,1,1,1,1,1,1,1])

# roots
roots = {"A": 21, "B": 22, "C":23, "D":24, "E":25, "F":26, "G":27}
gen_octave_offset = lambda octave: 12*octave

def gen_scale(root, octave, scale_type):
  midi_root = roots[root]
  steps = np.cumsum(scale_type)
  new_midi_root = midi_root + gen_octave_offset(octave)
  sequence = new_midi_root + steps
  scale = np.insert(sequence,0,new_midi_root)
  return scale

# example: generate the A4 major scale (one octave)
root = "A"
octave = 4

A4_major = gen_scale(root, octave, major)
print(A4_major)
