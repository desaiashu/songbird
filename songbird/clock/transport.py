# This will control playing and pausing melodies along with tempo

from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock

class Transport:
    def __init__(
        self,
    ):
        self.step = -1
        self.playing = False
        self.sequencers = []

    def msg_handler(self, message):
        if isinstance(message, TimingClock) and self.playing:
            self.step = self.step + 1
            if self.step % 6 == 0:
                for sequencer in self.sequencers:
                     sequencer.step()
        elif isinstance(message, Start):
            self.step = -1
            self.playing = True
            print('start')
        elif isinstance(message, Stop):
            self.playing = False
            print('stop')

transport = Transport()
