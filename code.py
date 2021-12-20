import time
import songbird.interface.program as program
import songbird.clock.clock as clock

from MIDIFile import MIDIFile

m = MIDIFile('midifiles/rats.mid')
m.parse()
print(m.tracks)
print(m.tracks[0])
print('yay')

# Run loop
while True:
    program.handler()
    clock.handler()
    time.sleep(0.005)
