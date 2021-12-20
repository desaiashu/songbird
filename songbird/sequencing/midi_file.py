from .sequencer import Sequencer

class FileSequencer(Sequencer):
    def __init__(
        self,
        track
    ):
        self.track = track

    def step(self):
        pass
