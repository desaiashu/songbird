#acts as master clock
#takes in midi clock if it's sensing one, otherwise sets BPM internally
#registers instruments to master clock

from .transport import transport
from songbird.interface.midi import midi
from songbird.sequencing.sequencer import Sequencer

def register_sequencer(sequencer: Sequencer):
    transport.sequencers.append(sequencer)

def set_transport_callback(callback):
    transport.step_callback = callback

def handler():
    msg = midi.receive()
    if msg is not None:
        transport.msg_handler(msg)
