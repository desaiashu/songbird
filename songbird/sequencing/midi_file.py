from .sequencer import Sequencer
from songbird.clock.clock import TICKS_PER_BAR
from MIDIFile.events import MIDIEvent

class FileSequencer(Sequencer):
    def __init__(
        self,
        track
    ):
        self.track = track
        self.length = len(track)
        self.index = 0
        self.ticks = 0

        # print(track)
        # for i in range(0, 20):
        #     print(track.events[i])

    def tick(self):
        self.ticks += 1
        if self.index == self.length and self.ticks % TICKS_PER_BAR == 0:
            self.ticks = 0
            self.index = 0

        while (self.index < self.length and self.ticks >= self.track.events[self.index].time):
            event = self.track.events[self.index]
            if isinstance(event, MIDIEvent) and event.command in [0x80, 0x90]:
                note = event.message.note.number
                vel = event.message.velocity
                if event.message.onOff == 'ON':
                    self.instrument.start_note(note, vel)
                else:
                    self.instrument.end_note(note)
            self.index += 1
