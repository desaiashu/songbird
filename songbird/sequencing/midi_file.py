from .sequencer import Sequencer

class FileSequencer(Sequencer):
    def __init__(
        self,
        track
    ):
        self.track = track

        # print(track)
        # for i in range(0, 20):
        #     print(track.events[i])

    def tick(self):
        pass
