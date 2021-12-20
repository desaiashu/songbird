# This will control playing and pausing melodies along with tempo

from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock

class Transport:
    def __init__(
        self,
    ):
        self.playing = False
        self.sequencers = []

    def msg_handler(self, message):
        if isinstance(message, TimingClock) and self.playing:
            for sequencer in self.sequencers:
                 sequencer.step()
        elif isinstance(message, Start):
            self.playing = True
            for sequencer in self.sequencers:
                 sequencer.start()
            print('start')
        elif isinstance(message, Stop):
            self.playing = False
            for sequencer in self.sequencers:
                 sequencer.stop()
            print('stop')

transport = Transport()
