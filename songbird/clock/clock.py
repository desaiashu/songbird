#acts as master clock
#takes in midi clock if it's sensing one, otherwise sets BPM internally
#registers instruments to master clock

import time
from songbird.interface.midi import midi
from songbird.sequencing.sequencer import Sequencer
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.timing_clock import TimingClock

class Transport:
    def __init__(
        self,
    ):
        self.playing = False
        self.sequencers = []

    def pulse(self):
        for sequencer in self.sequencers:
             sequencer.pulse()

    def tick(self):
        for sequencer in self.sequencers:
             sequencer.tick()

    def start(self):
        for sequencer in self.sequencers:
             sequencer.start()
        self.playing = True
        print('start')

    def stop(self):
        for sequencer in self.sequencers:
             sequencer.stop()
        self.playing = False
        print('stop')


# Todos:
# Rewrite midi clock in c++?
# Move to raspberry pi?
# Allow for 48ppq clock? 96ppq clock?

#PPQ = Pulses per quarter note (1 quarter note = 1 beat)
PPQ = 24
NS_PER_MIN = 60000000000
QUARTER_NOTE_PER_BAR = 4 # This may change later
TICKS_PER_PULSE = 4 # Assumes 24ppq clock and 96ppq midi files
TICKS_PER_BAR = TICKS_PER_PULSE*PPQ*QUARTER_NOTE_PER_BAR

class Clock:

    def __init__(
        self,
        internal = True
    ):
        self.internal = internal
        self.transport = Transport()
        if internal:
            self.BPM = 120.0
            self.calc_miliseconds()
        # else:
        #     self.estimated_BPM = 0.0

        self.estimated_BPM = 0.0

        self.midi_time = -1.0
        self.time = 0.0

        self.ticks = 0
        self.pulses = 0

    def register_sequencer(self, sequencer: Sequencer):
        self.transport.sequencers.append(sequencer)

    def set_transport_callback(self, callback):
        self.transport.step_callback = callback

    def pulse(self):
        self.transport.pulse()
        self.time_since_pulse = 0.0
        # if self.internal:
        #     midi.send(TimingClock())

    def tick(self):
        self.transport.tick()
        self.time_since_tick = 0.0

    def start(self):
        self.transport.start()

    def stop(self):
        self.transport.stop()
        self.midi_time = -1.0


    def calc_miliseconds(self, bpm=None):
        if not bpm:
            bpm = self.BPM
        self.ns_per_pulse = NS_PER_MIN/(bpm*PPQ)
        self.ns_per_tick = self.ns_per_pulse / TICKS_PER_PULSE

    def estimate_bpm(self, delta_ns):
        if delta_ns > 0:
            if self.estimated_BPM == 0.0:
                self.estimated_BPM = NS_PER_MIN/(self.time_since_pulse*PPQ)
            else:
                self.estimated_BPM = 0.5 * (self.estimated_BPM + NS_PER_MIN/(self.time_since_pulse*PPQ))
            self.calc_miliseconds(self.estimated_BPM)
            # print(self.estimated_BPM)

    def get_midi_and_delta_time(self):
        current_time = time.monotonic_ns()
        if self.midi_time >=0:
            delta_time = (current_time - self.time)
            self.midi_time += delta_time
            self.time_since_tick += delta_time
            self.time_since_pulse += delta_time
        else:
            delta_time = 0
            self.midi_time = 0.0
            self.time_since_tick = 0.0
            self.time_since_pulse = 0.0
        self.time = current_time
        return delta_time

    def handler(self):
        delta = self.get_midi_and_delta_time()
        if self.internal:
            if self.transport.playing:
                if self.time_since_tick >= self.ns_per_tick:
                    self.tick()
                if self.time_since_pulse >= self.ns_per_pulse:
                    self.pulse()
        else:
            msg = midi.receive()
            if msg is not None:
                if isinstance(message, TimingClock) and self.transport.playing:
                    self.estimate_bpm(delta)
                    self.pulse()
                elif isinstance(message, Start):
                    self.start()
                elif isinstance(message, Stop):
                    self.stop()
            elif self.estimated_BPM > 0:
                if self.time_since_tick > self.ns_per_tick:
                    self.tick()


clock = Clock()
