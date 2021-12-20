from .sequencer import Sequencer

class FileSequencer(Sequencer):
    def __init__(
        self,
        track
    ):
        self.track = track

        for i in range(0, 25):
            print(track.events[i])

    def step(self):
        pass
