import time
import songbird.interface.program as program
import songbird.clock.clock as clock

from MIDIFile import MIDIFile

m = MIDIFile('midifiles/Grooves From Mars/CR-78/Patterns/CR-78 Waltz A.mid')
m.parse()
for idx, track in enumerate(m):
    track.parse()
    print(f'Track {idx}:')
    print(str(track))
print('yay')

# Run loop
while True:
    program.handler()
    clock.handler()
    time.sleep(0.005)
